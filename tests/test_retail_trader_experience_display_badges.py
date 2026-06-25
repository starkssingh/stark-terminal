from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience_display.badges import (
    RetailTraderExperienceDisplayBadgePlaceholder,
    default_retail_trader_experience_display_badges,
)
from stark_terminal_core.retail_trader_experience_display.contracts import (
    RetailTraderExperienceDisplayBadgeKind,
)


def _badge_kwargs(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "badge_id": "badge-test",
        "badge_kind": RetailTraderExperienceDisplayBadgeKind.PLANNING_ONLY,
        "label": "Badge test",
        "description": "Display placeholder only.",
    }
    values.update(overrides)
    return values


def test_retail_trader_experience_display_badge_placeholder_validates() -> None:
    badge = RetailTraderExperienceDisplayBadgePlaceholder(**_badge_kwargs())

    assert badge.active_ui is False
    assert badge.unavailable is True
    assert badge.recommendation is False
    assert badge.readiness_to_trade is False
    assert badge.execution_ready is False


@pytest.mark.parametrize(
    "field",
    [
        "active_ui",
        "unavailable",
        "recommendation",
        "action_signal",
        "confidence_signal",
        "decision_object_signal",
        "readiness_to_trade",
        "broker_control",
        "execution_ready",
        "suitability_profile",
    ],
)
def test_retail_trader_experience_display_badge_rejects_unsafe_flags(field: str) -> None:
    value = False if field == "unavailable" else True
    with pytest.raises(ValidationError):
        RetailTraderExperienceDisplayBadgePlaceholder(**_badge_kwargs(**{field: value}))


def test_retail_trader_experience_display_badge_rejects_unknown_kind() -> None:
    with pytest.raises(ValidationError):
        RetailTraderExperienceDisplayBadgePlaceholder(
            **_badge_kwargs(badge_kind=RetailTraderExperienceDisplayBadgeKind.UNKNOWN)
        )


def test_default_retail_trader_experience_display_badges_validate() -> None:
    badges = default_retail_trader_experience_display_badges()

    assert len(badges) >= 8
    assert all(badge.unavailable for badge in badges)
    assert all(not badge.execution_ready for badge in badges)
