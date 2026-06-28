from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.strategy_research_workspace_boundary.forbidden import (
    StrategyResearchBoundarySafetyLabel,
)
from stark_terminal_core.strategy_research_workspace_boundary.invariants import (
    StrategyResearchBoundaryInvariantResult,
    evaluate_strategy_research_boundary_invariants,
    reject_strategy_research_active_ui_boundary_violation,
    reject_strategy_research_backtesting_boundary_violation,
    reject_strategy_research_broker_control_boundary_violation,
    reject_strategy_research_execution_boundary_violation,
    reject_strategy_research_paper_parsing_boundary_violation,
    reject_strategy_research_readiness_to_trade_boundary_violation,
    reject_strategy_research_recommendation_boundary_violation,
    reject_strategy_research_strategy_generation_boundary_violation,
)


def test_strategy_research_boundary_default_invariants_pass() -> None:
    result = evaluate_strategy_research_boundary_invariants()

    assert result.passed is True
    assert result.blockers == []
    assert "strategy-research-workspace-boundary" in result.checked_families
    assert "strategy_research_workspace_boundary" in result.checked_families
    assert result.active_ui_allowed is False
    assert result.paper_parsing_allowed is False
    assert result.strategy_generation_allowed is False
    assert result.backtesting_allowed is False
    assert result.recommendations_allowed is False
    assert result.confidence_scoring_allowed is False
    assert result.decision_object_generation_allowed is False
    assert result.readiness_to_trade_allowed is False
    assert result.broker_controls_allowed is False
    assert result.execution_allowed is False


@pytest.mark.parametrize(
    "field_name",
    [
        "active_ui_allowed",
        "frontend_components_allowed",
        "desktop_components_allowed",
        "paper_ingestion_allowed",
        "paper_parsing_allowed",
        "strategy_generation_allowed",
        "strategy_code_generation_allowed",
        "backtesting_allowed",
        "optimization_allowed",
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
def test_strategy_research_boundary_invariant_rejects_dangerous_allow_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        StrategyResearchBoundaryInvariantResult(
            result_id="strategy-research-boundary-invariant-test-v1",
            passed=False,
            checked_families=["strategy_research_workspace_boundary"],
            **{field_name: True},
        )


def test_strategy_research_boundary_invariant_cannot_pass_with_blockers() -> None:
    with pytest.raises(ValidationError):
        StrategyResearchBoundaryInvariantResult(
            result_id="strategy-research-boundary-invariant-test-v1",
            passed=True,
            checked_families=["strategy_research_workspace_boundary"],
            blockers=["blocked"],
        )


def test_strategy_research_boundary_reject_helpers_return_blocked_safe_results() -> None:
    helpers = [
        reject_strategy_research_active_ui_boundary_violation,
        reject_strategy_research_paper_parsing_boundary_violation,
        reject_strategy_research_strategy_generation_boundary_violation,
        reject_strategy_research_backtesting_boundary_violation,
        reject_strategy_research_recommendation_boundary_violation,
        reject_strategy_research_execution_boundary_violation,
        reject_strategy_research_broker_control_boundary_violation,
        reject_strategy_research_readiness_to_trade_boundary_violation,
    ]

    for helper in helpers:
        result = helper()
        assert result.passed is False
        assert result.blockers
        assert result.safety_label == StrategyResearchBoundarySafetyLabel.BLOCKED
        assert result.active_ui_allowed is False
        assert result.paper_parsing_allowed is False
        assert result.strategy_generation_allowed is False
        assert result.backtesting_allowed is False
        assert result.recommendations_allowed is False
        assert result.execution_allowed is False
