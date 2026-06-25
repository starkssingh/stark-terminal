from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


def test_retail_trader_experience_boundary_health_endpoint_is_safe() -> None:
    response = client.get("/retail-trader-experience-boundary/health")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-retail-trader-experience-boundary"
    assert body["enabled"] is True
    assert body["stage"] == "boundary_hardening"
    assert body["forbidden_behavior_count"] > 0
    assert body["endpoint_policy_count"] == 4
    assert body["module_policy_count"] == 4
    assert body["invariant_passed"] is True
    assert body["active_ui_allowed"] is False
    assert body["frontend_components_allowed"] is False
    assert body["desktop_components_allowed"] is False
    assert body["recommendations_allowed"] is False
    assert body["action_generation_allowed"] is False
    assert body["confidence_scoring_allowed"] is False
    assert body["decision_object_generation_allowed"] is False
    assert body["readiness_to_trade_allowed"] is False
    assert body["suitability_profiling_allowed"] is False
    assert body["broker_controls_allowed"] is False
    assert body["execution_allowed"] is False
    assert body["approval_allowed"] is False
    assert body["override_allowed"] is False
    assert body["status"] == "healthy"
    assert "password" not in str(body).lower()
    assert "secret" not in str(body).lower()


def test_retail_trader_experience_boundary_contracts_endpoint_returns_policy_metadata() -> None:
    response = client.get("/retail-trader-experience-boundary/contracts")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-retail-trader-experience-boundary"
    assert body["computation_scope"] == "boundary-hardening-only"
    assert "ACTIVE_UI" in body["forbidden_behaviors"]
    assert "RECOMMENDATION_CARD" in body["forbidden_behaviors"]
    assert "SUITABILITY_PROFILING" in body["forbidden_behaviors"]
    assert "EXECUTION" in body["forbidden_behaviors"]
    assert "retail-trader-experience-boundary" in body["endpoint_families"]
    assert "retail_trader_experience_boundary" in body["module_families"]
    assert body["active_ui_allowed_now"] is False
    assert body["frontend_components_allowed_now"] is False
    assert body["desktop_components_allowed_now"] is False
    assert body["recommendations_allowed_now"] is False
    assert body["action_generation_allowed_now"] is False
    assert body["confidence_scoring_allowed_now"] is False
    assert body["decision_object_generation_allowed_now"] is False
    assert body["readiness_to_trade_allowed_now"] is False
    assert body["suitability_profiling_allowed_now"] is False
    assert body["broker_controls_allowed_now"] is False
    assert body["execution_allowed_now"] is False
    assert body["approval_allowed_now"] is False
    assert body["override_allowed_now"] is False


def test_retail_trader_experience_boundary_invariants_endpoint_returns_safe_result() -> None:
    response = client.get("/retail-trader-experience-boundary/invariants")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-retail-trader-experience-boundary"
    assert body["boundary_hardening_only"] is True
    assert body["invariant_result"]["passed"] is True
    assert body["blockers"] == []
    assert body["no_active_ui"] is True
    assert body["no_frontend_components"] is True
    assert body["no_desktop_components"] is True
    assert body["no_recommendations"] is True
    assert body["no_action_generation"] is True
    assert body["no_confidence_scoring"] is True
    assert body["no_decision_object"] is True
    assert body["no_readiness_to_trade"] is True
    assert body["no_suitability_profiling"] is True
    assert body["no_broker_controls"] is True
    assert body["no_approval"] is True
    assert body["no_override"] is True
    assert body["no_execution"] is True
    assert body["recommendation_generated"] is False
    assert body["action_generated"] is False
    assert body["confidence_generated"] is False
    assert body["decision_object_generated"] is False
    assert body["readiness_to_trade_generated"] is False
    assert body["suitability_profile_generated"] is False
    assert body["broker_control_enabled"] is False
    assert body["approval_granted"] is False
    assert body["override_granted"] is False
    assert body["execution_ready"] is False


def test_retail_trader_experience_boundary_has_no_post_endpoints() -> None:
    for route in app.routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set())
        if path.startswith("/retail-trader-experience-boundary"):
            assert "POST" not in methods
