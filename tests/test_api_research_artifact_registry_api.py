from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)
ROOT = Path(__file__).resolve().parents[1]
ROUTE_PATH = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry_api.py"


def _assert_safe_flags(body: dict) -> None:
    assert body["service"] == "stark-terminal-research-artifact-registry-api"
    assert body["active_ingestion_enabled"] is False
    assert body["persistent_storage_enabled"] is False
    assert body["file_uploads_enabled"] is False
    assert body["file_downloads_enabled"] is False
    assert body["paper_parsing_enabled"] is False
    assert body["strategy_generation_enabled"] is False
    assert body["backtesting_enabled"] is False
    assert body["recommendations_enabled"] is False
    assert body["execution_enabled"] is False


def test_research_artifact_registry_api_health_endpoint() -> None:
    response = client.get("/research-artifact-registry-api/health")

    assert response.status_code == 200
    body = response.json()
    _assert_safe_flags(body)
    assert body["enabled"] is True
    assert body["stage"] == "api_contract_skeleton"
    assert body["read_only"] is True
    assert body["unavailable_by_default"] is True
    assert body["status"] == "healthy"


def test_research_artifact_registry_api_contracts_endpoint() -> None:
    response = client.get("/research-artifact-registry-api/contracts")

    assert response.status_code == 200
    body = response.json()
    _assert_safe_flags(body)
    assert body["api_contract_skeleton_only"] is True
    assert body["read_only"] is True
    assert body["unavailable_by_default"] is True
    assert body["contract"]["read_only"] is True
    assert "ACTIVE_INGESTION" in body["forbidden_actions"]
    assert "FILE_UPLOAD" in body["forbidden_actions"]
    assert "PAPER_PARSING" in body["forbidden_actions"]
    assert "STRATEGY_GENERATION" in body["forbidden_actions"]
    assert "BACKTESTING" in body["forbidden_actions"]
    assert "RECOMMENDATION_GENERATION" in body["forbidden_actions"]
    assert "EXECUTION" in body["forbidden_actions"]


def test_research_artifact_registry_api_unavailable_template_endpoint() -> None:
    response = client.get("/research-artifact-registry-api/unavailable-template")

    assert response.status_code == 200
    body = response.json()
    _assert_safe_flags(body)
    assert body["unavailable_response"]["unavailable"] is True
    assert body["unavailable_response"]["allowed_stage"] == "api_contract_skeleton"
    assert body["no_broker_controls"] is True
    assert body["no_readiness_to_trade"] is True
    assert body["no_active_decision_objects"] is True


def test_research_artifact_registry_api_response_placeholder_endpoint() -> None:
    response = client.get("/research-artifact-registry-api/response-placeholder")

    assert response.status_code == 200
    body = response.json()
    _assert_safe_flags(body)
    assert body["response_placeholder"]["unavailable"] is True
    assert body["response_placeholder"]["placeholder_only"] is True
    assert body["no_parsed_paper_content"] is True
    assert body["no_generated_strategy"] is True
    assert body["no_backtest_result"] is True
    assert body["no_recommendation"] is True
    assert body["no_decision_object"] is True
    assert body["no_execution_fields"] is True


def test_research_artifact_registry_api_reference_placeholder_endpoint() -> None:
    response = client.get("/research-artifact-registry-api/reference-placeholder")

    assert response.status_code == 200
    body = response.json()
    _assert_safe_flags(body)
    assert body["api_reference"]["external_fetch_enabled"] is False
    assert body["api_reference"]["local_file_read_enabled"] is False
    assert body["api_reference"]["source_trusted"] is False
    assert body["metadata_reference"]["validated_artifact_record"] is False
    assert body["provenance_reference"]["descriptive_only"] is True
    assert body["no_external_fetch"] is True
    assert body["no_local_file_read"] is True
    assert body["no_source_trust_claim"] is True


def test_research_artifact_registry_api_no_post_endpoints() -> None:
    route_source = ROUTE_PATH.read_text(encoding="utf-8")

    assert '@router.get("/research-artifact-registry-api/health")' in route_source
    assert "@router.post" not in route_source
    assert "@router.put" not in route_source
    assert "@router.delete" not in route_source


def test_research_artifact_registry_api_responses_do_not_expose_secrets() -> None:
    responses = [
        client.get("/research-artifact-registry-api/health").json(),
        client.get("/research-artifact-registry-api/contracts").json(),
        client.get("/research-artifact-registry-api/unavailable-template").json(),
        client.get("/research-artifact-registry-api/response-placeholder").json(),
        client.get("/research-artifact-registry-api/reference-placeholder").json(),
    ]
    serialized = " ".join(str(response).lower() for response in responses)

    assert "secret" not in serialized
    assert "password" not in serialized
    assert "credential" not in serialized
    assert "api_key" not in serialized
