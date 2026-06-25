import pytest

from stark_terminal_core.strategy_research_workspace_display.artifacts import (
    default_strategy_research_workspace_display_artifact_placeholders,
)
from stark_terminal_core.strategy_research_workspace_display.contracts import (
    default_strategy_research_workspace_display_contract_metadata,
)
from stark_terminal_core.strategy_research_workspace_display.experiments import (
    default_strategy_research_workspace_display_experiment_placeholders,
)
from stark_terminal_core.strategy_research_workspace_display.hypotheses import (
    default_strategy_research_workspace_display_hypothesis_placeholders,
)
from stark_terminal_core.strategy_research_workspace_display.papers import (
    default_strategy_research_workspace_display_paper_placeholders,
)
from stark_terminal_core.strategy_research_workspace_display.safety import (
    StrategyResearchWorkspaceDisplaySafetyPolicy,
    default_strategy_research_workspace_display_safety_policy,
    evaluate_strategy_research_display_artifact_safety,
    evaluate_strategy_research_display_contract_safety,
    evaluate_strategy_research_display_experiment_safety,
    evaluate_strategy_research_display_hypothesis_safety,
    evaluate_strategy_research_display_paper_safety,
    evaluate_strategy_research_display_workspace_safety,
    reject_display_as_active_ui,
    reject_display_as_backtest,
    reject_display_as_execution_surface,
    reject_display_as_recommendation,
    reject_display_as_strategy_generation,
)
from stark_terminal_core.strategy_research_workspace_display.workspaces import (
    default_strategy_research_workspace_display_workspace_placeholders,
)


SAFETY_FLAGS = [
    "allow_active_ui",
    "allow_frontend_components",
    "allow_desktop_components",
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
]


def test_default_strategy_research_workspace_display_safety_policy_forbids_dangerous_flags():
    policy = default_strategy_research_workspace_display_safety_policy()

    assert isinstance(policy, StrategyResearchWorkspaceDisplaySafetyPolicy)
    for field in SAFETY_FLAGS:
        assert getattr(policy, field) is False
    assert policy.require_display_contract_only is True


@pytest.mark.parametrize("field", SAFETY_FLAGS)
def test_strategy_research_workspace_display_safety_policy_rejects_unsafe_flags(field):
    with pytest.raises(ValueError):
        StrategyResearchWorkspaceDisplaySafetyPolicy(
            policy_id="unsafe-policy",
            name="Unsafe Policy",
            **{field: True},
        )


def test_strategy_research_workspace_display_safety_accepts_safe_defaults():
    policy = default_strategy_research_workspace_display_safety_policy()

    assert evaluate_strategy_research_display_contract_safety(
        default_strategy_research_workspace_display_contract_metadata(), policy
    ).safe
    assert evaluate_strategy_research_display_workspace_safety(
        default_strategy_research_workspace_display_workspace_placeholders(), policy
    ).safe
    assert evaluate_strategy_research_display_artifact_safety(
        default_strategy_research_workspace_display_artifact_placeholders(), policy
    ).safe
    assert evaluate_strategy_research_display_paper_safety(
        default_strategy_research_workspace_display_paper_placeholders(), policy
    ).safe
    assert evaluate_strategy_research_display_hypothesis_safety(
        default_strategy_research_workspace_display_hypothesis_placeholders(), policy
    ).safe
    assert evaluate_strategy_research_display_experiment_safety(
        default_strategy_research_workspace_display_experiment_placeholders(), policy
    ).safe


def test_strategy_research_workspace_display_safety_rejects_unsafe_objects():
    policy = default_strategy_research_workspace_display_safety_policy()
    unsafe_contract = default_strategy_research_workspace_display_contract_metadata().model_copy(
        update={"strategy_generation_allowed": True}
    )
    unsafe_workspace = default_strategy_research_workspace_display_workspace_placeholders()[0].model_copy(
        update={"active_ui": True}
    )
    unsafe_artifact = default_strategy_research_workspace_display_artifact_placeholders()[0].model_copy(
        update={"strategy_ready": True}
    )
    unsafe_paper = default_strategy_research_workspace_display_paper_placeholders()[0].model_copy(
        update={"paper_parsed": True}
    )
    unsafe_hypothesis = default_strategy_research_workspace_display_hypothesis_placeholders()[0].model_copy(
        update={"generated_strategy": True}
    )
    unsafe_experiment = default_strategy_research_workspace_display_experiment_placeholders()[0].model_copy(
        update={"executable": True}
    )

    assert not evaluate_strategy_research_display_contract_safety(unsafe_contract, policy).safe
    assert not evaluate_strategy_research_display_workspace_safety([unsafe_workspace], policy).safe
    assert not evaluate_strategy_research_display_artifact_safety([unsafe_artifact], policy).safe
    assert not evaluate_strategy_research_display_paper_safety([unsafe_paper], policy).safe
    assert not evaluate_strategy_research_display_hypothesis_safety([unsafe_hypothesis], policy).safe
    assert not evaluate_strategy_research_display_experiment_safety([unsafe_experiment], policy).safe


@pytest.mark.parametrize(
    "rejector",
    [
        reject_display_as_active_ui,
        reject_display_as_strategy_generation,
        reject_display_as_backtest,
        reject_display_as_recommendation,
        reject_display_as_execution_surface,
    ],
)
def test_strategy_research_workspace_display_reject_helpers_block_safely(rejector):
    result = rejector()

    assert result.safe is False
    assert result.display_contract_only is True
    assert result.execution_allowed is False
    assert result.broker_controls_allowed is False
