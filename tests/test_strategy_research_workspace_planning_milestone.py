from __future__ import annotations

from stark_terminal_core.strategy_research_workspace.artifacts import (
    default_strategy_research_artifact_placeholders,
)
from stark_terminal_core.strategy_research_workspace.datasets import (
    default_strategy_research_dataset_reference_placeholders,
)
from stark_terminal_core.strategy_research_workspace.experiments import (
    default_strategy_research_experiment_placeholders,
)
from stark_terminal_core.strategy_research_workspace.interactions import (
    StrategyResearchForbiddenInteractionKind,
    default_strategy_research_forbidden_interactions,
)
from stark_terminal_core.strategy_research_workspace.papers import (
    default_strategy_research_paper_reference_placeholders,
)
from stark_terminal_core.strategy_research_workspace.planning import (
    default_strategy_research_workspace_planning_contract,
)
from stark_terminal_core.strategy_research_workspace.readiness import (
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
from stark_terminal_core.strategy_research_workspace.strategies import (
    default_strategy_research_hypothesis_placeholders,
)
from stark_terminal_core.strategy_research_workspace.workspaces import (
    default_strategy_research_workspace_placeholders,
)


def test_strategy_research_workspace_planning_layer_remains_placeholder_only() -> None:
    plan = default_strategy_research_workspace_planning_contract()
    workspaces = default_strategy_research_workspace_placeholders()
    artifacts = default_strategy_research_artifact_placeholders()
    papers = default_strategy_research_paper_reference_placeholders()
    hypotheses = default_strategy_research_hypothesis_placeholders()
    datasets = default_strategy_research_dataset_reference_placeholders()
    experiments = default_strategy_research_experiment_placeholders()

    assert plan.returns_unavailable_by_default is True
    assert workspaces and all(workspace.planning_only and not workspace.active_ui for workspace in workspaces)
    assert artifacts and all(artifact.planning_only and not artifact.validated for artifact in artifacts)
    assert papers and all(paper.planning_only and not paper.paper_parsed for paper in papers)
    assert hypotheses and all(hypothesis.planning_only and not hypothesis.generated_strategy for hypothesis in hypotheses)
    assert datasets and all(not dataset.live_data and not dataset.real_market_data for dataset in datasets)
    assert experiments and all(not experiment.executable and not experiment.backtest_executable for experiment in experiments)


def test_strategy_research_workspace_forbidden_interactions_remain_complete() -> None:
    kinds = {interaction.kind for interaction in default_strategy_research_forbidden_interactions()}

    for kind in [
        StrategyResearchForbiddenInteractionKind.PAPER_INGESTION,
        StrategyResearchForbiddenInteractionKind.PAPER_PARSING,
        StrategyResearchForbiddenInteractionKind.STRATEGY_GENERATION,
        StrategyResearchForbiddenInteractionKind.STRATEGY_CODE_GENERATION,
        StrategyResearchForbiddenInteractionKind.BACKTESTING,
        StrategyResearchForbiddenInteractionKind.OPTIMIZATION,
        StrategyResearchForbiddenInteractionKind.RECOMMENDATION_GENERATION,
        StrategyResearchForbiddenInteractionKind.ACTION_GENERATION,
        StrategyResearchForbiddenInteractionKind.CONFIDENCE_SCORING,
        StrategyResearchForbiddenInteractionKind.DECISION_OBJECT_GENERATION,
        StrategyResearchForbiddenInteractionKind.READINESS_TO_TRADE,
        StrategyResearchForbiddenInteractionKind.BROKER_CONTROL,
        StrategyResearchForbiddenInteractionKind.EXECUTION,
    ]:
        assert kind in kinds


def test_strategy_research_workspace_readiness_helpers_fail_closed() -> None:
    plan = default_strategy_research_workspace_planning_contract()
    policy = default_strategy_research_safety_policy()
    safety_result = evaluate_strategy_research_plan_safety(plan, policy)
    report = build_strategy_research_workspace_readiness_report(
        plan,
        default_strategy_research_workspace_placeholders(),
        default_strategy_research_artifact_placeholders(),
        default_strategy_research_paper_reference_placeholders(),
        default_strategy_research_hypothesis_placeholders(),
        default_strategy_research_dataset_reference_placeholders(),
        default_strategy_research_experiment_placeholders(),
        default_strategy_research_forbidden_interactions(),
        safety_result,
    )

    assert strategy_research_ready_for_active_ui(report) is False
    assert strategy_research_ready_for_strategy_generation(report) is False
    assert strategy_research_ready_for_backtesting(report) is False
    assert strategy_research_ready_for_recommendations(report) is False
    assert strategy_research_ready_for_execution(report) is False
    assert report.ready_for_broker_controls is False
