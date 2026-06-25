from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


def _assert_no_secret_keys(payload: object) -> None:
    text = str(payload).lower()
    assert "password" not in text
    assert "api_key" not in text
    assert "token" not in text
    assert "secret" not in text


def test_retail_trader_experience_display_health_endpoint_is_safe() -> None:
    response = client.get("/retail-trader-experience-display/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["service"] == "stark-terminal-retail-trader-experience-display"
    assert payload["status"] == "healthy"
    assert payload["stage"] == "display_contract_skeleton"
    assert payload["active_ui_allowed"] is False
    assert payload["frontend_components_allowed"] is False
    assert payload["desktop_components_allowed"] is False
    assert payload["recommendations_allowed"] is False
    assert payload["action_generation_allowed"] is False
    assert payload["confidence_scoring_allowed"] is False
    assert payload["decision_object_generation_allowed"] is False
    assert payload["readiness_to_trade_allowed"] is False
    assert payload["broker_controls_allowed"] is False
    assert payload["execution_allowed"] is False
    assert payload["approval_allowed"] is False
    assert payload["override_allowed"] is False
    assert payload["suitability_profiling_allowed"] is False
    assert payload["returns_unavailable_by_default"] is True
    assert payload["persona_count"] > 0
    assert payload["journey_count"] > 0
    assert payload["section_count"] > 0
    assert payload["widget_count"] > 0
    assert payload["badge_count"] > 0
    _assert_no_secret_keys(payload)


def test_retail_trader_experience_display_contracts_endpoint_is_safe() -> None:
    response = client.get("/retail-trader-experience-display/contracts")

    assert response.status_code == 200
    payload = response.json()
    assert payload["computation_scope"] == "display-contract-skeleton-only"
    assert payload["active_ui_allowed_now"] is False
    assert payload["frontend_components_allowed_now"] is False
    assert payload["desktop_components_allowed_now"] is False
    assert payload["recommendations_allowed_now"] is False
    assert payload["action_generation_allowed_now"] is False
    assert payload["confidence_scoring_allowed_now"] is False
    assert payload["decision_object_generation_allowed_now"] is False
    assert payload["readiness_to_trade_allowed_now"] is False
    assert payload["broker_controls_allowed_now"] is False
    assert payload["execution_allowed_now"] is False
    assert payload["approval_allowed_now"] is False
    assert payload["override_allowed_now"] is False
    assert payload["suitability_profiling_allowed_now"] is False
    assert payload["returns_unavailable_by_default"] is True
    assert payload["forbidden_outputs"]
    assert payload["persona_kinds"]
    assert payload["journey_kinds"]
    assert payload["section_kinds"]
    assert payload["widget_kinds"]
    assert payload["badge_kinds"]
    _assert_no_secret_keys(payload)


def test_retail_trader_experience_display_unavailable_template_endpoint_is_safe() -> None:
    response = client.get("/retail-trader-experience-display/unavailable-template")

    assert response.status_code == 200
    payload = response.json()
    assert payload["display_contract_skeleton_only"] is True
    assert payload["unavailable_response"]["unavailable"] is True
    assert payload["unavailable_response"]["display_contract_only"] is True
    assert payload["no_active_ui"] is True
    assert payload["no_frontend_components"] is True
    assert payload["no_desktop_components"] is True
    assert payload["no_recommendations"] is True
    assert payload["no_action_generation"] is True
    assert payload["no_confidence_scoring"] is True
    assert payload["no_decision_object"] is True
    assert payload["no_readiness_to_trade"] is True
    assert payload["no_broker_controls"] is True
    assert payload["no_suitability_profiling"] is True
    assert payload["no_execution"] is True
    assert payload["no_approval"] is True
    assert payload["no_override"] is True
    _assert_no_secret_keys(payload)


def test_retail_trader_experience_display_placeholder_experience_endpoint_is_safe() -> None:
    response = client.get("/retail-trader-experience-display/placeholder-experience")

    assert response.status_code == 200
    payload = response.json()
    assert payload["display_contract_skeleton_only"] is True
    assert payload["persona_placeholders"]
    assert payload["journey_placeholders"]
    assert payload["visual_sections"]
    assert payload["widgets"]
    assert payload["badges"]
    assert payload["no_active_ui"] is True
    assert payload["no_generated_outputs"] is True
    assert payload["no_broker_controls"] is True
    assert payload["no_suitability_profiling"] is True
    assert payload["no_execution"] is True
    assert payload["active_ui_generated"] is False
    assert payload["frontend_component_generated"] is False
    assert payload["desktop_component_generated"] is False
    assert payload["recommendation_generated"] is False
    assert payload["action_generated"] is False
    assert payload["confidence_generated"] is False
    assert payload["decision_object_generated"] is False
    assert payload["readiness_to_trade_generated"] is False
    assert payload["broker_control_generated"] is False
    assert payload["suitability_profile_generated"] is False
    assert payload["execution_ready"] is False
    assert payload["approval_granted"] is False
    assert payload["override_granted"] is False
    _assert_no_secret_keys(payload)


def test_retail_trader_experience_display_adds_no_post_endpoints() -> None:
    for path in [
        "/retail-trader-experience-display/health",
        "/retail-trader-experience-display/contracts",
        "/retail-trader-experience-display/unavailable-template",
        "/retail-trader-experience-display/placeholder-experience",
    ]:
        assert client.get(path).status_code == 200
        assert client.post(path).status_code in {404, 405}
