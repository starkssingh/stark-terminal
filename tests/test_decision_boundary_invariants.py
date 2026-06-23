from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_boundary.invariants import (
    DecisionBoundaryInvariantResult,
    evaluate_decision_boundary_invariants,
    reject_active_ui_workflow_boundary_violation,
    reject_approval_override_boundary_violation,
    reject_execution_boundary_violation,
    reject_readiness_to_trade_boundary_violation,
    reject_recommendation_boundary_violation,
)


def test_default_boundary_invariants_pass() -> None:
    result = evaluate_decision_boundary_invariants()

    assert result.passed is True
    assert result.blockers == []
    assert result.checked_families
    assert result.recommendations_allowed is False
    assert result.action_generation_allowed is False
    assert result.confidence_scoring_allowed is False
    assert result.decision_object_generation_allowed is False
    assert result.execution_allowed is False
    assert result.approval_allowed is False
    assert result.override_allowed is False
    assert result.active_ui_allowed is False
    assert result.active_workflow_allowed is False
    assert result.readiness_to_trade_allowed is False


@pytest.mark.parametrize(
    "field_name",
    [
        "recommendations_allowed",
        "action_generation_allowed",
        "confidence_scoring_allowed",
        "decision_object_generation_allowed",
        "execution_allowed",
        "approval_allowed",
        "override_allowed",
        "active_ui_allowed",
        "active_workflow_allowed",
        "readiness_to_trade_allowed",
    ],
)
def test_boundary_invariant_result_rejects_dangerous_allowed_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        DecisionBoundaryInvariantResult(
            result_id="invariant-test",
            passed=False,
            checked_families=["decision_boundary"],
            **{field_name: True},
        )


def test_boundary_invariant_result_cannot_pass_with_blockers() -> None:
    with pytest.raises(ValidationError):
        DecisionBoundaryInvariantResult(
            result_id="invariant-test",
            passed=True,
            checked_families=["decision_boundary"],
            blockers=["blocked"],
        )


def test_rejection_helpers_return_blocked_results() -> None:
    results = [
        reject_recommendation_boundary_violation(),
        reject_execution_boundary_violation(),
        reject_approval_override_boundary_violation(),
        reject_active_ui_workflow_boundary_violation(),
        reject_readiness_to_trade_boundary_violation(),
    ]

    for result in results:
        assert result.passed is False
        assert result.blockers
        assert result.execution_allowed is False
        assert result.approval_allowed is False
        assert result.override_allowed is False
        assert result.active_ui_allowed is False
        assert result.active_workflow_allowed is False
        assert result.readiness_to_trade_allowed is False
