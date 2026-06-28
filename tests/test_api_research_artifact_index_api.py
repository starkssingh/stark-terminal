from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)
ROOT = Path(__file__).resolve().parents[1]
ROUTE_PATH = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index_api.py"


def _assert_safe_flags(body: dict[str, object]) -> None:
    assert body["service"] == "stark-terminal-research-artifact-index-api"
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


def test_research_artifact_index_api_health_endpoint() -> None:
    response = client.get("/research-artifact-index-api/health")

    assert response.status_code == 200
    body = response.json()
    _assert_safe_flags(body)
    assert body["enabled"] is True
    assert body["stage"] == "api_contract_skeleton"
    assert body["read_only"] is True
    assert body["unavailable_by_default"] is True
    assert body["status"] == "healthy"


def test_research_artifact_index_api_contracts_endpoint() -> None:
    response = client.get("/research-artifact-index-api/contracts")

    assert response.status_code == 200
    body = response.json()
    _assert_safe_flags(body)
    assert body["api_contract_skeleton_only"] is True
    assert body["read_only"] is True
    assert body["unavailable_by_default"] is True
    assert body["contract"]["read_only"] is True
    for action in ["INDEXING_ENGINE", "SEARCH_ENGINE", "RANKING_ENGINE", "VECTOR_STORE", "EXECUTION"]:
        assert action in body["forbidden_actions"]


def test_research_artifact_index_api_unavailable_template_endpoint() -> None:
    response = client.get("/research-artifact-index-api/unavailable-template")

    assert response.status_code == 200
    body = response.json()
    _assert_safe_flags(body)
    assert body["unavailable_response"]["unavailable"] is True
    assert body["unavailable_response"]["allowed_stage"] == "api_contract_skeleton"
    assert body["no_broker_controls"] is True
    assert body["no_readiness_to_trade"] is True
    assert body["no_active_decision_objects"] is True


def test_research_artifact_index_api_response_placeholder_endpoint() -> None:
    response = client.get("/research-artifact-index-api/response-placeholder")

    assert response.status_code == 200
    body = response.json()
    _assert_safe_flags(body)
    assert body["response_placeholder"]["unavailable"] is True
    assert body["response_placeholder"]["placeholder_only"] is True
    assert body["no_indexed_artifact_records"] is True
    assert body["no_search_results"] is True
    assert body["no_ranking_results"] is True
    assert body["no_retrieval_results"] is True
    assert body["no_embeddings"] is True
    assert body["no_vector_ids"] is True
    assert body["no_generated_strategy"] is True
    assert body["no_backtest_result"] is True
    assert body["no_recommendation"] is True
    assert body["no_decision_object"] is True
    assert body["no_execution_fields"] is True


def test_research_artifact_index_api_reference_placeholder_endpoint() -> None:
    response = client.get("/research-artifact-index-api/reference-placeholder")

    assert response.status_code == 200
    body = response.json()
    _assert_safe_flags(body)
    assert body["api_reference"]["external_fetch_enabled"] is False
    assert body["api_reference"]["local_file_read_enabled"] is False
    assert body["api_reference"]["registry_lookup_enabled"] is False
    assert body["api_reference"]["index_lookup_enabled"] is False
    assert body["api_reference"]["source_trusted"] is False
    assert body["metadata_reference"]["validated_index_record"] is False
    assert body["provenance_reference"]["descriptive_only"] is True
    assert body["no_external_fetch"] is True
    assert body["no_local_file_read"] is True
    assert body["no_source_trust_claim"] is True


def test_research_artifact_index_api_no_post_endpoints() -> None:
    route_source = ROUTE_PATH.read_text(encoding="utf-8")

    assert '@router.get("/research-artifact-index-api/health")' in route_source
    assert "@router.post" not in route_source
    assert "@router.put" not in route_source
    assert "@router.delete" not in route_source


def test_research_artifact_index_api_responses_do_not_expose_secrets_or_active_behavior() -> None:
    responses = [
        client.get("/research-artifact-index-api/health").json(),
        client.get("/research-artifact-index-api/contracts").json(),
        client.get("/research-artifact-index-api/unavailable-template").json(),
        client.get("/research-artifact-index-api/response-placeholder").json(),
        client.get("/research-artifact-index-api/reference-placeholder").json(),
    ]
    serialized = " ".join(str(response).lower() for response in responses)

    for forbidden in ["password", "credential", "api_key", "ready_to_trade"]:
        assert forbidden not in serialized
