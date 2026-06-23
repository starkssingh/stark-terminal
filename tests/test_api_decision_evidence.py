from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


def test_decision_evidence_health_endpoint_is_safe() -> None:
    response = client.get("/decision-evidence/health")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-decision-evidence"
    assert body["enabled"] is True
    assert body["planning_stage"] == "contracts_only"
    assert body["real_data_allowed"] is False
    assert body["recommendations_allowed"] is False
    assert body["action_generation_allowed"] is False
    assert body["confidence_scoring_allowed"] is False
    assert body["decision_object_generation_allowed"] is False
    assert body["execution_allowed"] is False
    assert body["source_reference_required"] is True
    assert body["validation_checklist_required"] is True
    assert body["human_review_attachment_required"] is True
    assert body["default_evidence_item_count"] > 0
    assert "password" not in str(body).lower()
    assert "secret" not in str(body).lower()


def test_decision_evidence_contracts_endpoint_is_contracts_only() -> None:
    response = client.get("/decision-evidence/contracts")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-decision-evidence"
    assert body["computation_scope"] == "contracts-only"
    assert body["recommendations_allowed_now"] is False
    assert body["action_generation_allowed_now"] is False
    assert body["confidence_scoring_allowed_now"] is False
    assert body["decision_object_generation_allowed_now"] is False
    assert body["execution_allowed_now"] is False
    assert "DATA_QUALITY" in body["default_evidence_item_kinds"]
    assert "DecisionObject_generation" in body["forbidden_outputs"]


def test_decision_evidence_templates_do_not_generate_outputs() -> None:
    readiness = client.get("/decision-evidence/readiness-template").json()
    assert readiness["contracts_only"] is True
    assert readiness["must_not_generate_action_states"] is True
    assert readiness["must_not_generate_confidence_scores"] is True
    assert readiness["must_not_generate_decision_objects"] is True
    assert readiness["must_not_generate_recommendations"] is True
    assert readiness["readiness_report"]["ready_for_decision_object_generation"] is False
    assert readiness["readiness_report"]["ready_for_recommendations"] is False
    assert readiness["readiness_report"]["ready_for_execution"] is False

    human_review = client.get("/decision-evidence/human-review-template").json()
    assert human_review["contracts_only"] is True
    assert human_review["approval_granted"] is False
    assert human_review["no_decision_object_generation"] is True
    assert human_review["no_execution"] is True
