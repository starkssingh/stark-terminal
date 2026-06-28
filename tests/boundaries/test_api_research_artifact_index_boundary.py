from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


def _assert_safe_response(body: dict) -> None:
    serialized = str(body).lower()
    assert "api_key" not in serialized
    assert "token" not in serialized
    assert "password" not in serialized
    assert body["service"] == "stark-terminal-research-artifact-index-boundary"
    assert body.get("system_boundary_hardening_only", True) is True
    for key in [
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
    ]:
        if key in body:
            assert body[key] is False


def test_research_artifact_index_boundary_health_endpoint() -> None:
    response = client.get("/research-artifact-index-boundary/health")
    assert response.status_code == 200
    body = response.json()
    assert body["stage"] == "system_boundary_hardening"
    assert body["invariants_passed"] is True
    assert body["forbidden_behavior_count"] >= 30
    _assert_safe_response(body)


def test_research_artifact_index_boundary_contracts_endpoint() -> None:
    response = client.get("/research-artifact-index-boundary/contracts")
    assert response.status_code == 200
    body = response.json()
    assert "INDEXING_ENGINE" in body["forbidden_behaviors"]
    assert "SEARCH_ENGINE" in body["forbidden_behaviors"]
    assert "RETRIEVAL_ENGINE" in body["forbidden_behaviors"]
    assert "VECTOR_STORE" in body["forbidden_behaviors"]
    assert "EXECUTION" in body["forbidden_behaviors"]
    assert body["no_indexing_search_ranking_retrieval"] is True
    assert body["no_embeddings_vector_store"] is True
    assert body["no_execution"] is True
    _assert_safe_response(body)


def test_research_artifact_index_boundary_invariants_endpoint() -> None:
    response = client.get("/research-artifact-index-boundary/invariants")
    assert response.status_code == 200
    body = response.json()
    assert body["invariant_result"]["passed"] is True
    assert body["blockers"] == []
    assert body["no_ingestion_storage_upload_download_preview"] is True
    assert body["no_recommendations"] is True
    assert body["no_execution"] is True
    _assert_safe_response(body)


def test_research_artifact_index_boundary_has_no_post_or_execution_routes() -> None:
    def _iter_routes(routes):
        for route in routes:
            yield route
            original_router = getattr(route, "original_router", None)
            if original_router is not None:
                yield from _iter_routes(getattr(original_router, "routes", []))

    boundary_routes = [
        route
        for route in _iter_routes(app.routes)
        if getattr(route, "path", "").startswith("/research-artifact-index-boundary")
    ]
    assert {getattr(route, "path", "") for route in boundary_routes} == {
        "/research-artifact-index-boundary/health",
        "/research-artifact-index-boundary/contracts",
        "/research-artifact-index-boundary/invariants",
    }
    for route in boundary_routes:
        assert getattr(route, "methods", set()) <= {"GET"}
        lowered = getattr(route, "path", "").lower()
        assert "broker" not in lowered
        assert "order" not in lowered
        assert "execution" not in lowered
        assert "trade" not in lowered
