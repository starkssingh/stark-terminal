from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_evidence_validation.contracts import (
    DecisionEvidenceValidationRequest,
    default_decision_evidence_validation_request,
)


def test_decision_evidence_validation_request_validates() -> None:
    request = DecisionEvidenceValidationRequest(request_id="validation-request-test")

    assert request.validate_items is True
    assert request.validate_provenance is True
    assert request.validate_checklist is True
    assert request.validate_human_review is True
    assert request.validate_safety_flags is True
    assert request.recommendations_allowed is False
    assert request.decision_object_generation_allowed is False
    assert request.readiness_to_trade_allowed is False


def test_decision_evidence_validation_request_requires_at_least_one_validation_flag() -> None:
    with pytest.raises(ValidationError):
        DecisionEvidenceValidationRequest(
            request_id="validation-request-test",
            validate_items=False,
            validate_provenance=False,
            validate_checklist=False,
            validate_human_review=False,
            validate_safety_flags=False,
        )


@pytest.mark.parametrize(
    "override",
    [
        {"recommendations_allowed": True},
        {"action_generation_allowed": True},
        {"confidence_scoring_allowed": True},
        {"decision_object_generation_allowed": True},
        {"execution_allowed": True},
        {"approval_allowed": True},
        {"override_allowed": True},
        {"readiness_to_trade_allowed": True},
    ],
)
def test_decision_evidence_validation_request_rejects_dangerous_flags(
    override: dict[str, object],
) -> None:
    with pytest.raises(ValidationError):
        DecisionEvidenceValidationRequest(request_id="validation-request-test", **override)


def test_default_decision_evidence_validation_request_validates() -> None:
    request = default_decision_evidence_validation_request()

    assert request.request_id == "decision-evidence-validation-request-v1"
    assert request.bundle_id is None
    assert request.notes

