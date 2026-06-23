from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_safety.approval import (
    DecisionApprovalPlaceholder,
    default_decision_approval_placeholders,
    evaluate_decision_approval_placeholders,
)
from stark_terminal_core.decision_safety.guardrails import DecisionApprovalPlaceholderStatus


def test_valid_approval_placeholder_is_inactive() -> None:
    placeholder = DecisionApprovalPlaceholder(
        approval_id="approval-1",
        title="Approval Placeholder",
        description="Inactive approval placeholder.",
    )

    assert placeholder.status == DecisionApprovalPlaceholderStatus.PLACEHOLDER_ONLY
    assert placeholder.approval_granted is False
    assert placeholder.active_workflow is False
    assert placeholder.grants_recommendations is False
    assert placeholder.grants_action_generation is False
    assert placeholder.grants_confidence_scoring is False
    assert placeholder.grants_decision_object_generation is False
    assert placeholder.grants_execution is False


def test_approval_placeholder_rejects_active_approval_or_grants() -> None:
    for field in [
        "approval_granted",
        "active_workflow",
        "grants_recommendations",
        "grants_action_generation",
        "grants_confidence_scoring",
        "grants_decision_object_generation",
        "grants_execution",
    ]:
        with pytest.raises(ValidationError):
            DecisionApprovalPlaceholder(
                approval_id="approval-1",
                title="Approval Placeholder",
                description="Unsafe approval placeholder.",
                **{field: True},
            )

    with pytest.raises(ValidationError):
        DecisionApprovalPlaceholder(
            approval_id="approval-1",
            title="Approval Placeholder",
            description="Unknown status.",
            status=DecisionApprovalPlaceholderStatus.UNKNOWN,
        )


def test_default_approval_placeholders_are_not_active_approvals() -> None:
    placeholders = default_decision_approval_placeholders()

    assert placeholders
    assert evaluate_decision_approval_placeholders(placeholders) == []
    assert all(placeholder.approval_granted is False for placeholder in placeholders)
    assert all(placeholder.active_workflow is False for placeholder in placeholders)
