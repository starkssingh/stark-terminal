from __future__ import annotations

import json

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


def test_research_artifact_registry_boundary_health_endpoint_is_safe() -> None:
    response = client.get("/research-artifact-registry-boundary/health")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-research-artifact-registry-boundary"
    assert body["enabled"] is True
    assert body["stage"] == "boundary_hardening"
    assert body["forbidden_behavior_count"] >= 35
    assert body["endpoint_policy_count"] == 4
    assert body["module_policy_count"] == 4
    assert body["invariant_passed"] is True
    assert body["active_ingestion_allowed"] is False
    assert body["persistent_storage_allowed"] is False
    assert body["file_uploads_allowed"] is False
    assert body["file_downloads_allowed"] is False
    assert body["file_previews_allowed"] is False
    assert body["active_ui_allowed"] is False
    assert body["frontend_components_allowed"] is False
    assert body["desktop_components_allowed"] is False
    assert body["paper_parsing_allowed"] is False
    assert body["strategy_generation_allowed"] is False
    assert body["backtesting_allowed"] is False
    assert body["recommendations_allowed"] is False
    assert body["confidence_scoring_allowed"] is False
    assert body["decision_object_generation_allowed"] is False
    assert body["readiness_to_trade_allowed"] is False
    assert body["broker_controls_allowed"] is False
    assert body["execution_allowed"] is False
    assert body["approval_allowed"] is False
    assert body["override_allowed"] is False
    assert body["status"] == "healthy"
    assert "password" not in json.dumps(body).lower()
    assert "secret" not in json.dumps(body).lower()


def test_research_artifact_registry_boundary_contracts_endpoint_returns_policy_metadata() -> None:
    response = client.get("/research-artifact-registry-boundary/contracts")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-research-artifact-registry-boundary"
    assert body["computation_scope"] == "boundary-hardening-only"
    assert body["boundary_hardening_only"] is True
    assert "ACTIVE_INGESTION" in body["forbidden_behaviors"]
    assert "PERSISTENT_STORAGE" in body["forbidden_behaviors"]
    assert "FILE_UPLOAD" in body["forbidden_behaviors"]
    assert "FILE_DOWNLOAD" in body["forbidden_behaviors"]
    assert "FILE_PREVIEW" in body["forbidden_behaviors"]
    assert "ACTIVE_UI" in body["forbidden_behaviors"]
    assert "PAPER_PARSING" in body["forbidden_behaviors"]
    assert "STRATEGY_GENERATION" in body["forbidden_behaviors"]
    assert "BACKTESTING" in body["forbidden_behaviors"]
    assert "RECOMMENDATION_GENERATION" in body["forbidden_behaviors"]
    assert "EXECUTION" in body["forbidden_behaviors"]
    assert "research-artifact-registry-boundary" in body["endpoint_families"]
    assert "research_artifact_registry_boundary" in body["module_families"]
    assert body["active_ingestion_allowed"] is False
    assert body["persistent_storage_allowed"] is False
    assert body["file_uploads_allowed"] is False
    assert body["file_downloads_allowed"] is False
    assert body["file_previews_allowed"] is False
    assert body["active_ui_allowed"] is False
    assert body["paper_parsing_allowed"] is False
    assert body["strategy_generation_allowed"] is False
    assert body["backtesting_allowed"] is False
    assert body["recommendations_allowed"] is False
    assert body["confidence_scoring_allowed"] is False
    assert body["decision_object_generation_allowed"] is False
    assert body["readiness_to_trade_allowed"] is False
    assert body["broker_controls_allowed"] is False
    assert body["execution_allowed"] is False
    assert body["approval_allowed"] is False
    assert body["override_allowed"] is False


def test_research_artifact_registry_boundary_invariants_endpoint_returns_safe_result() -> None:
    response = client.get("/research-artifact-registry-boundary/invariants")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-research-artifact-registry-boundary"
    assert body["boundary_hardening_only"] is True
    assert body["computation_scope"] == "boundary-hardening-only"
    assert body["invariant_result"]["passed"] is True
    assert body["blockers"] == []
    assert body["no_active_ingestion"] is True
    assert body["no_persistent_storage"] is True
    assert body["no_file_uploads"] is True
    assert body["no_file_downloads"] is True
    assert body["no_file_previews"] is True
    assert body["no_active_ui"] is True
    assert body["no_paper_parsing"] is True
    assert body["no_strategy_generation"] is True
    assert body["no_backtesting"] is True
    assert body["no_recommendations"] is True
    assert body["no_confidence_scoring"] is True
    assert body["no_decision_object"] is True
    assert body["no_readiness_to_trade"] is True
    assert body["no_broker_controls"] is True
    assert body["no_approval"] is True
    assert body["no_override"] is True
    assert body["no_execution"] is True
    assert body["active_ingestion_enabled"] is False
    assert body["persistent_storage_enabled"] is False
    assert body["file_upload_enabled"] is False
    assert body["file_download_enabled"] is False
    assert body["file_preview_enabled"] is False
    assert body["paper_parsed"] is False
    assert body["strategy_generated"] is False
    assert body["backtest_generated"] is False
    assert body["recommendation_generated"] is False
    assert body["execution_ready"] is False


def test_research_artifact_registry_boundary_has_no_post_endpoints() -> None:
    for route in app.routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set())
        if path.startswith("/research-artifact-registry-boundary"):
            assert "POST" not in methods

