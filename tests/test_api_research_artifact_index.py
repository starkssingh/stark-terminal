from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)
ROOT = Path(__file__).resolve().parents[1]
ROUTE_PATH = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index.py"


def _assert_safe_flags(body: dict[str, object]) -> None:
    for flag in [
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
        assert body[flag] is False


def test_research_artifact_index_health_endpoint() -> None:
    response = client.get("/research-artifact-index/health")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-research-artifact-index"
    assert body["enabled"] is True
    assert body["stage"] == "planning_and_guardrails"
    assert body["planning_only"] is True
    _assert_safe_flags(body)
    assert body["status"] == "healthy"


def test_research_artifact_index_contracts_endpoint() -> None:
    response = client.get("/research-artifact-index/contracts")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-research-artifact-index"
    assert body["computation_scope"] == "planning-and-guardrails-only"
    assert body["planning_only"] is True
    assert body["unavailable_by_default"] is True
    assert "METADATA_INDEX_PLACEHOLDER" in body["index_kinds"]
    assert "ARTIFACT_ID" in body["key_kinds"]
    assert "PAPER_REFERENCE" in body["tag_kinds"]
    assert "INDEXING_ENGINE" in body["forbidden_interactions"]
    assert "SEARCH_ENGINE" in body["forbidden_interactions"]
    assert "VECTOR_STORE" in body["forbidden_interactions"]
    assert body["next_allowed_phase"] == "api_contract_skeleton"
    _assert_safe_flags(body)


def test_research_artifact_index_placeholder_readiness_and_unavailable_endpoints() -> None:
    for endpoint in [
        "/research-artifact-index/placeholder-index",
        "/research-artifact-index/readiness-template",
        "/research-artifact-index/unavailable-template",
    ]:
        response = client.get(endpoint)
        assert response.status_code == 200
        body = response.json()
        assert body["service"] == "stark-terminal-research-artifact-index"
        assert body["planning_only"] is True
        _assert_safe_flags(body)


def test_research_artifact_index_no_post_or_dangerous_routes() -> None:
    route_source = ROUTE_PATH.read_text(encoding="utf-8")

    assert '@router.get("/research-artifact-index/health")' in route_source
    assert "@router.post" not in route_source
    assert "@router.put" not in route_source
    assert "@router.delete" not in route_source
    for forbidden in ["upload", "download", "preview", "search", "rank", "embed", "execute"]:
        assert f'@router.get("/research-artifact-index/{forbidden}' not in route_source


def test_research_artifact_index_responses_do_not_expose_secrets_or_active_behavior() -> None:
    responses = [
        client.get("/research-artifact-index/health").json(),
        client.get("/research-artifact-index/contracts").json(),
        client.get("/research-artifact-index/placeholder-index").json(),
        client.get("/research-artifact-index/readiness-template").json(),
        client.get("/research-artifact-index/unavailable-template").json(),
    ]
    serialized = " ".join(str(response).lower() for response in responses)

    for forbidden in ["password", "credential", "api_key", "ready_to_trade"]:
        assert forbidden not in serialized
