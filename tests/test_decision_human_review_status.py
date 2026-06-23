from __future__ import annotations

import pytest

from stark_terminal_core.decision_human_review.status import (
    DecisionHumanReviewStatusPlaceholder,
    default_decision_human_review_status_placeholder,
)
from stark_terminal_core.decision_human_review.workflow import DecisionReviewStatusKind


def _status_kwargs() -> dict[str, object]:
    return {
        "status_id": "status-test",
        "status_kind": DecisionReviewStatusKind.UNAVAILABLE,
        "message": "Status placeholder test",
    }


def test_valid_decision_human_review_status_placeholder() -> None:
    status = DecisionHumanReviewStatusPlaceholder(**_status_kwargs())

    assert status.workflow_active is False
    assert status.tasks_active is False
    assert status.approval_granted is False
    assert status.override_granted is False
    assert status.recommendation_generated is False
    assert status.decision_object_generated is False
    assert status.readiness_to_trade_generated is False
    assert status.execution_ready is False


def test_unknown_decision_human_review_status_kind_rejected() -> None:
    kwargs = _status_kwargs()
    kwargs["status_kind"] = DecisionReviewStatusKind.UNKNOWN

    with pytest.raises(ValueError):
        DecisionHumanReviewStatusPlaceholder(**kwargs)


@pytest.mark.parametrize(
    "flag",
    [
        "workflow_active",
        "tasks_active",
        "approval_granted",
        "override_granted",
        "recommendation_generated",
        "decision_object_generated",
        "readiness_to_trade_generated",
        "execution_ready",
    ],
)
def test_decision_human_review_status_rejects_active_or_generated_flags(flag: str) -> None:
    kwargs = _status_kwargs()
    kwargs[flag] = True

    with pytest.raises(ValueError):
        DecisionHumanReviewStatusPlaceholder(**kwargs)


def test_default_decision_human_review_status_placeholder_validates() -> None:
    status = default_decision_human_review_status_placeholder()

    assert status.workflow_active is False
    assert status.approval_granted is False
    assert status.execution_ready is False
