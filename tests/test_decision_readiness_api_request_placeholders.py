from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_readiness_api.requests import (
    DecisionReadinessRequestKind,
    DecisionReadinessRequestPlaceholder,
    default_decision_readiness_request_placeholder,
)


def test_valid_decision_readiness_request_placeholder() -> None:
    placeholder = DecisionReadinessRequestPlaceholder(
        request_id="readiness-request-1",
        request_kind=DecisionReadinessRequestKind.READINESS_STATUS_REQUEST,
        requested_readiness_sections=[" evidence ", "", "safety"],
        notes=[" contract ", ""],
    )

    assert placeholder.request_id == "readiness-request-1"
    assert placeholder.request_kind == DecisionReadinessRequestKind.READINESS_STATUS_REQUEST
    assert placeholder.requested_readiness_sections == ["evidence", "safety"]
    assert placeholder.notes == ["contract"]
    assert placeholder.evidence_reference_required is True
    assert placeholder.safety_reference_required is True
    assert placeholder.human_review_reference_required is True
    assert placeholder.blocked_output_reference_required is True


def test_unknown_readiness_request_kind_rejected() -> None:
    with pytest.raises(ValidationError):
        DecisionReadinessRequestPlaceholder(
            request_id="readiness-request-1",
            request_kind=DecisionReadinessRequestKind.UNKNOWN,
        )


@pytest.mark.parametrize(
    "field",
    [
        "recommendations_allowed",
        "action_generation_allowed",
        "confidence_scoring_allowed",
        "decision_object_generation_allowed",
        "execution_allowed",
        "approval_allowed",
        "override_allowed",
    ],
)
def test_readiness_request_placeholder_rejects_dangerous_flags(field: str) -> None:
    with pytest.raises(ValidationError):
        DecisionReadinessRequestPlaceholder(
            request_id="readiness-request-1",
            request_kind=DecisionReadinessRequestKind.READINESS_STATUS_REQUEST,
            **{field: True},
        )


def test_default_readiness_request_placeholder_validates() -> None:
    placeholder = default_decision_readiness_request_placeholder()

    assert placeholder.request_kind == DecisionReadinessRequestKind.READINESS_STATUS_REQUEST
    assert placeholder.evidence_reference_required is True
    assert placeholder.safety_reference_required is True
    assert placeholder.human_review_reference_required is True
    assert placeholder.blocked_output_reference_required is True
    assert placeholder.recommendations_allowed is False
