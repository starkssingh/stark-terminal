from __future__ import annotations

import pytest

from stark_terminal_core.decision_human_review.queues import (
    DecisionReviewQueuePlaceholder,
    default_decision_review_queue_placeholders,
)
from stark_terminal_core.decision_human_review.workflow import DecisionReviewQueueKind


def _queue_kwargs() -> dict[str, object]:
    return {
        "queue_id": "queue-test",
        "queue_kind": DecisionReviewQueueKind.PLACEHOLDER_QUEUE,
        "name": "Queue Test",
        "description": "Queue placeholder test",
    }


def test_valid_decision_review_queue_placeholder() -> None:
    queue = DecisionReviewQueuePlaceholder(**_queue_kwargs())

    assert queue.active_queue is False
    assert queue.persisted is False
    assert queue.task_assignment_allowed is False
    assert queue.notifications_allowed is False
    assert queue.approval_allowed is False
    assert queue.override_allowed is False
    assert queue.execution_allowed is False


def test_unknown_decision_review_queue_kind_rejected() -> None:
    kwargs = _queue_kwargs()
    kwargs["queue_kind"] = DecisionReviewQueueKind.UNKNOWN

    with pytest.raises(ValueError):
        DecisionReviewQueuePlaceholder(**kwargs)


@pytest.mark.parametrize(
    "flag",
    [
        "active_queue",
        "persisted",
        "task_assignment_allowed",
        "notifications_allowed",
        "approval_allowed",
        "override_allowed",
        "execution_allowed",
    ],
)
def test_decision_review_queue_rejects_active_or_allowed_flags(flag: str) -> None:
    kwargs = _queue_kwargs()
    kwargs[flag] = True

    with pytest.raises(ValueError):
        DecisionReviewQueuePlaceholder(**kwargs)


def test_default_decision_review_queue_placeholders_validate() -> None:
    queues = default_decision_review_queue_placeholders()

    assert queues
    assert all(queue.active_queue is False for queue in queues)
    assert all(queue.persisted is False for queue in queues)
    assert all(queue.task_assignment_allowed is False for queue in queues)
