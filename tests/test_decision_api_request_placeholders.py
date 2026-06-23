from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_api.requests import (
    DecisionAPIRequestKind,
    DecisionDeskRequestPlaceholder,
    default_decision_desk_request_placeholder,
)


def test_valid_decision_desk_request_placeholder() -> None:
    placeholder = DecisionDeskRequestPlaceholder(
        request_id="request-1",
        request_kind=DecisionAPIRequestKind.SNAPSHOT_REQUEST,
        requested_sections=[" instrument ", "", "safety"],
        notes=[" contract ", ""],
    )

    assert placeholder.request_id == "request-1"
    assert placeholder.request_kind == DecisionAPIRequestKind.SNAPSHOT_REQUEST
    assert placeholder.requested_sections == ["instrument", "safety"]
    assert placeholder.notes == ["contract"]
    assert placeholder.evidence_bundle_reference_required is True
    assert placeholder.safety_reference_required is True
    assert placeholder.human_review_required is True


def test_unknown_request_kind_rejected() -> None:
    with pytest.raises(ValidationError):
        DecisionDeskRequestPlaceholder(
            request_id="request-1",
            request_kind=DecisionAPIRequestKind.UNKNOWN,
        )


@pytest.mark.parametrize(
    "field",
    [
        "recommendations_allowed",
        "action_generation_allowed",
        "confidence_scoring_allowed",
        "decision_object_generation_allowed",
        "execution_allowed",
    ],
)
def test_request_placeholder_rejects_dangerous_flags(field: str) -> None:
    with pytest.raises(ValidationError):
        DecisionDeskRequestPlaceholder(
            request_id="request-1",
            request_kind=DecisionAPIRequestKind.SNAPSHOT_REQUEST,
            **{field: True},
        )


def test_default_request_placeholder_validates() -> None:
    placeholder = default_decision_desk_request_placeholder()

    assert placeholder.request_kind == DecisionAPIRequestKind.SNAPSHOT_REQUEST
    assert placeholder.evidence_bundle_reference_required is True
    assert placeholder.safety_reference_required is True
    assert placeholder.recommendations_allowed is False

