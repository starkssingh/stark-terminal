import pytest

from stark_terminal_core.strategy_research_workspace.interactions import (
    StrategyResearchForbiddenInteraction,
    default_strategy_research_forbidden_interactions,
)
from stark_terminal_core.strategy_research_workspace.planning import StrategyResearchForbiddenInteractionKind


def test_strategy_research_forbidden_interactions_include_all_dangerous_kinds():
    interactions = default_strategy_research_forbidden_interactions()
    kinds = {interaction.kind for interaction in interactions}

    assert interactions
    assert StrategyResearchForbiddenInteractionKind.ACTIVE_UI in kinds
    assert StrategyResearchForbiddenInteractionKind.FRONTEND_COMPONENT in kinds
    assert StrategyResearchForbiddenInteractionKind.DESKTOP_COMPONENT in kinds
    assert StrategyResearchForbiddenInteractionKind.PAPER_INGESTION in kinds
    assert StrategyResearchForbiddenInteractionKind.PAPER_PARSING in kinds
    assert StrategyResearchForbiddenInteractionKind.STRATEGY_GENERATION in kinds
    assert StrategyResearchForbiddenInteractionKind.STRATEGY_CODE_GENERATION in kinds
    assert StrategyResearchForbiddenInteractionKind.BACKTESTING in kinds
    assert StrategyResearchForbiddenInteractionKind.OPTIMIZATION in kinds
    assert StrategyResearchForbiddenInteractionKind.RECOMMENDATION_GENERATION in kinds
    assert StrategyResearchForbiddenInteractionKind.ACTION_GENERATION in kinds
    assert StrategyResearchForbiddenInteractionKind.CONFIDENCE_SCORING in kinds
    assert StrategyResearchForbiddenInteractionKind.DECISION_OBJECT_GENERATION in kinds
    assert StrategyResearchForbiddenInteractionKind.READINESS_TO_TRADE in kinds
    assert StrategyResearchForbiddenInteractionKind.BROKER_CONTROL in kinds
    assert StrategyResearchForbiddenInteractionKind.ORDER_BUTTON in kinds
    assert StrategyResearchForbiddenInteractionKind.EXECUTION in kinds
    assert all(interaction.forbidden_now for interaction in interactions)
    assert all(interaction.requires_future_prompt for interaction in interactions)
    assert all(interaction.requires_audit_before_unlock for interaction in interactions)


@pytest.mark.parametrize("field", ["forbidden_now", "requires_future_prompt", "requires_audit_before_unlock"])
def test_strategy_research_forbidden_interaction_enforces_lock_flags(field):
    payload = default_strategy_research_forbidden_interactions()[0].model_dump()
    payload[field] = False

    with pytest.raises(ValueError):
        StrategyResearchForbiddenInteraction(**payload)


def test_strategy_research_forbidden_interaction_rejects_unknown_kind():
    payload = default_strategy_research_forbidden_interactions()[0].model_dump()
    payload["kind"] = StrategyResearchForbiddenInteractionKind.UNKNOWN

    with pytest.raises(ValueError):
        StrategyResearchForbiddenInteraction(**payload)
