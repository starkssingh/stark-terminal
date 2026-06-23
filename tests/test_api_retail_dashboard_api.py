from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


def test_retail_dashboard_api_health_endpoint_is_safe() -> None:
    response = client.get("/retail-dashboard-api/health")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-retail-dashboard-api"
    assert body["enabled"] is True
    assert body["stage"] == "api_contract_skeleton"
    assert body["active_ui_allowed"] is False
    assert body["recommendations_allowed"] is False
    assert body["action_generation_allowed"] is False
    assert body["confidence_scoring_allowed"] is False
    assert body["decision_object_generation_allowed"] is False
    assert body["readiness_to_trade_allowed"] is False
    assert body["broker_controls_allowed"] is False
    assert body["execution_allowed"] is False
    assert body["approval_allowed"] is False
    assert body["override_allowed"] is False
    assert body["returns_unavailable_by_default"] is True
    assert body["status"] == "healthy"
    assert "password" not in str(body).lower()
    assert "secret" not in str(body).lower()


def test_retail_dashboard_api_contracts_endpoint_returns_metadata() -> None:
    response = client.get("/retail-dashboard-api/contracts")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-retail-dashboard-api"
    assert body["computation_scope"] == "api-contract-skeleton-only"
    assert body["active_ui_allowed_now"] is False
    assert body["recommendations_allowed_now"] is False
    assert body["action_generation_allowed_now"] is False
    assert body["confidence_scoring_allowed_now"] is False
    assert body["decision_object_generation_allowed_now"] is False
    assert body["readiness_to_trade_allowed_now"] is False
    assert body["broker_controls_allowed_now"] is False
    assert body["execution_allowed_now"] is False
    assert body["approval_allowed_now"] is False
    assert body["override_allowed_now"] is False
    assert body["returns_unavailable_by_default"] is True
    assert "DASHBOARD_OVERVIEW_REQUEST" in body["request_kinds"]
    assert "API_CONTRACT_SKELETON_ONLY" in body["unavailable_reasons"]
    assert "execution_apis" in body["forbidden_outputs"]


def test_retail_dashboard_api_unavailable_template_returns_no_generated_outputs() -> None:
    response = client.get("/retail-dashboard-api/unavailable-template")
    assert response.status_code == 200
    body = response.json()

    assert body["api_contract_skeleton_only"] is True
    unavailable = body["unavailable_response"]
    assert unavailable["unavailable"] is True
    assert unavailable["api_contract_skeleton_only"] is True
    assert unavailable["active_ui_allowed"] is False
    assert unavailable["recommendations_allowed"] is False
    assert unavailable["action_generation_allowed"] is False
    assert unavailable["confidence_scoring_allowed"] is False
    assert unavailable["decision_object_generation_allowed"] is False
    assert unavailable["readiness_to_trade_allowed"] is False
    assert unavailable["broker_controls_allowed"] is False
    assert unavailable["execution_allowed"] is False
    assert unavailable["approval_granted"] is False
    assert unavailable["override_granted"] is False
    assert body["no_active_ui"] is True
    assert body["no_recommendations"] is True
    assert body["no_broker_controls"] is True
    assert body["no_execution"] is True


def test_retail_dashboard_api_response_placeholder_returns_references_only() -> None:
    response = client.get("/retail-dashboard-api/response-placeholder")
    assert response.status_code == 200
    body = response.json()

    assert body["api_contract_skeleton_only"] is True
    assert body["no_generated_outputs"] is True
    assert body["data_reference"]["real_market_data"] is False
    assert body["data_reference"]["live_data"] is False
    assert body["data_reference"]["display_ready"] is False
    assert body["decision_reference"]["active_decision_object"] is False
    assert body["decision_reference"]["recommendation_available"] is False
    assert body["decision_reference"]["action_available"] is False
    assert body["decision_reference"]["confidence_available"] is False
    assert body["decision_reference"]["readiness_to_trade_available"] is False
    assert body["safety_reference"]["safety_passed"] is False
    assert body["safety_reference"]["approval_granted"] is False
    assert body["safety_reference"]["override_granted"] is False
    assert body["safety_reference"]["execution_allowed"] is False
    assert body["safety_reference"]["broker_controls_allowed"] is False
    for key in [
        "active_ui_generated",
        "recommendation_generated",
        "action_generated",
        "confidence_generated",
        "decision_object_generated",
        "readiness_to_trade_generated",
        "broker_control_generated",
        "execution_ready",
        "approval_granted",
        "override_granted",
    ]:
        assert body[key] is False


def test_retail_dashboard_api_has_no_post_endpoints() -> None:
    paths = app.openapi()["paths"]
    for path, operations in paths.items():
        if path.startswith("/retail-dashboard-api"):
            assert "post" not in operations
            assert "put" not in operations
            assert "patch" not in operations
            assert "delete" not in operations
