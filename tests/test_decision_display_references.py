from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_display.references import (
    DecisionDisplayEvidenceReference,
    DecisionDisplaySafetyReference,
    default_decision_display_evidence_reference,
    default_decision_display_safety_reference,
)


def test_decision_display_evidence_reference_validates() -> None:
    reference = default_decision_display_evidence_reference()

    assert reference.required is True
    assert reference.display_ready is False


@pytest.mark.parametrize(
    "override",
    [
        {"required": False},
        {"complete": True},
        {"validation_passed": True},
        {"display_ready": True},
    ],
)
def test_decision_display_evidence_reference_rejects_ready_values(override: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        DecisionDisplayEvidenceReference(reference_id="display-evidence-reference-test", **override)


def test_decision_display_safety_reference_validates() -> None:
    reference = default_decision_display_safety_reference()

    assert reference.required is True
    assert reference.passed is False
    assert reference.display_ready is False


@pytest.mark.parametrize(
    "override",
    [
        {"required": False},
        {"passed": True},
        {"approval_granted": True},
        {"override_granted": True},
        {"execution_allowed": True},
        {"display_ready": True},
    ],
)
def test_decision_display_safety_reference_rejects_ready_values(override: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        DecisionDisplaySafetyReference(reference_id="display-safety-reference-test", **override)

