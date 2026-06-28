from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.strategy_research_workspace_boundary.forbidden import (
    REQUIRED_STRATEGY_RESEARCH_FORBIDDEN_BEHAVIORS,
    StrategyResearchBoundarySeverity,
    StrategyResearchForbiddenBehavior,
    StrategyResearchForbiddenBehaviorKind,
    StrategyResearchForbiddenBehaviorRegistry,
    default_strategy_research_forbidden_behavior_registry,
    default_strategy_research_forbidden_behaviors,
)


def test_strategy_research_forbidden_behavior_registry_validates() -> None:
    registry = default_strategy_research_forbidden_behavior_registry()

    assert registry.complete is True
    assert registry.behaviors
    assert {behavior.kind for behavior in registry.behaviors}.issuperset(
        REQUIRED_STRATEGY_RESEARCH_FORBIDDEN_BEHAVIORS
    )
    assert registry.active_ui_allowed is False
    assert registry.paper_parsing_allowed is False
    assert registry.strategy_generation_allowed is False
    assert registry.backtesting_allowed is False
    assert registry.recommendations_allowed is False
    assert registry.confidence_scoring_allowed is False
    assert registry.decision_object_generation_allowed is False
    assert registry.readiness_to_trade_allowed is False
    assert registry.broker_controls_allowed is False
    assert registry.execution_allowed is False


@pytest.mark.parametrize("flag_name", ["forbidden_now", "requires_future_prompt", "requires_audit_before_unlock"])
def test_strategy_research_forbidden_behavior_enforces_locked_flags(flag_name: str) -> None:
    kwargs = {
        "behavior_id": "strategy-research-test-forbidden-v1",
        "kind": StrategyResearchForbiddenBehaviorKind.ACTIVE_UI,
        "name": "Active UI",
        "description": "Active UI remains forbidden.",
        flag_name: False,
    }
    with pytest.raises(ValidationError):
        StrategyResearchForbiddenBehavior(**kwargs)


def test_strategy_research_forbidden_behavior_rejects_unknowns() -> None:
    with pytest.raises(ValidationError):
        StrategyResearchForbiddenBehavior(
            behavior_id="strategy-research-unknown-forbidden-v1",
            kind=StrategyResearchForbiddenBehaviorKind.UNKNOWN,
            name="Unknown",
            description="Unknown behavior.",
        )
    with pytest.raises(ValidationError):
        StrategyResearchForbiddenBehavior(
            behavior_id="strategy-research-unknown-severity-v1",
            kind=StrategyResearchForbiddenBehaviorKind.ACTIVE_UI,
            name="Unknown severity",
            description="Unknown severity.",
            severity=StrategyResearchBoundarySeverity.UNKNOWN,
        )


@pytest.mark.parametrize(
    "flag_name",
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
def test_strategy_research_forbidden_registry_rejects_dangerous_allow_flags(flag_name: str) -> None:
    with pytest.raises(ValidationError):
        StrategyResearchForbiddenBehaviorRegistry(
            registry_id="strategy-research-forbidden-registry-test-v1",
            behaviors=default_strategy_research_forbidden_behaviors(),
            **{flag_name: True},
        )


def test_strategy_research_forbidden_registry_requires_complete_coverage() -> None:
    behaviors = [
        behavior
        for behavior in default_strategy_research_forbidden_behaviors()
        if behavior.kind != StrategyResearchForbiddenBehaviorKind.EXECUTION
    ]
    with pytest.raises(ValidationError):
        StrategyResearchForbiddenBehaviorRegistry(
            registry_id="strategy-research-incomplete-registry-test-v1",
            behaviors=behaviors,
        )
