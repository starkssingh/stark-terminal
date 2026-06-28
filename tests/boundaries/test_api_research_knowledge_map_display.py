from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


KNOWLEDGE_MAP_DISPLAY_ENDPOINTS = [
    "/research-knowledge-map-display/health",
    "/research-knowledge-map-display/contracts",
    "/research-knowledge-map-display/unavailable-template",
    "/research-knowledge-map-display/item-placeholder",
    "/research-knowledge-map-display/relationship-placeholder",
    "/research-knowledge-map-display/evidence-placeholder",
    "/research-knowledge-map-display/provenance-placeholder",
    "/research-knowledge-map-display/lifecycle-placeholder",
]

DANGEROUS_FLAGS = [
    "active_ui_enabled",
    "frontend_components_enabled",
    "desktop_components_enabled",
    "active_map_enabled",
    "database_enabled",
    "persistent_writes_enabled",
    "traversal_enabled",
    "search_enabled",
    "ranking_enabled",
    "retrieval_enabled",
    "embeddings_enabled",
    "vector_store_enabled",
    "active_ingestion_enabled",
    "file_uploads_enabled",
    "file_downloads_enabled",
    "file_previews_enabled",
    "paper_parsing_enabled",
    "strategy_generation_enabled",
    "backtesting_enabled",
    "recommendations_enabled",
    "execution_enabled",
    "broker_controls_enabled",
    "readiness_to_trade_enabled",
    "active_decision_objects_enabled",
]


def _iter_routes(routes):
    for route in routes:
        yield route
        original_router = getattr(route, "original_router", None)
        if original_router is not None:
            yield from _iter_routes(getattr(original_router, "routes", []))


def _assert_no_secrets_or_enabled_dangerous_flags(value) -> None:
    serialized = str(value).lower()
    for secret_term in ["api_key", "token", "password", "secret", "credential"]:
        assert secret_term not in serialized
    if isinstance(value, dict):
        for key, item in value.items():
            if key in DANGEROUS_FLAGS:
                assert item is False
            _assert_no_secrets_or_enabled_dangerous_flags(item)
    elif isinstance(value, list):
        for item in value:
            _assert_no_secrets_or_enabled_dangerous_flags(item)


def test_research_knowledge_map_display_get_endpoints_work() -> None:
    for endpoint in KNOWLEDGE_MAP_DISPLAY_ENDPOINTS:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint
        body = response.json()
        assert body["service"] == "stark-terminal-research-knowledge-map-display"
        assert body["display_contract_skeleton_only"] is True
        assert body["read_only"] is True
        assert body["unavailable_by_default"] is True
        assert body["active_ui_enabled"] is False
        assert body["frontend_components_enabled"] is False
        assert body["desktop_components_enabled"] is False
        assert body["active_map_enabled"] is False
        assert body["database_enabled"] is False
        assert body["search_enabled"] is False
        assert body["retrieval_enabled"] is False
        assert body["execution_enabled"] is False
        _assert_no_secrets_or_enabled_dangerous_flags(body)


def test_research_knowledge_map_display_routes_are_get_only() -> None:
    routes = [
        route
        for route in _iter_routes(app.routes)
        if getattr(route, "path", "").startswith("/research-knowledge-map-display")
    ]
    discovered = {getattr(route, "path", "") for route in routes}
    assert set(KNOWLEDGE_MAP_DISPLAY_ENDPOINTS) <= discovered
    for route in routes:
        assert getattr(route, "methods", set()) <= {"GET"}


def test_research_knowledge_map_display_routes_have_no_unsafe_paths() -> None:
    forbidden_segments = [
        "broker",
        "order",
        "execution",
        "trade",
        "upload",
        "download",
        "preview",
        "ingest",
        "store",
        "database",
        "traversal",
        "query",
        "search",
        "ranking",
        "retrieval",
        "embedding",
        "vector",
        "parse",
        "strategy",
        "backtest",
        "recommendation",
        "ui",
        "frontend",
        "desktop",
    ]
    bad: list[str] = []
    for route in _iter_routes(app.routes):
        path = getattr(route, "path", "")
        if not path.startswith("/research-knowledge-map-display"):
            continue
        segments = {segment for segment in path.lower().split("/") if segment}
        for term in forbidden_segments:
            if term in segments:
                bad.append(f"{path}:{term}")

    assert bad == []
