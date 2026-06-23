from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


def test_decision_boundary_health_endpoint_is_safe() -> None:
    response = client.get("/decision-boundary/health")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-decision-boundary"
    assert body["enabled"] is True
    assert body["stage"] == "boundary_hardening"
    assert body["forbidden_behavior_count"] > 0
    assert body["endpoint_policy_count"] > 0
    assert body["module_policy_count"] > 0
    assert body["invariant_passed"] is True
    assert body["recommendations_allowed"] is False
    assert body["action_generation_allowed"] is False
    assert body["confidence_scoring_allowed"] is False
    assert body["decision_object_generation_allowed"] is False
    assert body["execution_allowed"] is False
    assert body["approval_allowed"] is False
    assert body["override_allowed"] is False
    assert body["active_ui_allowed"] is False
    assert body["active_workflow_allowed"] is False
    assert body["readiness_to_trade_allowed"] is False
    assert body["status"] == "healthy"
    assert "password" not in str(body).lower()
    assert "secret" not in str(body).lower()


def test_decision_boundary_contracts_endpoint_returns_boundary_metadata() -> None:
    response = client.get("/decision-boundary/contracts")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-decision-boundary"
    assert body["computation_scope"] == "boundary-hardening-only"
    assert "RECOMMENDATION" in body["forbidden_behaviors"]
    assert "EXECUTION" in body["forbidden_behaviors"]
    assert "decision-readiness-api" in body["endpoint_families"]
    assert "decision-human-review" in body["endpoint_families"]
    assert "decision_boundary" in body["module_families"]
    assert body["recommendations_allowed_now"] is False
    assert body["action_generation_allowed_now"] is False
    assert body["confidence_scoring_allowed_now"] is False
    assert body["decision_object_generation_allowed_now"] is False
    assert body["execution_allowed_now"] is False
    assert body["approval_allowed_now"] is False
    assert body["override_allowed_now"] is False
    assert body["active_ui_allowed_now"] is False
    assert body["active_workflow_allowed_now"] is False
    assert body["readiness_to_trade_allowed_now"] is False


def test_decision_boundary_invariants_endpoint_returns_safe_result() -> None:
    response = client.get("/decision-boundary/invariants")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-decision-boundary"
    assert body["boundary_hardening_only"] is True
    assert body["invariant_result"]["passed"] is True
    assert body["blockers"] == []
    assert body["no_recommendations"] is True
    assert body["no_action_generation"] is True
    assert body["no_confidence_scoring"] is True
    assert body["no_decision_object"] is True
    assert body["no_approval"] is True
    assert body["no_override"] is True
    assert body["no_active_ui"] is True
    assert body["no_active_workflow"] is True
    assert body["no_readiness_to_trade"] is True
    assert body["no_execution"] is True
    assert body["recommendation_generated"] is False
    assert body["action_generated"] is False
    assert body["confidence_generated"] is False
    assert body["decision_object_generated"] is False
    assert body["approval_granted"] is False
    assert body["override_granted"] is False
    assert body["active_ui"] is False
    assert body["workflow_active"] is False
    assert body["readiness_to_trade"] is False
    assert body["execution_ready"] is False


def test_decision_boundary_has_no_post_endpoints() -> None:
    for route in app.routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set())
        if path.startswith("/decision-boundary"):
            assert "POST" not in methods
