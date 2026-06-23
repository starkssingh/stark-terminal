from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_dashboard_boundary.invariants import (
    RetailDashboardBoundaryInvariantResult,
    evaluate_retail_dashboard_boundary_invariants,
    reject_dashboard_active_ui_boundary_violation,
    reject_dashboard_broker_control_boundary_violation,
    reject_dashboard_execution_boundary_violation,
    reject_dashboard_readiness_to_trade_boundary_violation,
    reject_dashboard_recommendation_boundary_violation,
)


def test_default_retail_dashboard_boundary_invariants_pass() -> None:
    result = evaluate_retail_dashboard_boundary_invariants()

    assert result.passed is True
    assert result.blockers == []
    assert "retail-dashboard" in result.checked_families
    assert "retail_dashboard_boundary" in result.checked_families
    assert result.active_ui_allowed is False
    assert result.frontend_components_allowed is False
    assert result.desktop_components_allowed is False
    assert result.recommendations_allowed is False
    assert result.action_generation_allowed is False
    assert result.confidence_scoring_allowed is False
    assert result.decision_object_generation_allowed is False
    assert result.readiness_to_trade_allowed is False
    assert result.broker_controls_allowed is False
    assert result.execution_allowed is False
    assert result.approval_allowed is False
    assert result.override_allowed is False


@pytest.mark.parametrize(
    "field_name",
    [
        "active_ui_allowed",
        "frontend_components_allowed",
        "desktop_components_allowed",
        "recommendations_allowed",
        "action_generation_allowed",
        "confidence_scoring_allowed",
        "decision_object_generation_allowed",
        "readiness_to_trade_allowed",
        "broker_controls_allowed",
        "execution_allowed",
        "approval_allowed",
        "override_allowed",
    ],
)
def test_invariant_result_cannot_allow_dangerous_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        RetailDashboardBoundaryInvariantResult(
            result_id="bad-result",
            passed=False,
            checked_families=["retail_dashboard_boundary"],
            blockers=["blocked"],
            **{field_name: True},
        )


def test_invariant_result_cannot_pass_with_blockers() -> None:
    with pytest.raises(ValidationError):
        RetailDashboardBoundaryInvariantResult(
            result_id="bad-result",
            passed=True,
            checked_families=["retail_dashboard_boundary"],
            blockers=["blocked"],
        )


@pytest.mark.parametrize(
    "factory",
    [
        reject_dashboard_active_ui_boundary_violation,
        reject_dashboard_recommendation_boundary_violation,
        reject_dashboard_execution_boundary_violation,
        reject_dashboard_broker_control_boundary_violation,
        reject_dashboard_readiness_to_trade_boundary_violation,
    ],
)
def test_boundary_rejection_helpers_return_blocked_results(factory: object) -> None:
    result = factory()  # type: ignore[operator]

    assert result.passed is False
    assert result.blockers
    assert result.execution_allowed is False
    assert result.broker_controls_allowed is False
    assert result.recommendations_allowed is False
