import pytest

from stark_terminal_core.strategy_research_workspace.artifacts import default_strategy_research_artifact_placeholders
from stark_terminal_core.strategy_research_workspace.experiments import default_strategy_research_experiment_placeholders
from stark_terminal_core.strategy_research_workspace.papers import default_strategy_research_paper_reference_placeholders
from stark_terminal_core.strategy_research_workspace.planning import default_strategy_research_workspace_planning_contract
from stark_terminal_core.strategy_research_workspace.safety import (
    StrategyResearchSafetyPolicy,
    default_strategy_research_safety_policy,
    evaluate_strategy_research_artifact_safety,
    evaluate_strategy_research_experiment_safety,
    evaluate_strategy_research_hypothesis_safety,
    evaluate_strategy_research_paper_reference_safety,
    evaluate_strategy_research_plan_safety,
    evaluate_strategy_research_workspace_safety,
    reject_research_as_active_ui,
    reject_research_as_backtest,
    reject_research_as_execution_surface,
    reject_research_as_recommendation,
    reject_research_as_strategy_generation,
)
from stark_terminal_core.strategy_research_workspace.strategies import default_strategy_research_hypothesis_placeholders
from stark_terminal_core.strategy_research_workspace.workspaces import default_strategy_research_workspace_placeholders


def test_default_strategy_research_safety_policy_forbids_dangerous_behavior():
    policy = default_strategy_research_safety_policy()

    assert policy.allow_active_ui is False
    assert policy.allow_frontend_components is False
    assert policy.allow_desktop_components is False
    assert policy.allow_paper_ingestion is False
    assert policy.allow_paper_parsing is False
    assert policy.allow_strategy_generation is False
    assert policy.allow_strategy_code_generation is False
    assert policy.allow_backtesting is False
    assert policy.allow_optimization is False
    assert policy.allow_recommendations is False
    assert policy.allow_action_generation is False
    assert policy.allow_confidence_scoring is False
    assert policy.allow_decision_object_generation is False
    assert policy.allow_readiness_to_trade is False
    assert policy.allow_broker_controls is False
    assert policy.allow_execution is False
    assert policy.allow_approval is False
    assert policy.allow_override is False
    assert policy.require_planning_only is True


@pytest.mark.parametrize(
    "field",
    [
        "allow_active_ui",
        "allow_paper_ingestion",
        "allow_paper_parsing",
        "allow_strategy_generation",
        "allow_strategy_code_generation",
        "allow_backtesting",
        "allow_optimization",
        "allow_recommendations",
        "allow_action_generation",
        "allow_confidence_scoring",
        "allow_decision_object_generation",
        "allow_readiness_to_trade",
        "allow_broker_controls",
        "allow_execution",
        "allow_approval",
        "allow_override",
    ],
)
def test_strategy_research_safety_policy_rejects_unsafe_flags(field):
    payload = default_strategy_research_safety_policy().model_dump()
    payload[field] = True

    with pytest.raises(ValueError):
        StrategyResearchSafetyPolicy(**payload)


def test_strategy_research_safety_evaluators_accept_safe_defaults_and_reject_unsafe_copies():
    policy = default_strategy_research_safety_policy()
    plan = default_strategy_research_workspace_planning_contract()
    workspaces = default_strategy_research_workspace_placeholders()
    artifacts = default_strategy_research_artifact_placeholders()
    papers = default_strategy_research_paper_reference_placeholders()
    hypotheses = default_strategy_research_hypothesis_placeholders()
    experiments = default_strategy_research_experiment_placeholders()

    assert evaluate_strategy_research_plan_safety(plan, policy).safe is True
    assert evaluate_strategy_research_workspace_safety(workspaces, policy).safe is True
    assert evaluate_strategy_research_artifact_safety(artifacts, policy).safe is True
    assert evaluate_strategy_research_paper_reference_safety(papers, policy).safe is True
    assert evaluate_strategy_research_hypothesis_safety(hypotheses, policy).safe is True
    assert evaluate_strategy_research_experiment_safety(experiments, policy).safe is True

    assert evaluate_strategy_research_plan_safety(plan.model_copy(update={"strategy_generation_allowed": True}), policy).safe is False
    assert evaluate_strategy_research_workspace_safety([workspaces[0].model_copy(update={"active_ui": True})], policy).safe is False
    assert evaluate_strategy_research_artifact_safety([artifacts[0].model_copy(update={"validated": True})], policy).safe is False
    assert evaluate_strategy_research_paper_reference_safety([papers[0].model_copy(update={"paper_parsed": True})], policy).safe is False
    assert evaluate_strategy_research_hypothesis_safety([hypotheses[0].model_copy(update={"generated_strategy": True})], policy).safe is False
    assert evaluate_strategy_research_experiment_safety([experiments[0].model_copy(update={"backtest_executable": True})], policy).safe is False


def test_strategy_research_reject_helpers_return_blocking_results():
    results = [
        reject_research_as_active_ui(),
        reject_research_as_strategy_generation(),
        reject_research_as_backtest(),
        reject_research_as_recommendation(),
        reject_research_as_execution_surface(),
    ]

    assert all(result.safe is False for result in results)
    assert all(result.planning_only is True for result in results)
    assert all(result.execution_allowed is False for result in results)
