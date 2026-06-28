from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)
ROOT = Path(__file__).resolve().parents[1]
ROUTE_PATH = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry.py"


def test_research_artifact_registry_health_endpoint() -> None:
    response = client.get("/research-artifact-registry/health")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-research-artifact-registry"
    assert body["enabled"] is True
    assert body["stage"] == "planning"
    assert body["planning_only"] is True
    assert body["active_ingestion_enabled"] is False
    assert body["persistent_storage_enabled"] is False
    assert body["file_uploads_enabled"] is False
    assert body["file_downloads_enabled"] is False
    assert body["paper_parsing_enabled"] is False
    assert body["strategy_generation_enabled"] is False
    assert body["backtesting_enabled"] is False
    assert body["recommendations_enabled"] is False
    assert body["execution_enabled"] is False
    assert body["status"] == "healthy"


def test_research_artifact_registry_contracts_endpoint() -> None:
    response = client.get("/research-artifact-registry/contracts")

    assert response.status_code == 200
    body = response.json()
    assert body["computation_scope"] == "planning-and-guardrails-only"
    assert body["planning_only"] is True
    assert body["unavailable_by_default"] is True
    assert "PAPER_REFERENCE" in body["artifact_kinds"]
    assert "BACKTEST_REFERENCE_PLACEHOLDER" in body["artifact_kinds"]
    assert "STRATEGY_REFERENCE_PLACEHOLDER" in body["artifact_kinds"]
    assert "ACTIVE_INGESTION" in body["forbidden_interactions"]
    assert "PAPER_PARSING" in body["forbidden_interactions"]
    assert "STRATEGY_GENERATION" in body["forbidden_interactions"]
    assert "BACKTESTING" in body["forbidden_interactions"]
    assert "RECOMMENDATION_GENERATION" in body["forbidden_interactions"]
    assert "EXECUTION" in body["forbidden_interactions"]


def test_research_artifact_registry_placeholder_endpoint() -> None:
    response = client.get("/research-artifact-registry/placeholder-artifact")

    assert response.status_code == 200
    body = response.json()
    assert body["planning_only"] is True
    assert body["metadata_placeholders"]
    assert body["reference_placeholders"]
    assert body["provenance_placeholders"]
    assert body["lifecycle_placeholders"]
    assert body["no_file_contents"] is True
    assert body["no_parsed_paper_text"] is True
    assert body["no_strategy_logic"] is True
    assert body["no_backtest_metrics"] is True
    assert body["no_recommendation_text"] is True
    assert body["execution_enabled"] is False


def test_research_artifact_registry_readiness_endpoint() -> None:
    response = client.get("/research-artifact-registry/readiness-template")

    assert response.status_code == 200
    body = response.json()
    readiness = body["readiness_report"]
    assert readiness["registry_planning_ready"] is True
    assert readiness["active_ingestion_enabled"] is False
    assert readiness["persistent_storage_enabled"] is False
    assert readiness["paper_parsing_enabled"] is False
    assert readiness["strategy_generation_enabled"] is False
    assert readiness["backtesting_enabled"] is False
    assert readiness["recommendations_enabled"] is False
    assert readiness["execution_enabled"] is False
    assert readiness["next_allowed_phase"] == "api_contract_skeleton"


def test_research_artifact_registry_unavailable_endpoint() -> None:
    response = client.get("/research-artifact-registry/unavailable-template")

    assert response.status_code == 200
    body = response.json()
    unavailable = body["unavailable_response"]
    assert unavailable["unavailable"] is True
    assert unavailable["planning_only"] is True
    assert unavailable["active_ingestion_enabled"] is False
    assert unavailable["persistent_storage_enabled"] is False
    assert unavailable["paper_parsing_enabled"] is False
    assert unavailable["strategy_generation_enabled"] is False
    assert unavailable["backtesting_enabled"] is False
    assert unavailable["recommendations_enabled"] is False
    assert unavailable["execution_enabled"] is False


def test_research_artifact_registry_no_post_endpoints() -> None:
    route_source = ROUTE_PATH.read_text(encoding="utf-8")

    assert '@router.get("/research-artifact-registry/health")' in route_source
    assert "@router.post" not in route_source
    assert "@router.put" not in route_source
    assert "@router.delete" not in route_source


def test_research_artifact_registry_responses_do_not_expose_secrets() -> None:
    responses = [
        client.get("/research-artifact-registry/health").json(),
        client.get("/research-artifact-registry/contracts").json(),
        client.get("/research-artifact-registry/placeholder-artifact").json(),
        client.get("/research-artifact-registry/readiness-template").json(),
        client.get("/research-artifact-registry/unavailable-template").json(),
    ]
    serialized = " ".join(str(response).lower() for response in responses)

    assert "secret" not in serialized
    assert "password" not in serialized
    assert "credential" not in serialized
    assert "api_key" not in serialized
