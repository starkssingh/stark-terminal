from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience.cards import (
    RetailTraderExperienceCardPlaceholder,
    default_retail_trader_experience_card_placeholders,
)
from stark_terminal_core.retail_trader_experience.planning import RetailTraderExperienceCardKind


def test_retail_trader_experience_card_placeholders_default_validate() -> None:
    cards = default_retail_trader_experience_card_placeholders()
    assert cards
    for card in cards:
        assert card.active_ui is False
        assert card.unavailable is True
        assert card.planning_only is True
        assert card.recommendation_card is False
        assert card.confidence_display is False
        assert card.suitability_profile_display is False
        assert card.execution_control is False


def test_retail_trader_experience_card_rejects_unknown_kind() -> None:
    data = default_retail_trader_experience_card_placeholders()[0].model_dump()
    data["card_kind"] = RetailTraderExperienceCardKind.UNKNOWN
    with pytest.raises(ValidationError):
        RetailTraderExperienceCardPlaceholder(**data)


@pytest.mark.parametrize(
    "field_name",
    [
        "active_ui",
        "unavailable",
        "planning_only",
        "recommendation_card",
        "action_card",
        "confidence_display",
        "decision_object_display",
        "readiness_to_trade_display",
        "broker_control",
        "execution_control",
        "approval_control",
        "override_control",
        "suitability_profile_display",
    ],
)
def test_retail_trader_experience_card_enforces_safe_flags(field_name: str) -> None:
    data = default_retail_trader_experience_card_placeholders()[0].model_dump()
    data[field_name] = False if field_name in {"unavailable", "planning_only"} else True
    with pytest.raises(ValidationError):
        RetailTraderExperienceCardPlaceholder(**data)
