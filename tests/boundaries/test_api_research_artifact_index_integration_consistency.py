from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


INDEX_ENDPOINTS = [
    "/research-artifact-index/health",
    "/research-artifact-index/contracts",
    "/research-artifact-index/placeholder-index",
    "/research-artifact-index/readiness-template",
    "/research-artifact-index/unavailable-template",
    "/research-artifact-index-api/health",
    "/research-artifact-index-api/contracts",
    "/research-artifact-index-api/unavailable-template",
    "/research-artifact-index-api/response-placeholder",
    "/research-artifact-index-api/reference-placeholder",
    "/research-artifact-index-display/health",
    "/research-artifact-index-display/contracts",
    "/research-artifact-index-display/unavailable-template",
    "/research-artifact-index-display/placeholder-card",
    "/research-artifact-index-display/placeholder-reference",
    "/research-artifact-index-display/placeholder-tag",
    "/research-artifact-index-display/placeholder-provenance",
    "/research-artifact-index-display/placeholder-lifecycle",
    "/research-artifact-index-boundary/health",
    "/research-artifact-index-boundary/contracts",
    "/research-artifact-index-boundary/invariants",
]

DANGEROUS_ENABLED_FLAGS = [
    "active_ui_enabled",
    "frontend_components_enabled",
    "desktop_components_enabled",
    "indexing_engine_enabled",
    "search_engine_enabled",
    "ranking_engine_enabled",
    "retrieval_engine_enabled",
    "embeddings_enabled",
    "vector_store_enabled",
    "active_ingestion_enabled",
    "persistent_storage_enabled",
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


def _assert_safe_response(body: dict) -> None:
    serialized = str(body).lower()
    for secret_term in ["api_key", "token", "password", "secret", "credential"]:
        assert secret_term not in serialized
    for flag in DANGEROUS_ENABLED_FLAGS:
        if flag in body:
            assert body[flag] is False


def test_all_research_artifact_index_endpoint_families_still_work() -> None:
    for endpoint in INDEX_ENDPOINTS:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint
        body = response.json()
        assert body["service"].startswith("stark-terminal-research-artifact-index")
        _assert_safe_response(body)


def test_research_artifact_index_route_families_are_get_only() -> None:
    routes = [
        route
        for route in _iter_routes(app.routes)
        if getattr(route, "path", "").startswith("/research-artifact-index")
    ]
    discovered = {getattr(route, "path", "") for route in routes}
    assert set(INDEX_ENDPOINTS) <= discovered

    for route in routes:
        assert getattr(route, "methods", set()) <= {"GET"}


def test_research_artifact_index_route_families_have_no_unsafe_paths() -> None:
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
        "indexing",
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
        if not path.startswith("/research-artifact-index"):
            continue
        segments = {segment for segment in path.lower().split("/") if segment}
        for term in forbidden_segments:
            if term in segments:
                bad.append(f"{path}:{term}")

    assert bad == []
