from __future__ import annotations

import pytest

from stark_terminal_core.decision_human_review.tasks import (
    DecisionReviewTaskPlaceholder,
    default_decision_review_task_placeholders,
)
from stark_terminal_core.decision_human_review.workflow import DecisionReviewTaskKind


def _task_kwargs() -> dict[str, object]:
    return {
        "task_id": "task-test",
        "task_kind": DecisionReviewTaskKind.EVIDENCE_REVIEW,
        "title": "Task Test",
        "description": "Task placeholder test",
    }


def test_valid_decision_review_task_placeholder() -> None:
    task = DecisionReviewTaskPlaceholder(**_task_kwargs())

    assert task.assigned is False
    assert task.active is False
    assert task.completed is False
    assert task.approval_granted is False
    assert task.override_granted is False
    assert task.recommendation_generated is False
    assert task.action_generated is False
    assert task.confidence_generated is False
    assert task.decision_object_generated is False
    assert task.readiness_to_trade_generated is False
    assert task.execution_ready is False


def test_unknown_decision_review_task_kind_rejected() -> None:
    kwargs = _task_kwargs()
    kwargs["task_kind"] = DecisionReviewTaskKind.UNKNOWN

    with pytest.raises(ValueError):
        DecisionReviewTaskPlaceholder(**kwargs)


@pytest.mark.parametrize(
    "flag",
    [
        "assigned",
        "active",
        "completed",
        "approval_granted",
        "override_granted",
        "recommendation_generated",
        "action_generated",
        "confidence_generated",
        "decision_object_generated",
        "readiness_to_trade_generated",
        "execution_ready",
    ],
)
def test_decision_review_task_rejects_active_or_generated_flags(flag: str) -> None:
    kwargs = _task_kwargs()
    kwargs[flag] = True

    with pytest.raises(ValueError):
        DecisionReviewTaskPlaceholder(**kwargs)


def test_default_decision_review_task_placeholders_validate() -> None:
    tasks = default_decision_review_task_placeholders()

    assert tasks
    assert all(task.assigned is False for task in tasks)
    assert all(task.active is False for task in tasks)
    assert all(task.approval_granted is False for task in tasks)
