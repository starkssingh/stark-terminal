from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_readiness_api.references import (
    DecisionReadinessBlockedOutputReference,
    DecisionReadinessEvidenceReference,
    DecisionReadinessHumanReviewReference,
    DecisionReadinessSafetyReference,
    default_decision_readiness_blocked_output_reference,
    default_decision_readiness_evidence_reference,
    default_decision_readiness_human_review_reference,
    default_decision_readiness_safety_reference,
)


def test_evidence_reference_placeholder_validates() -> None:
    reference = DecisionReadinessEvidenceReference(reference_id="evidence-ref-1")

    assert reference.required is True
    assert reference.complete is False
    assert reference.validation_passed is False
    assert reference.human_review_attached is False
    assert reference.active_decision_object_ready is False


@pytest.mark.parametrize(
    "field",
    ["complete", "validation_passed", "human_review_attached", "active_decision_object_ready"],
)
def test_evidence_reference_rejects_active_state(field: str) -> None:
    with pytest.raises(ValidationError):
        DecisionReadinessEvidenceReference(reference_id="evidence-ref-1", **{field: True})


def test_safety_reference_placeholder_validates() -> None:
    reference = DecisionReadinessSafetyReference(reference_id="safety-ref-1")

    assert reference.required is True
    assert reference.passed is False
    assert reference.approval_granted is False
    assert reference.override_granted is False
    assert reference.execution_allowed is False


@pytest.mark.parametrize("field", ["passed", "approval_granted", "override_granted", "execution_allowed"])
def test_safety_reference_rejects_passed_or_granted_state(field: str) -> None:
    with pytest.raises(ValidationError):
        DecisionReadinessSafetyReference(reference_id="safety-ref-1", **{field: True})


def test_human_review_reference_cannot_grant_approval_or_bypass() -> None:
    reference = DecisionReadinessHumanReviewReference(reference_id="human-review-ref-1")

    assert reference.required is True
    assert reference.approval_granted is False
    assert reference.bypass_allowed is False

    for field in ["approval_granted", "bypass_allowed"]:
        with pytest.raises(ValidationError):
            DecisionReadinessHumanReviewReference(reference_id="human-review-ref-1", **{field: True})


@pytest.mark.parametrize(
    "field",
    [
        "policy_active",
        "recommendations_blocked",
        "action_generation_blocked",
        "confidence_scoring_blocked",
        "decision_object_generation_blocked",
        "execution_blocked",
    ],
)
def test_blocked_output_reference_enforces_fail_closed_flags(field: str) -> None:
    with pytest.raises(ValidationError):
        DecisionReadinessBlockedOutputReference(reference_id="blocked-output-ref-1", **{field: False})


def test_blocked_output_reference_rejects_bypass() -> None:
    with pytest.raises(ValidationError):
        DecisionReadinessBlockedOutputReference(reference_id="blocked-output-ref-1", bypass_allowed=True)


def test_default_reference_placeholders_validate() -> None:
    assert default_decision_readiness_evidence_reference().active_decision_object_ready is False
    assert default_decision_readiness_safety_reference().approval_granted is False
    assert default_decision_readiness_human_review_reference().bypass_allowed is False
    assert default_decision_readiness_blocked_output_reference().execution_blocked is True
