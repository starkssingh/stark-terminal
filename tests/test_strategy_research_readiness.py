import pytest

from stark_terminal_core.strategy_research_workspace.artifacts import default_strategy_research_artifact_placeholders
from stark_terminal_core.strategy_research_workspace.datasets import default_strategy_research_dataset_reference_placeholders
from stark_terminal_core.strategy_research_workspace.experiments import default_strategy_research_experiment_placeholders
from stark_terminal_core.strategy_research_workspace.interactions import default_strategy_research_forbidden_interactions
from stark_terminal_core.strategy_research_workspace.papers import default_strategy_research_paper_reference_placeholders
from stark_terminal_core.strategy_research_workspace.planning import default_strategy_research_workspace_planning_contract
from stark_terminal_core.strategy_research_workspace.readiness import (
    StrategyResearchWorkspaceReadinessReport,
    build_strategy_research_workspace_readiness_report,
    strategy_research_ready_for_active_ui,
    strategy_research_ready_for_backtesting,
    strategy_research_ready_for_execution,
    strategy_research_ready_for_recommendations,
    strategy_research_ready_for_strategy_generation,
)
from stark_terminal_core.strategy_research_workspace.safety import (
    default_strategy_research_safety_policy,
    evaluate_strategy_research_plan_safety,
)
from stark_terminal_core.strategy_research_workspace.strategies import default_strategy_research_hypothesis_placeholders
from stark_terminal_core.strategy_research_workspace.workspaces import default_strategy_research_workspace_placeholders


def _readiness_report():
    plan = default_strategy_research_workspace_planning_contract()
    policy = default_strategy_research_safety_policy()
    return build_strategy_research_workspace_readiness_report(
        plan,
        default_strategy_research_workspace_placeholders(),
        default_strategy_research_artifact_placeholders(),
        default_strategy_research_paper_reference_placeholders(),
        default_strategy_research_hypothesis_placeholders(),
        default_strategy_research_dataset_reference_placeholders(),
        default_strategy_research_experiment_placeholders(),
        default_strategy_research_forbidden_interactions(),
        evaluate_strategy_research_plan_safety(plan, policy),
    )


def test_strategy_research_readiness_report_validates_and_blocks_active_readiness():
    report = _readiness_report()

    assert report.ready_for_api_contract_skeleton is True
    assert report.ready_for_display_contract_skeleton is True
    assert report.ready_for_active_ui is False
    assert report.ready_for_strategy_generation is False
    assert report.ready_for_backtesting is False
    assert report.ready_for_recommendations is False
    assert report.ready_for_broker_controls is False
    assert report.ready_for_readiness_to_trade is False
    assert report.ready_for_execution is False

    for helper in [
        strategy_research_ready_for_active_ui,
        strategy_research_ready_for_strategy_generation,
        strategy_research_ready_for_backtesting,
        strategy_research_ready_for_recommendations,
        strategy_research_ready_for_execution,
    ]:
        assert helper(report) is False


def test_strategy_research_readiness_rejects_dangerous_readiness_flags():
    payload = _readiness_report().model_dump()
    payload["ready_for_execution"] = True

    with pytest.raises(ValueError):
        StrategyResearchWorkspaceReadinessReport(**payload)
