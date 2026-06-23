from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_display.cards import (
    DecisionDisplayCardPlaceholder,
    default_decision_display_card_placeholders,
)
from stark_terminal_core.decision_display.contracts import DecisionDisplayCardKind


def _valid_card_kwargs() -> dict[str, object]:
    return {
        "card_id": "display-card-test",
        "card_kind": DecisionDisplayCardKind.PLACEHOLDER,
        "title": "Display Card",
        "description": "Display card placeholder.",
    }


def test_decision_display_card_placeholder_validates() -> None:
    card = DecisionDisplayCardPlaceholder(**_valid_card_kwargs())

    assert card.unavailable is True
    assert card.planning_only is True
    assert card.recommendation_generated is False


@pytest.mark.parametrize(
    "override",
    [
        {"card_kind": DecisionDisplayCardKind.UNKNOWN},
        {"unavailable": False},
        {"planning_only": False},
        {"recommendation_generated": True},
        {"action_generated": True},
        {"confidence_generated": True},
        {"decision_object_generated": True},
        {"readiness_to_trade_generated": True},
        {"execution_ready": True},
        {"approval_granted": True},
        {"override_granted": True},
    ],
)
def test_decision_display_card_placeholder_rejects_unsafe_values(override: dict[str, object]) -> None:
    kwargs = _valid_card_kwargs()
    kwargs.update(override)

    with pytest.raises(ValidationError):
        DecisionDisplayCardPlaceholder(**kwargs)


def test_default_decision_display_cards_validate() -> None:
    cards = default_decision_display_card_placeholders()

    assert cards
    assert all(card.unavailable for card in cards)
    assert all(not card.recommendation_generated for card in cards)
    assert all(not card.readiness_to_trade_generated for card in cards)

