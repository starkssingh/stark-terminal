from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


def test_decision_display_health_endpoint_is_safe() -> None:
    response = client.get("/decision-display/health")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-decision-display"
    assert body["enabled"] is True
    assert body["stage"] == "display_contract_skeleton"
    assert body["recommendations_allowed"] is False
    assert body["action_generation_allowed"] is False
    assert body["confidence_scoring_allowed"] is False
    assert body["decision_object_generation_allowed"] is False
    assert body["readiness_to_trade_allowed"] is False
    assert body["execution_allowed"] is False
    assert body["approval_allowed"] is False
    assert body["override_allowed"] is False
    assert body["returns_unavailable_by_default"] is True
    assert body["default_section_count"] > 0
    assert body["default_card_count"] > 0
    assert "password" not in str(body).lower()
    assert "secret" not in str(body).lower()


def test_decision_display_contracts_endpoint_is_skeleton_only() -> None:
    response = client.get("/decision-display/contracts")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-decision-display"
    assert body["computation_scope"] == "display-contract-skeleton-only"
    assert body["recommendations_allowed_now"] is False
    assert body["action_generation_allowed_now"] is False
    assert body["confidence_scoring_allowed_now"] is False
    assert body["decision_object_generation_allowed_now"] is False
    assert body["readiness_to_trade_allowed_now"] is False
    assert body["execution_allowed_now"] is False
    assert body["approval_allowed_now"] is False
    assert body["override_allowed_now"] is False
    assert body["returns_unavailable_by_default"] is True
    assert "HEADER" in body["supported_section_kinds"]
    assert "UNAVAILABLE" in body["supported_card_kinds"]
    assert "NOT_A_RECOMMENDATION" in body["supported_badge_kinds"]
    assert "readiness-to-trade" in body["forbidden_outputs"]
    assert "DecisionObject_generation" in body["forbidden_outputs"]


def test_decision_display_templates_return_no_generated_outputs() -> None:
    unavailable = client.get("/decision-display/unavailable-template").json()
    assert unavailable["display_contract_skeleton_only"] is True
    assert unavailable["unavailable_response"]["unavailable"] is True
    assert unavailable["unavailable_response"]["display_contract_only"] is True
    assert unavailable["unavailable_response"]["recommendations_allowed"] is False
    assert unavailable["unavailable_response"]["readiness_to_trade_allowed"] is False
    assert unavailable["no_recommendations"] is True
    assert unavailable["no_decision_object"] is True
    assert unavailable["no_readiness_to_trade"] is True
    assert unavailable["no_approval"] is True
    assert unavailable["no_execution"] is True
    assert unavailable["no_active_ui"] is True

    layout = client.get("/decision-display/placeholder-layout").json()
    assert layout["planning_only"] is True
    assert layout["display_contract_skeleton_only"] is True
    assert layout["sections"]
    assert layout["cards"]
    assert layout["badges"]
    assert layout["no_generated_outputs"] is True
    assert layout["recommendation_generated"] is False
    assert layout["action_generated"] is False
    assert layout["confidence_generated"] is False
    assert layout["decision_object_generated"] is False
    assert layout["readiness_to_trade_generated"] is False
    assert layout["execution_ready"] is False
    assert layout["approval_granted"] is False
    assert layout["override_granted"] is False
    assert layout["active_ui"] is False
    assert "password" not in str(layout).lower()
    assert "secret" not in str(layout).lower()

