from __future__ import annotations

from stark_terminal_core.decision_evidence_validation.contracts import (
    DecisionEvidenceValidationIssueKind,
    DecisionEvidenceValidationIssueSeverity,
)
from stark_terminal_core.decision_evidence_validation.issues import create_validation_issue
from stark_terminal_core.decision_evidence_validation.results import (
    create_invalid_decision_evidence_validation_result,
    create_valid_decision_evidence_validation_result,
)
from stark_terminal_core.decision_evidence_validation.safety import (
    default_decision_evidence_validation_safety_policy,
    evaluate_decision_evidence_validation_result_safety,
    reject_validation_as_decision_object_readiness,
    reject_validation_as_recommendation,
)


def test_default_decision_evidence_validation_safety_policy_forbids_dangerous_outputs() -> None:
    policy = default_decision_evidence_validation_safety_policy()

    assert policy.allow_recommendations is False
    assert policy.allow_action_generation is False
    assert policy.allow_confidence_scoring is False
    assert policy.allow_decision_object_generation is False
    assert policy.allow_execution is False
    assert policy.allow_approval is False
    assert policy.allow_override is False
    assert policy.allow_readiness_to_trade is False
    assert policy.require_validation_only is True


def test_validation_result_cannot_be_treated_as_recommendation_or_decisionobject_readiness() -> None:
    recommendation = reject_validation_as_recommendation()
    decision_object = reject_validation_as_decision_object_readiness()

    assert recommendation.decision == "blocked"
    assert decision_object.decision == "blocked"
    assert "recommendations" in recommendation.reasons[0]
    assert "DecisionObject" in decision_object.reasons[0]


def test_unsafe_result_blocks_and_safe_validation_only_result_passes_safely() -> None:
    policy = default_decision_evidence_validation_safety_policy()
    blocker = create_validation_issue(
        issue_id="blocker",
        kind=DecisionEvidenceValidationIssueKind.MISSING_VALIDATION_CHECKLIST,
        severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
        message="Missing checklist.",
    )
    unsafe_result = create_invalid_decision_evidence_validation_result("request-test", [blocker])
    safe_result = create_valid_decision_evidence_validation_result("request-test")

    unsafe_evaluation = evaluate_decision_evidence_validation_result_safety(unsafe_result, policy)
    safe_evaluation = evaluate_decision_evidence_validation_result_safety(safe_result, policy)

    assert unsafe_evaluation.decision == "blocked"
    assert "validation blockers remain unresolved" in unsafe_evaluation.reasons
    assert safe_evaluation.decision == "validation_only_allowed"
    assert any("validation-only" in reason for reason in safe_evaluation.reasons)

