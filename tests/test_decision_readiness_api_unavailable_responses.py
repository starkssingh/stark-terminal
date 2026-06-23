from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_readiness_api.requests import DecisionReadinessUnavailableReason
from stark_terminal_core.decision_readiness_api.unavailable import (
    DecisionReadinessUnavailableResponse,
    default_decision_readiness_unavailable_response,
)


def test_valid_decision_readiness_unavailable_response() -> None:
    response = DecisionReadinessUnavailableResponse(
        response_id="readiness-unavailable-1",
        reason=DecisionReadinessUnavailableReason.CONTRACT_SKELETON_ONLY,
        message="Unavailable by design.",
        notes=[" contract ", ""],
    )

    assert response.unavailable is True
    assert response.planning_only is True
    assert response.readiness_status_available is False
    assert response.notes == ["contract"]
    assert response.recommendations_allowed is False
    assert response.approval_granted is False


def test_readiness_unavailable_reason_unknown_rejected() -> None:
    with pytest.raises(ValidationError):
        DecisionReadinessUnavailableResponse(
            response_id="readiness-unavailable-1",
            reason=DecisionReadinessUnavailableReason.UNKNOWN,
            message="Unavailable.",
        )


@pytest.mark.parametrize("field", ["unavailable", "planning_only"])
def test_readiness_unavailable_response_enforces_true_flags(field: str) -> None:
    with pytest.raises(ValidationError):
        DecisionReadinessUnavailableResponse(
            response_id="readiness-unavailable-1",
            reason=DecisionReadinessUnavailableReason.CONTRACT_SKELETON_ONLY,
            message="Unavailable.",
            **{field: False},
        )


@pytest.mark.parametrize(
    "field",
    [
        "readiness_status_available",
        "recommendations_allowed",
        "action_generation_allowed",
        "confidence_scoring_allowed",
        "decision_object_generation_allowed",
        "execution_allowed",
        "approval_granted",
        "override_granted",
    ],
)
def test_readiness_unavailable_response_rejects_dangerous_flags(field: str) -> None:
    with pytest.raises(ValidationError):
        DecisionReadinessUnavailableResponse(
            response_id="readiness-unavailable-1",
            reason=DecisionReadinessUnavailableReason.CONTRACT_SKELETON_ONLY,
            message="Unavailable.",
            **{field: True},
        )


def test_default_readiness_unavailable_response_validates() -> None:
    response = default_decision_readiness_unavailable_response()

    assert response.reason == DecisionReadinessUnavailableReason.CONTRACT_SKELETON_ONLY
    assert response.unavailable is True
    assert response.readiness_status_available is False
    assert response.recommendations_allowed is False
