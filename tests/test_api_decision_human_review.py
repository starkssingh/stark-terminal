from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


def test_decision_human_review_health_endpoint_is_safe() -> None:
    response = client.get("/decision-human-review/health")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-decision-human-review"
    assert body["enabled"] is True
    assert body["stage"] == "workflow_skeleton"
    assert body["active_workflow_allowed"] is False
    assert body["task_assignment_allowed"] is False
    assert body["reviewer_auth_allowed"] is False
    assert body["notifications_allowed"] is False
    assert body["approval_allowed"] is False
    assert body["override_allowed"] is False
    assert body["recommendations_allowed"] is False
    assert body["action_generation_allowed"] is False
    assert body["confidence_scoring_allowed"] is False
    assert body["decision_object_generation_allowed"] is False
    assert body["readiness_to_trade_allowed"] is False
    assert body["execution_allowed"] is False
    assert body["returns_unavailable_by_default"] is True
    assert body["default_task_count"] > 0
    assert body["default_role_count"] > 0
    assert body["default_queue_count"] > 0
    assert body["status"] == "healthy"
    assert "password" not in str(body).lower()
    assert "secret" not in str(body).lower()


def test_decision_human_review_contracts_endpoint_is_workflow_skeleton_only() -> None:
    response = client.get("/decision-human-review/contracts")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-decision-human-review"
    assert body["computation_scope"] == "workflow-skeleton-only"
    assert body["active_workflow_allowed_now"] is False
    assert body["task_assignment_allowed_now"] is False
    assert body["reviewer_auth_allowed_now"] is False
    assert body["notifications_allowed_now"] is False
    assert body["approval_allowed_now"] is False
    assert body["override_allowed_now"] is False
    assert body["recommendations_allowed_now"] is False
    assert body["action_generation_allowed_now"] is False
    assert body["confidence_scoring_allowed_now"] is False
    assert body["decision_object_generation_allowed_now"] is False
    assert body["readiness_to_trade_allowed_now"] is False
    assert body["execution_allowed_now"] is False
    assert "EVIDENCE_REVIEW" in body["task_kinds"]
    assert "HUMAN_OPERATOR" in body["reviewer_roles"]
    assert "PLACEHOLDER_QUEUE" in body["queue_kinds"]
    assert "execution_apis" in body["forbidden_outputs"]


def test_decision_human_review_unavailable_template_and_placeholder_workflow_are_safe() -> None:
    template = client.get("/decision-human-review/unavailable-template").json()
    assert template["workflow_skeleton_only"] is True
    assert template["unavailable_response"]["unavailable"] is True
    assert template["unavailable_response"]["approval_allowed"] is False
    assert template["unavailable_response"]["execution_allowed"] is False
    assert template["no_active_workflow"] is True
    assert template["no_task_assignment"] is True
    assert template["no_reviewer_auth"] is True
    assert template["no_notifications"] is True
    assert template["no_approval"] is True
    assert template["no_override"] is True
    assert template["no_recommendations"] is True
    assert template["no_readiness_to_trade"] is True
    assert template["no_execution"] is True

    placeholder = client.get("/decision-human-review/placeholder-workflow").json()
    assert placeholder["workflow_skeleton_only"] is True
    assert placeholder["workflow_contract"]["active_workflow"] is False
    assert placeholder["task_placeholders"]
    assert placeholder["role_placeholders"]
    assert placeholder["queue_placeholders"]
    assert placeholder["status_placeholder"]["workflow_active"] is False
    assert placeholder["unavailable_response"]["workflow_skeleton_only"] is True
    assert placeholder["approval_granted"] is False
    assert placeholder["override_granted"] is False
    assert placeholder["recommendation_generated"] is False
    assert placeholder["action_generated"] is False
    assert placeholder["confidence_generated"] is False
    assert placeholder["decision_object_generated"] is False
    assert placeholder["readiness_to_trade_generated"] is False
    assert placeholder["execution_ready"] is False
    assert "password" not in str(placeholder).lower()
    assert "secret" not in str(placeholder).lower()


def test_decision_human_review_has_no_post_endpoints() -> None:
    for route in app.routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set())
        if path.startswith("/decision-human-review"):
            assert "POST" not in methods
