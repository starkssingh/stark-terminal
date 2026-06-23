from __future__ import annotations

import pytest

from stark_terminal_core.decision_human_review.unavailable import (
    DecisionHumanReviewUnavailableResponse,
    default_decision_human_review_unavailable_response,
)


def _response_kwargs() -> dict[str, object]:
    return {
        "response_id": "response-test",
        "message": "Human review workflow unavailable",
    }


def test_valid_decision_human_review_unavailable_response() -> None:
    response = DecisionHumanReviewUnavailableResponse(**_response_kwargs())

    assert response.unavailable is True
    assert response.workflow_skeleton_only is True
    assert response.active_workflow_allowed is False
    assert response.task_assignment_allowed is False
    assert response.reviewer_auth_allowed is False
    assert response.notifications_allowed is False
    assert response.approval_allowed is False
    assert response.override_allowed is False
    assert response.recommendations_allowed is False
    assert response.action_generation_allowed is False
    assert response.confidence_scoring_allowed is False
    assert response.decision_object_generation_allowed is False
    assert response.readiness_to_trade_allowed is False
    assert response.execution_allowed is False


@pytest.mark.parametrize("flag", ["unavailable", "workflow_skeleton_only"])
def test_decision_human_review_unavailable_response_enforces_true_flags(flag: str) -> None:
    kwargs = _response_kwargs()
    kwargs[flag] = False

    with pytest.raises(ValueError):
        DecisionHumanReviewUnavailableResponse(**kwargs)


@pytest.mark.parametrize(
    "flag",
    [
        "active_workflow_allowed",
        "task_assignment_allowed",
        "reviewer_auth_allowed",
        "notifications_allowed",
        "approval_allowed",
        "override_allowed",
        "recommendations_allowed",
        "action_generation_allowed",
        "confidence_scoring_allowed",
        "decision_object_generation_allowed",
        "readiness_to_trade_allowed",
        "execution_allowed",
    ],
)
def test_decision_human_review_unavailable_response_rejects_dangerous_flags(flag: str) -> None:
    kwargs = _response_kwargs()
    kwargs[flag] = True

    with pytest.raises(ValueError):
        DecisionHumanReviewUnavailableResponse(**kwargs)


def test_default_decision_human_review_unavailable_response_validates() -> None:
    response = default_decision_human_review_unavailable_response()

    assert response.unavailable is True
    assert response.workflow_skeleton_only is True
    assert response.approval_allowed is False
    assert response.execution_allowed is False
