from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


GRAPH_API_ENDPOINTS = [
    "/research-metadata-graph-api/health",
    "/research-metadata-graph-api/contracts",
    "/research-metadata-graph-api/unavailable-template",
    "/research-metadata-graph-api/request-placeholder",
    "/research-metadata-graph-api/response-placeholder",
    "/research-metadata-graph-api/reference-placeholder",
]

DANGEROUS_FLAGS = [
    "graph_database_enabled",
    "persistent_writes_enabled",
    "graph_traversal_enabled",
    "graph_search_enabled",
    "graph_ranking_enabled",
    "graph_retrieval_enabled",
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


def test_research_metadata_graph_api_get_endpoints_work() -> None:
    for endpoint in GRAPH_API_ENDPOINTS:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint
        body = response.json()
        assert body["service"] == "stark-terminal-research-metadata-graph-api"
        assert body["api_contract_skeleton_only"] is True
        assert body["read_only"] is True
        assert body["unavailable_by_default"] is True
        _assert_no_secrets_or_enabled_dangerous_flags(body)


def test_research_metadata_graph_api_routes_are_get_only() -> None:
    routes = [
        route
        for route in _iter_routes(app.routes)
        if getattr(route, "path", "").startswith("/research-metadata-graph-api")
    ]
    discovered = {getattr(route, "path", "") for route in routes}
    assert set(GRAPH_API_ENDPOINTS) <= discovered
    for route in routes:
        assert getattr(route, "methods", set()) <= {"GET"}


def test_research_metadata_graph_api_routes_have_no_unsafe_paths() -> None:
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
    ]
    bad: list[str] = []
    for route in _iter_routes(app.routes):
        path = getattr(route, "path", "")
        if not path.startswith("/research-metadata-graph-api"):
            continue
        segments = {segment for segment in path.lower().split("/") if segment}
        for term in forbidden_segments:
            if term in segments:
                bad.append(f"{path}:{term}")

    assert bad == []
