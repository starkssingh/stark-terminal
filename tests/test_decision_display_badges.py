from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_display.badges import (
    DecisionDisplayBadgePlaceholder,
    default_decision_display_badges,
)
from stark_terminal_core.decision_display.contracts import DecisionDisplayBadgeKind


def _valid_badge_kwargs() -> dict[str, object]:
    return {
        "badge_id": "display-badge-test",
        "badge_kind": DecisionDisplayBadgeKind.UNAVAILABLE,
        "label": "Unavailable",
        "description": "Display badge placeholder.",
    }


def test_decision_display_badge_placeholder_validates() -> None:
    badge = DecisionDisplayBadgePlaceholder(**_valid_badge_kwargs())

    assert badge.unavailable is True
    assert badge.planning_only is True
    assert badge.recommendation is False


@pytest.mark.parametrize(
    "override",
    [
        {"badge_kind": DecisionDisplayBadgeKind.UNKNOWN},
        {"unavailable": False},
        {"planning_only": False},
        {"recommendation": True},
        {"action_signal": True},
        {"confidence_signal": True},
        {"readiness_to_trade": True},
        {"approval_granted": True},
        {"execution_ready": True},
    ],
)
def test_decision_display_badge_placeholder_rejects_unsafe_values(override: dict[str, object]) -> None:
    kwargs = _valid_badge_kwargs()
    kwargs.update(override)

    with pytest.raises(ValidationError):
        DecisionDisplayBadgePlaceholder(**kwargs)


def test_default_decision_display_badges_validate() -> None:
    badges = default_decision_display_badges()

    assert badges
    assert all(badge.unavailable for badge in badges)
    assert all(not badge.recommendation for badge in badges)
    assert all(not badge.readiness_to_trade for badge in badges)

