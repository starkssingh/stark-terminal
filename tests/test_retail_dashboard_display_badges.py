from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_dashboard_display.badges import (
    RetailDashboardDisplayBadgePlaceholder,
    default_retail_dashboard_display_badges,
)
from stark_terminal_core.retail_dashboard_display.contracts import RetailDashboardDisplayBadgeKind


def _badge(**overrides: object) -> RetailDashboardDisplayBadgePlaceholder:
    data = {
        "badge_id": "retail-dashboard-display-badge-test",
        "badge_kind": RetailDashboardDisplayBadgeKind.PLANNING_ONLY,
        "label": "Badge test",
        "description": "Display contract placeholder badge.",
    }
    data.update(overrides)
    return RetailDashboardDisplayBadgePlaceholder(**data)


def test_retail_dashboard_display_badge_placeholder_validates() -> None:
    badge = _badge()

    assert badge.visible is True
    assert badge.active_ui is False
    assert badge.unavailable is True
    assert badge.recommendation is False


def test_retail_dashboard_display_badge_rejects_unknown_kind() -> None:
    with pytest.raises(ValidationError):
        _badge(badge_kind=RetailDashboardDisplayBadgeKind.UNKNOWN)


def test_retail_dashboard_display_badge_enforces_active_ui_false_and_unavailable_true() -> None:
    with pytest.raises(ValidationError):
        _badge(active_ui=True)
    with pytest.raises(ValidationError):
        _badge(unavailable=False)


@pytest.mark.parametrize(
    "field_name",
    [
        "recommendation",
        "action_signal",
        "confidence_signal",
        "decision_object_signal",
        "readiness_to_trade",
        "broker_control",
        "execution_ready",
    ],
)
def test_retail_dashboard_display_badge_rejects_dangerous_signal_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _badge(**{field_name: True})


def test_default_retail_dashboard_display_badges_validate() -> None:
    badges = default_retail_dashboard_display_badges()

    assert badges
    assert all(badge.active_ui is False for badge in badges)
    assert all(badge.unavailable is True for badge in badges)
    assert all(badge.execution_ready is False for badge in badges)
