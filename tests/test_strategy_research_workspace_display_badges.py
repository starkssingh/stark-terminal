import pytest
from pydantic import ValidationError

from stark_terminal_core.strategy_research_workspace_display.badges import (
    StrategyResearchWorkspaceDisplayBadgePlaceholder,
    default_strategy_research_workspace_display_badges,
)
from stark_terminal_core.strategy_research_workspace_display.contracts import (
    StrategyResearchWorkspaceDisplayBadgeKind,
)


def _badge_kwargs(**overrides):
    base = {
        "badge_id": "badge-placeholder-test",
        "badge_kind": StrategyResearchWorkspaceDisplayBadgeKind.PLANNING_ONLY,
        "label": "Planning only",
        "description": "Display contract only.",
    }
    base.update(overrides)
    return base


def test_strategy_research_workspace_display_badge_placeholder_validates():
    badge = StrategyResearchWorkspaceDisplayBadgePlaceholder(**_badge_kwargs())

    assert badge.visible is True
    assert badge.active_ui is False
    assert badge.unavailable is True
    assert badge.paper_parsed is False
    assert badge.strategy_generated is False
    assert badge.backtest_generated is False
    assert badge.recommendation is False
    assert badge.action_signal is False
    assert badge.confidence_signal is False
    assert badge.decision_object_signal is False
    assert badge.readiness_to_trade is False
    assert badge.broker_control is False
    assert badge.execution_ready is False


@pytest.mark.parametrize(
    "field,value",
    [
        ("badge_kind", StrategyResearchWorkspaceDisplayBadgeKind.UNKNOWN),
        ("active_ui", True),
        ("unavailable", False),
        ("paper_parsed", True),
        ("strategy_generated", True),
        ("backtest_generated", True),
        ("recommendation", True),
        ("action_signal", True),
        ("confidence_signal", True),
        ("decision_object_signal", True),
        ("readiness_to_trade", True),
        ("broker_control", True),
        ("execution_ready", True),
    ],
)
def test_strategy_research_workspace_display_badge_rejects_unsafe_values(field, value):
    with pytest.raises(ValidationError):
        StrategyResearchWorkspaceDisplayBadgePlaceholder(**_badge_kwargs(**{field: value}))


def test_default_strategy_research_workspace_display_badges_validate():
    badges = default_strategy_research_workspace_display_badges()

    assert badges
    assert all(not badge.active_ui and badge.unavailable for badge in badges)
    assert all(not badge.recommendation and not badge.execution_ready for badge in badges)

