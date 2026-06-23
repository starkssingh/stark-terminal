from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_api.references import (
    DecisionEvidenceBundleReferencePlaceholder,
    DecisionSafetyReferencePlaceholder,
    default_decision_safety_reference_placeholder,
    default_evidence_bundle_reference_placeholder,
)


def test_evidence_bundle_reference_placeholder_validates() -> None:
    reference = DecisionEvidenceBundleReferencePlaceholder(reference_id="evidence-ref-1")

    assert reference.required is True
    assert reference.complete is False
    assert reference.validation_passed is False
    assert reference.human_review_attached is False
    assert reference.active_decision_object_ready is False


@pytest.mark.parametrize(
    "field",
    ["complete", "validation_passed", "human_review_attached", "active_decision_object_ready"],
)
def test_evidence_bundle_reference_rejects_active_state(field: str) -> None:
    with pytest.raises(ValidationError):
        DecisionEvidenceBundleReferencePlaceholder(reference_id="evidence-ref-1", **{field: True})


def test_decision_safety_reference_placeholder_validates() -> None:
    reference = DecisionSafetyReferencePlaceholder(reference_id="safety-ref-1")

    assert reference.required is True
    assert reference.passed is False
    assert reference.approval_granted is False
    assert reference.override_granted is False
    assert reference.execution_allowed is False


@pytest.mark.parametrize("field", ["passed", "approval_granted", "override_granted", "execution_allowed"])
def test_decision_safety_reference_rejects_passed_or_granted_state(field: str) -> None:
    with pytest.raises(ValidationError):
        DecisionSafetyReferencePlaceholder(reference_id="safety-ref-1", **{field: True})


def test_default_reference_placeholders_validate() -> None:
    assert default_evidence_bundle_reference_placeholder().active_decision_object_ready is False
    assert default_decision_safety_reference_placeholder().approval_granted is False

