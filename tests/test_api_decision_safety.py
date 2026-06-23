from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


def test_decision_safety_health_endpoint_is_safe() -> None:
    response = client.get("/decision-safety/health")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-decision-safety"
    assert body["enabled"] is True
    assert body["stage"] == "guardrails_only"
    assert body["recommendations_allowed"] is False
    assert body["action_generation_allowed"] is False
    assert body["confidence_scoring_allowed"] is False
    assert body["decision_object_generation_allowed"] is False
    assert body["execution_allowed"] is False
    assert body["human_approval_allowed"] is False
    assert body["overrides_allowed"] is False
    assert body["human_review_required"] is True
    assert body["blocked_output_policy_required"] is True
    assert body["default_guardrail_count"] > 0
    assert "password" not in str(body).lower()
    assert "secret" not in str(body).lower()


def test_decision_safety_contracts_endpoint_is_guardrails_only() -> None:
    response = client.get("/decision-safety/contracts")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-decision-safety"
    assert body["computation_scope"] == "guardrails-only"
    assert body["recommendations_allowed_now"] is False
    assert body["action_generation_allowed_now"] is False
    assert body["confidence_scoring_allowed_now"] is False
    assert body["decision_object_generation_allowed_now"] is False
    assert body["execution_allowed_now"] is False
    assert body["human_approval_allowed_now"] is False
    assert body["overrides_allowed_now"] is False
    assert "RECOMMENDATION" in body["blocked_outputs"]
    assert "DecisionObject_generation" in body["forbidden_outputs"]


def test_decision_safety_templates_do_not_generate_outputs_or_approvals() -> None:
    readiness = client.get("/decision-safety/readiness-template").json()
    assert readiness["guardrails_only"] is True
    assert readiness["recommendations_allowed_now"] is False
    assert readiness["decision_object_generation_allowed_now"] is False
    assert readiness["execution_allowed_now"] is False
    assert readiness["approval_granted"] is False
    assert readiness["overrides_allowed_now"] is False
    assert readiness["must_not_generate_action_states"] is True
    assert readiness["must_not_generate_confidence_scores"] is True
    assert readiness["must_not_generate_decision_objects"] is True
    assert readiness["must_not_generate_recommendations"] is True
    assert readiness["readiness_report"]["ready_for_recommendations"] is False
    assert readiness["readiness_report"]["ready_for_decision_object_generation"] is False
    assert readiness["readiness_report"]["ready_for_execution"] is False

    human_review = client.get("/decision-safety/human-review-template").json()
    assert human_review["guardrails_only"] is True
    assert human_review["approval_granted"] is False
    assert human_review["no_decision_object_generation"] is True
    assert human_review["no_execution"] is True
    assert "password" not in str(human_review).lower()
    assert "secret" not in str(human_review).lower()
