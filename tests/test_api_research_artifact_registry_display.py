from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)
ROOT = Path(__file__).resolve().parents[1]
ROUTE_PATH = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry_display.py"


def _assert_safe_flags(body: dict) -> None:
    assert body["service"] == "stark-terminal-research-artifact-registry-display"
    assert body["active_ui_enabled"] is False
    assert body["frontend_components_enabled"] is False
    assert body["desktop_components_enabled"] is False
    assert body["active_ingestion_enabled"] is False
    assert body["persistent_storage_enabled"] is False
    assert body["file_uploads_enabled"] is False
    assert body["file_downloads_enabled"] is False
    assert body["paper_parsing_enabled"] is False
    assert body["strategy_generation_enabled"] is False
    assert body["backtesting_enabled"] is False
    assert body["recommendations_enabled"] is False
    assert body["execution_enabled"] is False


def test_research_artifact_registry_display_health_endpoint() -> None:
    response = client.get("/research-artifact-registry-display/health")

    assert response.status_code == 200
    body = response.json()
    _assert_safe_flags(body)
    assert body["enabled"] is True
    assert body["stage"] == "display_contract_skeleton"
    assert body["read_only"] is True
    assert body["unavailable_by_default"] is True
    assert body["status"] == "healthy"


def test_research_artifact_registry_display_contracts_endpoint() -> None:
    response = client.get("/research-artifact-registry-display/contracts")

    assert response.status_code == 200
    body = response.json()
    _assert_safe_flags(body)
    assert body["display_contract_skeleton_only"] is True
    assert body["read_only"] is True
    assert body["unavailable_by_default"] is True
    assert body["contract"]["read_only"] is True
    assert "ACTIVE_UI" in body["forbidden_actions"]
    assert "FRONTEND_COMPONENT" in body["forbidden_actions"]
    assert "DESKTOP_COMPONENT" in body["forbidden_actions"]
    assert "FILE_PREVIEW" in body["forbidden_actions"]
    assert "PAPER_PARSING" in body["forbidden_actions"]
    assert "STRATEGY_GENERATION" in body["forbidden_actions"]
    assert "BACKTESTING" in body["forbidden_actions"]
    assert "RECOMMENDATION_GENERATION" in body["forbidden_actions"]
    assert "EXECUTION" in body["forbidden_actions"]


def test_research_artifact_registry_display_unavailable_template_endpoint() -> None:
    response = client.get("/research-artifact-registry-display/unavailable-template")

    assert response.status_code == 200
    body = response.json()
    _assert_safe_flags(body)
    assert body["unavailable_response"]["unavailable"] is True
    assert body["unavailable_response"]["allowed_stage"] == "display_contract_skeleton"
    assert body["no_broker_controls"] is True
    assert body["no_readiness_to_trade"] is True
    assert body["no_active_decision_objects"] is True


def test_research_artifact_registry_display_placeholder_card_endpoint() -> None:
    response = client.get("/research-artifact-registry-display/placeholder-card")

    assert response.status_code == 200
    body = response.json()
    _assert_safe_flags(body)
    assert body["card_placeholders"]["artifact_card"]["active_ui"] is False
    assert body["card_placeholders"]["artifact_card"]["file_content_preview"] is False
    assert body["card_placeholders"]["artifact_card"]["parsed_paper_content"] is False
    assert body["card_placeholders"]["artifact_card"]["generated_strategy_content"] is False
    assert body["card_placeholders"]["artifact_card"]["backtest_metrics_present"] is False
    assert body["no_active_ui"] is True
    assert body["no_file_preview"] is True
    assert body["no_generated_strategy"] is True
    assert body["no_execution_controls"] is True


def test_research_artifact_registry_display_placeholder_provenance_endpoint() -> None:
    response = client.get("/research-artifact-registry-display/placeholder-provenance")

    assert response.status_code == 200
    body = response.json()
    _assert_safe_flags(body)
    assert body["provenance_display"]["descriptive_only"] is True
    assert body["provenance_display"]["source_validation_claim"] is False
    assert body["display_reference"]["external_fetch_enabled"] is False
    assert body["source_display"]["local_file_read_enabled"] is False
    assert body["no_external_fetch"] is True
    assert body["no_source_trust_claim"] is True


def test_research_artifact_registry_display_placeholder_lifecycle_endpoint() -> None:
    response = client.get("/research-artifact-registry-display/placeholder-lifecycle")

    assert response.status_code == 200
    body = response.json()
    _assert_safe_flags(body)
    assert body["lifecycle_display"]["validated_strategy"] is False
    assert body["lifecycle_display"]["recommended_strategy"] is False
    assert body["lifecycle_display"]["readiness_to_trade"] is False
    assert body["lifecycle_badge"]["execution_ready"] is False
    assert body["no_recommendation"] is True
    assert body["no_readiness_to_trade"] is True
    assert body["no_execution"] is True


def test_research_artifact_registry_display_no_post_endpoints() -> None:
    route_source = ROUTE_PATH.read_text(encoding="utf-8")

    assert '@router.get("/research-artifact-registry-display/health")' in route_source
    assert "@router.post" not in route_source
    assert "@router.put" not in route_source
    assert "@router.delete" not in route_source


def test_research_artifact_registry_display_responses_do_not_expose_secrets() -> None:
    responses = [
        client.get("/research-artifact-registry-display/health").json(),
        client.get("/research-artifact-registry-display/contracts").json(),
        client.get("/research-artifact-registry-display/unavailable-template").json(),
        client.get("/research-artifact-registry-display/placeholder-card").json(),
        client.get("/research-artifact-registry-display/placeholder-provenance").json(),
        client.get("/research-artifact-registry-display/placeholder-lifecycle").json(),
    ]
    serialized = " ".join(str(response).lower() for response in responses)

    assert "secret" not in serialized
    assert "password" not in serialized
    assert "credential" not in serialized
    assert "api_key" not in serialized
