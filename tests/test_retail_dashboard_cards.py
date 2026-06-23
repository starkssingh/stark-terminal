from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_dashboard.cards import (
    RetailDashboardCardKind,
    RetailDashboardCardPlaceholder,
    default_retail_dashboard_card_placeholders,
)


def _card(**overrides: object) -> RetailDashboardCardPlaceholder:
    data = {
        "card_id": "card-test",
        "card_kind": RetailDashboardCardKind.PLACEHOLDER,
        "title": "Placeholder",
        "description": "Planning-only card.",
    }
    data.update(overrides)
    return RetailDashboardCardPlaceholder(**data)


def test_valid_retail_dashboard_card_placeholder() -> None:
    card = _card()

    assert card.active_ui is False
    assert card.unavailable is True
    assert card.planning_only is True
    assert card.recommendation_card is False
    assert card.execution_control is False


def test_retail_dashboard_card_rejects_unknown_kind() -> None:
    with pytest.raises(ValidationError):
        _card(card_kind=RetailDashboardCardKind.UNKNOWN)


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("active_ui", True),
        ("unavailable", False),
        ("planning_only", False),
        ("recommendation_card", True),
        ("action_card", True),
        ("confidence_display", True),
        ("decision_object_display", True),
        ("readiness_to_trade_display", True),
        ("broker_control", True),
        ("execution_control", True),
        ("approval_control", True),
        ("override_control", True),
    ],
)
def test_retail_dashboard_card_rejects_unsafe_flags(field_name: str, value: object) -> None:
    with pytest.raises(ValidationError):
        _card(**{field_name: value})


def test_default_retail_dashboard_cards_validate() -> None:
    cards = default_retail_dashboard_card_placeholders()

    assert cards
    assert all(card.active_ui is False for card in cards)
    assert all(card.unavailable is True for card in cards)
    assert all(card.planning_only is True for card in cards)
    assert all(card.recommendation_card is False for card in cards)
