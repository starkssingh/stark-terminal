from __future__ import annotations

import pytest

from stark_terminal_core.decision_human_review.workflow import (
    DecisionHumanReviewWorkflowContract,
    DecisionReviewQueueKind,
    DecisionReviewTaskKind,
    DecisionReviewerRoleKind,
    default_decision_human_review_workflow_contract,
)


def _workflow_kwargs() -> dict[str, object]:
    return {
        "workflow_id": "workflow-test",
        "name": "Workflow Test",
        "task_kinds": [DecisionReviewTaskKind.EVIDENCE_REVIEW],
        "reviewer_roles": [DecisionReviewerRoleKind.HUMAN_OPERATOR],
        "queue_kinds": [DecisionReviewQueueKind.PLACEHOLDER_QUEUE],
        "forbidden_outputs": [
            "active workflow",
            "task assignment",
            "reviewer auth",
            "notifications",
            "approval",
            "override",
            "recommendation",
            "action",
            "confidence",
            "DecisionObject",
            "readiness-to-trade",
            "execution",
        ],
    }


def test_valid_decision_human_review_workflow_contract() -> None:
    contract = DecisionHumanReviewWorkflowContract(**_workflow_kwargs())

    assert contract.active_workflow is False
    assert contract.task_assignment_allowed is False
    assert contract.reviewer_auth_allowed is False
    assert contract.notifications_allowed is False
    assert contract.approval_allowed is False
    assert contract.override_allowed is False
    assert contract.recommendations_allowed is False
    assert contract.action_generation_allowed is False
    assert contract.confidence_scoring_allowed is False
    assert contract.decision_object_generation_allowed is False
    assert contract.readiness_to_trade_allowed is False
    assert contract.execution_allowed is False
    assert contract.returns_unavailable_by_default is True


@pytest.mark.parametrize(
    "flag",
    [
        "active_workflow",
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
def test_decision_human_review_workflow_rejects_dangerous_flags(flag: str) -> None:
    kwargs = _workflow_kwargs()
    kwargs[flag] = True

    with pytest.raises(ValueError):
        DecisionHumanReviewWorkflowContract(**kwargs)


def test_decision_human_review_workflow_enforces_unavailable_by_default() -> None:
    kwargs = _workflow_kwargs()
    kwargs["returns_unavailable_by_default"] = False

    with pytest.raises(ValueError):
        DecisionHumanReviewWorkflowContract(**kwargs)


def test_default_decision_human_review_workflow_contract_validates() -> None:
    contract = default_decision_human_review_workflow_contract()

    assert contract.task_kinds
    assert contract.reviewer_roles
    assert contract.queue_kinds
    text = " ".join(contract.forbidden_outputs).lower()
    for phrase in [
        "active workflow",
        "task assignment",
        "reviewer auth",
        "notifications",
        "approval",
        "override",
        "recommendation",
        "action",
        "confidence",
        "decisionobject",
        "readiness-to-trade",
        "execution",
    ]:
        assert phrase in text
