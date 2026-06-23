from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


def test_retail_dashboard_display_health_endpoint_is_safe() -> None:
    response = client.get("/retail-dashboard-display/health")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-retail-dashboard-display"
    assert body["enabled"] is True
    assert body["stage"] == "display_contract_skeleton"
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
    assert body["layout_count"] > 0
    assert body["widget_count"] > 0
    assert body["section_count"] > 0
    assert body["badge_count"] > 0
    assert body["status"] == "healthy"
    assert "password" not in str(body).lower()
    assert "secret" not in str(body).lower()


def test_retail_dashboard_display_contracts_endpoint_returns_metadata() -> None:
    response = client.get("/retail-dashboard-display/contracts")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-retail-dashboard-display"
    assert body["computation_scope"] == "display-contract-skeleton-only"
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
    assert "RETAIL_OVERVIEW_PLACEHOLDER" in body["layout_kinds"]
    assert "PLACEHOLDER" in body["widget_kinds"]
    assert "OVERVIEW" in body["section_kinds"]
    assert "PLANNING_ONLY" in body["badge_kinds"]
    assert "execution_apis" in body["forbidden_outputs"]


def test_retail_dashboard_display_unavailable_template_returns_no_generated_outputs() -> None:
    response = client.get("/retail-dashboard-display/unavailable-template")
    assert response.status_code == 200
    body = response.json()

    assert body["display_contract_skeleton_only"] is True
    unavailable = body["unavailable_response"]
    assert unavailable["unavailable"] is True
    assert unavailable["display_contract_only"] is True
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


def test_retail_dashboard_display_placeholder_layout_returns_placeholders_only() -> None:
    response = client.get("/retail-dashboard-display/placeholder-layout")
    assert response.status_code == 200
    body = response.json()

    assert body["display_contract_skeleton_only"] is True
    assert body["no_generated_outputs"] is True
    assert body["layouts"]
    assert body["widgets"]
    assert body["visual_sections"]
    assert body["badges"]
    for collection in ["layouts", "widgets", "visual_sections"]:
        for item in body[collection]:
            assert item["active_ui"] is False
            assert item["unavailable"] is True
    for badge in body["badges"]:
        assert badge["active_ui"] is False
        assert badge["recommendation"] is False
        assert badge["readiness_to_trade"] is False
        assert badge["execution_ready"] is False
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


def test_retail_dashboard_display_has_no_post_endpoints() -> None:
    paths = app.openapi()["paths"]
    for path, operations in paths.items():
        if path.startswith("/retail-dashboard-display"):
            assert "post" not in operations
            assert "put" not in operations
            assert "patch" not in operations
            assert "delete" not in operations
