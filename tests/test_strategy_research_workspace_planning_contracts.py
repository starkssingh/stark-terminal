import pytest

from stark_terminal_core.strategy_research_workspace.planning import (
    REQUIRED_STRATEGY_RESEARCH_FORBIDDEN_INTERACTIONS,
    StrategyResearchForbiddenInteractionKind,
    StrategyResearchWorkspacePlanningContract,
    default_strategy_research_workspace_planning_contract,
)


def test_strategy_research_workspace_planning_contract_defaults_validate():
    contract = default_strategy_research_workspace_planning_contract()

    assert contract.plan_id
    assert contract.stage.value == "PLANNING_AND_GUARDRAILS"
    assert contract.planned_workspaces
    assert contract.planned_artifacts
    assert contract.planned_paper_references
    assert contract.planned_hypotheses
    assert contract.planned_dataset_references
    assert contract.planned_experiments
    assert REQUIRED_STRATEGY_RESEARCH_FORBIDDEN_INTERACTIONS.issubset(set(contract.forbidden_interactions))
    assert StrategyResearchForbiddenInteractionKind.PAPER_INGESTION in contract.forbidden_interactions
    assert StrategyResearchForbiddenInteractionKind.PAPER_PARSING in contract.forbidden_interactions
    assert StrategyResearchForbiddenInteractionKind.STRATEGY_GENERATION in contract.forbidden_interactions
    assert StrategyResearchForbiddenInteractionKind.STRATEGY_CODE_GENERATION in contract.forbidden_interactions
    assert StrategyResearchForbiddenInteractionKind.BACKTESTING in contract.forbidden_interactions
    assert StrategyResearchForbiddenInteractionKind.OPTIMIZATION in contract.forbidden_interactions
    assert StrategyResearchForbiddenInteractionKind.RECOMMENDATION_GENERATION in contract.forbidden_interactions
    assert StrategyResearchForbiddenInteractionKind.ACTION_GENERATION in contract.forbidden_interactions
    assert StrategyResearchForbiddenInteractionKind.CONFIDENCE_SCORING in contract.forbidden_interactions
    assert StrategyResearchForbiddenInteractionKind.DECISION_OBJECT_GENERATION in contract.forbidden_interactions
    assert StrategyResearchForbiddenInteractionKind.READINESS_TO_TRADE in contract.forbidden_interactions
    assert StrategyResearchForbiddenInteractionKind.BROKER_CONTROL in contract.forbidden_interactions
    assert StrategyResearchForbiddenInteractionKind.EXECUTION in contract.forbidden_interactions


@pytest.mark.parametrize(
    "field",
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
def test_strategy_research_workspace_planning_contract_rejects_dangerous_allowed_flags(field):
    payload = default_strategy_research_workspace_planning_contract().model_dump()
    payload[field] = True

    with pytest.raises(ValueError):
        StrategyResearchWorkspacePlanningContract(**payload)


def test_strategy_research_workspace_planning_contract_requires_unavailable_by_default():
    payload = default_strategy_research_workspace_planning_contract().model_dump()
    payload["returns_unavailable_by_default"] = False

    with pytest.raises(ValueError):
        StrategyResearchWorkspacePlanningContract(**payload)
