from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


def test_retail_trader_experience_api_health_endpoint_is_safe() -> None:
    response = client.get("/retail-trader-experience-api/health")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-retail-trader-experience-api"
    assert body["enabled"] is True
    assert body["stage"] == "api_contract_skeleton"
    assert body["active_ui_allowed"] is False
    assert body["frontend_components_allowed"] is False
    assert body["desktop_components_allowed"] is False
    assert body["recommendations_allowed"] is False
    assert body["action_generation_allowed"] is False
    assert body["confidence_scoring_allowed"] is False
    assert body["decision_object_generation_allowed"] is False
    assert body["readiness_to_trade_allowed"] is False
    assert body["broker_controls_allowed"] is False
    assert body["execution_allowed"] is False
    assert body["approval_allowed"] is False
    assert body["override_allowed"] is False
    assert body["suitability_profiling_allowed"] is False
    assert body["returns_unavailable_by_default"] is True
    assert body["status"] == "healthy"
    assert "password" not in str(body).lower()
    assert "secret" not in str(body).lower()


def test_retail_trader_experience_api_contracts_endpoint_returns_metadata() -> None:
    response = client.get("/retail-trader-experience-api/contracts")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-retail-trader-experience-api"
    assert body["computation_scope"] == "api-contract-skeleton-only"
    assert body["active_ui_allowed_now"] is False
    assert body["frontend_components_allowed_now"] is False
    assert body["desktop_components_allowed_now"] is False
    assert body["recommendations_allowed_now"] is False
    assert body["action_generation_allowed_now"] is False
    assert body["confidence_scoring_allowed_now"] is False
    assert body["decision_object_generation_allowed_now"] is False
    assert body["readiness_to_trade_allowed_now"] is False
    assert body["broker_controls_allowed_now"] is False
    assert body["execution_allowed_now"] is False
    assert body["approval_allowed_now"] is False
    assert body["override_allowed_now"] is False
    assert body["suitability_profiling_allowed_now"] is False
    assert body["returns_unavailable_by_default"] is True
    assert "EXPERIENCE_OVERVIEW_REQUEST" in body["request_kinds"]
    assert "API_CONTRACT_SKELETON_ONLY" in body["unavailable_reasons"]
    assert "execution_apis" in body["forbidden_outputs"]
    assert "suitability_profiling" in body["forbidden_outputs"]


def test_retail_trader_experience_api_unavailable_template_returns_no_generated_outputs() -> None:
    response = client.get("/retail-trader-experience-api/unavailable-template")
    assert response.status_code == 200
    body = response.json()

    assert body["api_contract_skeleton_only"] is True
    unavailable = body["unavailable_response"]
    assert unavailable["unavailable"] is True
    assert unavailable["api_contract_skeleton_only"] is True
    assert unavailable["active_ui_allowed"] is False
    assert unavailable["frontend_components_allowed"] is False
    assert unavailable["desktop_components_allowed"] is False
    assert unavailable["recommendations_allowed"] is False
    assert unavailable["action_generation_allowed"] is False
    assert unavailable["confidence_scoring_allowed"] is False
    assert unavailable["decision_object_generation_allowed"] is False
    assert unavailable["readiness_to_trade_allowed"] is False
    assert unavailable["broker_controls_allowed"] is False
    assert unavailable["execution_allowed"] is False
    assert unavailable["approval_granted"] is False
    assert unavailable["override_granted"] is False
    assert unavailable["suitability_profiling_allowed"] is False
    assert body["no_active_ui"] is True
    assert body["no_suitability_profiling"] is True
    assert body["no_execution"] is True


def test_retail_trader_experience_api_response_placeholder_returns_references_only() -> None:
    response = client.get("/retail-trader-experience-api/response-placeholder")
    assert response.status_code == 200
    body = response.json()

    assert body["api_contract_skeleton_only"] is True
    assert body["no_generated_outputs"] is True
    assert body["no_suitability_profiling"] is True
    assert body["persona_reference"]["active_profile"] is False
    assert body["persona_reference"]["suitability_profile"] is False
    assert body["journey_reference"]["trading_advice_journey"] is False
    assert body["dashboard_reference"]["active_dashboard"] is False
    assert body["dashboard_reference"]["active_ui"] is False
    assert body["decision_reference"]["active_decision_object"] is False
    assert body["decision_reference"]["recommendation_available"] is False
    assert body["decision_reference"]["confidence_available"] is False
    assert body["safety_reference"]["safety_passed"] is False
    assert body["safety_reference"]["approval_granted"] is False
    assert body["safety_reference"]["override_granted"] is False
    assert body["safety_reference"]["suitability_profiling_allowed"] is False
    for key in [
        "active_ui_generated",
        "frontend_component_generated",
        "desktop_component_generated",
        "recommendation_generated",
        "action_generated",
        "confidence_generated",
        "decision_object_generated",
        "readiness_to_trade_generated",
        "broker_control_generated",
        "suitability_profile_generated",
        "execution_ready",
        "approval_granted",
        "override_granted",
    ]:
        assert body[key] is False


def test_retail_trader_experience_api_has_no_post_endpoints() -> None:
    for route in app.routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set())
        if path.startswith("/retail-trader-experience-api"):
            assert "POST" not in methods
            assert "PUT" not in methods
            assert "PATCH" not in methods
            assert "DELETE" not in methods
