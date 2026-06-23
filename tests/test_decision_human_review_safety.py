from __future__ import annotations

import pytest

from stark_terminal_core.decision_human_review.roles import (
    DecisionReviewerRolePlaceholder,
    default_decision_reviewer_role_placeholders,
)
from stark_terminal_core.decision_human_review.safety import (
    DecisionHumanReviewSafetyPolicy,
    default_decision_human_review_safety_policy,
    evaluate_decision_human_review_workflow_safety,
    evaluate_decision_review_tasks_safety,
    evaluate_decision_reviewer_roles_safety,
    reject_review_as_approval,
    reject_review_as_override,
    reject_review_as_recommendation,
)
from stark_terminal_core.decision_human_review.tasks import (
    DecisionReviewTaskPlaceholder,
    default_decision_review_task_placeholders,
)
from stark_terminal_core.decision_human_review.workflow import (
    DecisionHumanReviewWorkflowContract,
    DecisionReviewTaskKind,
    DecisionReviewerRoleKind,
    default_decision_human_review_workflow_contract,
)


def test_default_decision_human_review_safety_policy_forbids_dangerous_capabilities() -> None:
    policy = default_decision_human_review_safety_policy()

    assert policy.allow_active_workflow is False
    assert policy.allow_task_assignment is False
    assert policy.allow_reviewer_auth is False
    assert policy.allow_notifications is False
    assert policy.allow_approval is False
    assert policy.allow_override is False
    assert policy.allow_recommendations is False
    assert policy.allow_action_generation is False
    assert policy.allow_confidence_scoring is False
    assert policy.allow_decision_object_generation is False
    assert policy.allow_readiness_to_trade is False
    assert policy.allow_execution is False
    assert policy.require_workflow_skeleton_only is True


@pytest.mark.parametrize(
    "flag",
    [
        "allow_active_workflow",
        "allow_task_assignment",
        "allow_reviewer_auth",
        "allow_notifications",
        "allow_approval",
        "allow_override",
        "allow_recommendations",
        "allow_action_generation",
        "allow_confidence_scoring",
        "allow_decision_object_generation",
        "allow_readiness_to_trade",
        "allow_execution",
    ],
)
def test_decision_human_review_safety_policy_rejects_unsafe_flags(flag: str) -> None:
    kwargs = {"policy_id": "policy-test", "name": "Policy Test", flag: True}

    with pytest.raises(ValueError):
        DecisionHumanReviewSafetyPolicy(**kwargs)


def test_workflow_safety_rejects_unsafe_workflow_constructed_for_audit() -> None:
    workflow_data = default_decision_human_review_workflow_contract().model_dump()
    workflow_data["active_workflow"] = True
    unsafe = DecisionHumanReviewWorkflowContract.model_construct(**workflow_data)
    result = evaluate_decision_human_review_workflow_safety(
        unsafe,
        default_decision_human_review_safety_policy(),
    )

    assert result.safe is False
    assert any("active" in reason for reason in result.reasons)
    assert result.approval_granted is False
    assert result.execution_allowed is False


def test_task_safety_rejects_unsafe_task_constructed_for_audit() -> None:
    task_data = default_decision_review_task_placeholders()[0].model_dump()
    task_data["assigned"] = True
    unsafe = DecisionReviewTaskPlaceholder.model_construct(**task_data)
    result = evaluate_decision_review_tasks_safety(
        [unsafe],
        default_decision_human_review_safety_policy(),
    )

    assert result.safe is False
    assert any("assigned" in reason for reason in result.reasons)


def test_role_safety_rejects_unsafe_role_constructed_for_audit() -> None:
    role_data = default_decision_reviewer_role_placeholders()[0].model_dump()
    role_data["can_approve"] = True
    unsafe = DecisionReviewerRolePlaceholder.model_construct(**role_data)
    result = evaluate_decision_reviewer_roles_safety(
        [unsafe],
        default_decision_human_review_safety_policy(),
    )

    assert result.safe is False
    assert any("approve" in reason for reason in result.reasons)


def test_safety_evaluators_accept_safe_placeholders_as_skeleton_only() -> None:
    policy = default_decision_human_review_safety_policy()

    workflow_result = evaluate_decision_human_review_workflow_safety(
        default_decision_human_review_workflow_contract(),
        policy,
    )
    task_result = evaluate_decision_review_tasks_safety(default_decision_review_task_placeholders(), policy)
    role_result = evaluate_decision_reviewer_roles_safety(default_decision_reviewer_role_placeholders(), policy)

    assert workflow_result.safe is True
    assert task_result.safe is True
    assert role_result.safe is True


def test_review_rejection_helpers_return_blocking_non_approval_results() -> None:
    approval = reject_review_as_approval()
    override = reject_review_as_override()
    recommendation = reject_review_as_recommendation()

    for result in [approval, override, recommendation]:
        assert result.safe is False
        assert result.workflow_skeleton_only is True
        assert result.approval_granted is False
        assert result.override_granted is False
        assert result.execution_allowed is False


def test_model_construct_helpers_have_expected_kinds_for_audit() -> None:
    task = DecisionReviewTaskPlaceholder.model_construct(
        task_id="audit-task",
        task_kind=DecisionReviewTaskKind.EVIDENCE_REVIEW,
        title="Audit",
        description="Audit",
        assigned=False,
    )
    role = DecisionReviewerRolePlaceholder.model_construct(
        role_id="audit-role",
        role_kind=DecisionReviewerRoleKind.HUMAN_OPERATOR,
        display_name="Audit",
        description="Audit",
        can_approve=False,
    )
    assert task.task_kind == DecisionReviewTaskKind.EVIDENCE_REVIEW
    assert role.role_kind == DecisionReviewerRoleKind.HUMAN_OPERATOR
