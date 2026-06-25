from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience_boundary.invariants import (
    RetailTraderExperienceBoundaryInvariantResult,
    evaluate_retail_trader_experience_boundary_invariants,
    reject_experience_active_ui_boundary_violation,
    reject_experience_broker_control_boundary_violation,
    reject_experience_execution_boundary_violation,
    reject_experience_readiness_to_trade_boundary_violation,
    reject_experience_recommendation_boundary_violation,
    reject_experience_suitability_profiling_boundary_violation,
)


def test_default_boundary_invariants_pass() -> None:
    result = evaluate_retail_trader_experience_boundary_invariants()

    assert result.passed is True
    assert result.blockers == []
    assert "retail-trader-experience-boundary" in result.checked_families
    assert "retail_trader_experience_boundary" in result.checked_families
    assert result.active_ui_allowed is False
    assert result.recommendations_allowed is False
    assert result.suitability_profiling_allowed is False
    assert result.broker_controls_allowed is False
    assert result.execution_allowed is False


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
        "suitability_profiling_allowed",
        "broker_controls_allowed",
        "execution_allowed",
        "approval_allowed",
        "override_allowed",
    ],
)
def test_invariant_result_cannot_allow_dangerous_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        RetailTraderExperienceBoundaryInvariantResult(
            result_id="unsafe",
            passed=False,
            checked_families=["retail_trader_experience_boundary"],
            blockers=["blocked"],
            **{field_name: True},
        )


def test_invariant_result_cannot_pass_with_blockers() -> None:
    with pytest.raises(ValidationError):
        RetailTraderExperienceBoundaryInvariantResult(
            result_id="unsafe",
            passed=True,
            checked_families=["retail_trader_experience_boundary"],
            blockers=["blocked"],
        )


@pytest.mark.parametrize(
    "factory",
    [
        reject_experience_active_ui_boundary_violation,
        reject_experience_recommendation_boundary_violation,
        reject_experience_execution_boundary_violation,
        reject_experience_broker_control_boundary_violation,
        reject_experience_readiness_to_trade_boundary_violation,
        reject_experience_suitability_profiling_boundary_violation,
    ],
)
def test_reject_helpers_return_blocked_results(factory) -> None:
    result = factory()

    assert result.passed is False
    assert result.blockers
    assert result.execution_allowed is False
    assert result.suitability_profiling_allowed is False
