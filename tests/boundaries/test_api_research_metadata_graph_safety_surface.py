from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


GRAPH_ENDPOINTS = [
    "/research-metadata-graph/health",
    "/research-metadata-graph/planning",
    "/research-metadata-graph/readiness",
    "/research-metadata-graph/node-placeholder",
    "/research-metadata-graph/edge-placeholder",
    "/research-metadata-graph/provenance-placeholder",
    "/research-metadata-graph/lifecycle-placeholder",
    "/research-metadata-graph/reference-placeholder",
    "/research-metadata-graph-api/health",
    "/research-metadata-graph-api/contracts",
    "/research-metadata-graph-api/unavailable-template",
    "/research-metadata-graph-api/request-placeholder",
    "/research-metadata-graph-api/response-placeholder",
    "/research-metadata-graph-api/reference-placeholder",
    "/research-metadata-graph-display/health",
    "/research-metadata-graph-display/contracts",
    "/research-metadata-graph-display/unavailable-template",
    "/research-metadata-graph-display/node-placeholder",
    "/research-metadata-graph-display/edge-placeholder",
    "/research-metadata-graph-display/provenance-placeholder",
    "/research-metadata-graph-display/lifecycle-placeholder",
    "/research-metadata-graph-display/reference-placeholder",
]

DANGEROUS_FLAGS = [
    "active_ui_enabled",
    "frontend_components_enabled",
    "desktop_components_enabled",
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


def test_research_metadata_graph_planning_api_display_get_endpoints_still_work() -> None:
    for endpoint in GRAPH_ENDPOINTS:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint
        body = response.json()
        assert body["read_only"] is True
        assert body["unavailable_by_default"] is True
        assert body["no_graph_database"] is True
        assert body["no_graph_traversal"] is True
        assert body["no_graph_search"] is True
        assert body["no_graph_ranking"] is True
        assert body["no_graph_retrieval"] is True
        assert body["no_embeddings_vector_store"] is True
        assert body["no_ingestion_storage_upload_download_preview"] is True
        assert body["no_paper_parsing"] is True
        assert body["no_strategy_generation"] is True
        assert body["no_backtesting"] is True
        assert body["no_recommendations"] is True
        assert body["no_execution"] is True
        _assert_no_secrets_or_enabled_dangerous_flags(body)


def test_research_metadata_graph_route_families_are_get_only() -> None:
    routes = [
        route
        for route in _iter_routes(app.routes)
        if getattr(route, "path", "").startswith("/research-metadata-graph")
    ]
    discovered = {getattr(route, "path", "") for route in routes}
    assert set(GRAPH_ENDPOINTS) <= discovered
    for route in routes:
        assert getattr(route, "methods", set()) <= {"GET"}


def test_research_metadata_graph_route_families_have_no_unsafe_paths() -> None:
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
        if not path.startswith("/research-metadata-graph"):
            continue
        segments = {segment for segment in path.lower().split("/") if segment}
        for term in forbidden_segments:
            if term in segments:
                bad.append(f"{path}:{term}")

    assert bad == []
