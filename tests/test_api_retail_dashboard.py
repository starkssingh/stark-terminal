from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


def test_retail_dashboard_health_endpoint_is_safe() -> None:
    response = client.get("/retail-dashboard/health")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-retail-dashboard"
    assert body["enabled"] is True
    assert body["stage"] == "planning_and_guardrails"
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
    assert body["default_section_count"] > 0
    assert body["default_card_count"] > 0
    assert body["forbidden_interaction_count"] > 0
    assert body["status"] == "healthy"
    assert "password" not in str(body).lower()
    assert "secret" not in str(body).lower()


def test_retail_dashboard_contracts_endpoint_returns_planning_metadata() -> None:
    response = client.get("/retail-dashboard/contracts")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-retail-dashboard"
    assert body["computation_scope"] == "planning-and-guardrails-only"
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
    assert "RECOMMENDATION_CARD" in body["forbidden_interactions"]
    assert "BROKER_CONTROL" in body["forbidden_interactions"]
    assert body["planned_sections"]
    assert body["planned_cards"]


def test_retail_dashboard_placeholder_layout_returns_no_generated_outputs() -> None:
    response = client.get("/retail-dashboard/placeholder-layout")
    assert response.status_code == 200
    body = response.json()

    assert body["planning_only"] is True
    assert body["active_ui_allowed_now"] is False
    assert body["unavailable_by_default"] is True
    assert body["sections"]
    assert body["cards"]
    assert body["data_source_references"]
    assert body["decision_reference"]["active_decision_object"] is False
    assert body["decision_reference"]["recommendation_available"] is False
    assert body["decision_reference"]["readiness_to_trade_available"] is False
    assert body["no_active_ui"] is True
    assert body["no_recommendations"] is True
    assert body["no_broker_controls"] is True
    assert body["no_execution"] is True
    assert body["recommendation_generated"] is False
    assert body["action_generated"] is False
    assert body["confidence_generated"] is False
    assert body["decision_object_generated"] is False
    assert body["readiness_to_trade"] is False
    assert body["broker_control_enabled"] is False
    assert body["execution_ready"] is False


def test_retail_dashboard_readiness_template_returns_no_active_ui_or_execution_readiness() -> None:
    response = client.get("/retail-dashboard/readiness-template")
    assert response.status_code == 200
    body = response.json()

    assert body["planning_only"] is True
    assert body["ready_for_active_ui"] is False
    assert body["ready_for_recommendations"] is False
    assert body["ready_for_broker_controls"] is False
    assert body["ready_for_execution"] is False
    assert body["no_readiness_to_trade"] is True
    report = body["readiness_report"]
    assert report["ready_for_active_ui"] is False
    assert report["ready_for_recommendations"] is False
    assert report["ready_for_broker_controls"] is False
    assert report["ready_for_execution"] is False
    assert report["ready_for_readiness_to_trade"] is False


def test_retail_dashboard_has_no_post_endpoints() -> None:
    for route in app.routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set())
        if path.startswith("/retail-dashboard"):
            assert "POST" not in methods
