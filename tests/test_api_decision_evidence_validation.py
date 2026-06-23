from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


def test_decision_evidence_validation_health_endpoint_is_safe() -> None:
    response = client.get("/decision-evidence-validation/health")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-decision-evidence-validation"
    assert body["enabled"] is True
    assert body["stage"] == "validation_v0"
    assert body["recommendations_allowed"] is False
    assert body["action_generation_allowed"] is False
    assert body["confidence_scoring_allowed"] is False
    assert body["decision_object_generation_allowed"] is False
    assert body["execution_allowed"] is False
    assert body["approval_allowed"] is False
    assert body["override_allowed"] is False
    assert body["readiness_to_trade_allowed"] is False
    assert body["validation_only"] is True
    assert body["status"] == "healthy"
    assert "password" not in str(body).lower()
    assert "secret" not in str(body).lower()


def test_decision_evidence_validation_contracts_endpoint_is_validation_only() -> None:
    response = client.get("/decision-evidence-validation/contracts")
    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "stark-terminal-decision-evidence-validation"
    assert body["computation_scope"] == "validation-only"
    assert body["recommendations_allowed_now"] is False
    assert body["action_generation_allowed_now"] is False
    assert body["confidence_scoring_allowed_now"] is False
    assert body["decision_object_generation_allowed_now"] is False
    assert body["execution_allowed_now"] is False
    assert body["approval_allowed_now"] is False
    assert body["override_allowed_now"] is False
    assert body["readiness_to_trade_allowed_now"] is False
    assert body["validation_only"] is True
    assert "MISSING_EVIDENCE_ITEM" in body["issue_kinds"]
    assert "BLOCKER" in body["issue_severities"]
    assert "DecisionObject_generation" in body["forbidden_outputs"]
    assert "execution_apis" in body["forbidden_outputs"]


def test_decision_evidence_validation_template_and_sample_do_not_generate_outputs() -> None:
    template = client.get("/decision-evidence-validation/template").json()
    assert template["validation_only"] is True
    assert template["default_validation_request"]["recommendations_allowed"] is False
    assert template["default_validation_result_template"]["validation_only"] is True
    assert template["default_validation_result_template"]["decision_object_generation_allowed"] is False
    assert template["no_recommendations"] is True
    assert template["no_decision_object"] is True
    assert template["no_approval"] is True
    assert template["no_readiness_to_trade"] is True
    assert template["no_execution"] is True

    sample = client.get("/decision-evidence-validation/sample").json()
    assert sample["validation_only"] is True
    assert sample["sample_scope"] == "built-in-default-contracts-only"
    assert sample["accepts_user_input"] is False
    assert sample["validation_result"]["validation_only"] is True
    assert sample["validation_result"]["recommendations_allowed"] is False
    assert sample["validation_result"]["decision_object_generation_allowed"] is False
    assert sample["validation_result"]["readiness_to_trade"] is False
    assert sample["no_recommendations"] is True
    assert sample["no_decision_object"] is True
    assert sample["no_approval"] is True
    assert sample["no_readiness_to_trade"] is True
    assert "password" not in str(sample).lower()
    assert "secret" not in str(sample).lower()

