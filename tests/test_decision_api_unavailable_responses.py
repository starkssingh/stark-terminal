from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_api.requests import DecisionAPIUnavailableReason
from stark_terminal_core.decision_api.unavailable import (
    DecisionDeskUnavailableResponse,
    default_decision_desk_unavailable_response,
)


def test_valid_decision_desk_unavailable_response() -> None:
    response = DecisionDeskUnavailableResponse(
        response_id="unavailable-1",
        reason=DecisionAPIUnavailableReason.CONTRACT_SKELETON_ONLY,
        message="Unavailable by design.",
        notes=[" contract ", ""],
    )

    assert response.unavailable is True
    assert response.planning_only is True
    assert response.notes == ["contract"]
    assert response.recommendations_allowed is False
    assert response.approval_granted is False


def test_unavailable_reason_unknown_rejected() -> None:
    with pytest.raises(ValidationError):
        DecisionDeskUnavailableResponse(
            response_id="unavailable-1",
            reason=DecisionAPIUnavailableReason.UNKNOWN,
            message="Unavailable.",
        )


@pytest.mark.parametrize(
    "field",
    [
        "unavailable",
        "planning_only",
    ],
)
def test_unavailable_response_enforces_true_flags(field: str) -> None:
    with pytest.raises(ValidationError):
        DecisionDeskUnavailableResponse(
            response_id="unavailable-1",
            reason=DecisionAPIUnavailableReason.CONTRACT_SKELETON_ONLY,
            message="Unavailable.",
            **{field: False},
        )


@pytest.mark.parametrize(
    "field",
    [
        "recommendations_allowed",
        "action_generation_allowed",
        "confidence_scoring_allowed",
        "decision_object_generation_allowed",
        "execution_allowed",
        "approval_granted",
        "override_granted",
    ],
)
def test_unavailable_response_rejects_dangerous_flags(field: str) -> None:
    with pytest.raises(ValidationError):
        DecisionDeskUnavailableResponse(
            response_id="unavailable-1",
            reason=DecisionAPIUnavailableReason.CONTRACT_SKELETON_ONLY,
            message="Unavailable.",
            **{field: True},
        )


def test_default_unavailable_response_validates() -> None:
    response = default_decision_desk_unavailable_response()

    assert response.reason == DecisionAPIUnavailableReason.CONTRACT_SKELETON_ONLY
    assert response.unavailable is True
    assert response.recommendations_allowed is False

