from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience.journeys import (
    RetailTraderJourneyPlaceholder,
    default_retail_trader_journey_placeholders,
)
from stark_terminal_core.retail_trader_experience.planning import RetailTraderJourneyKind


def test_retail_trader_journey_placeholders_default_validate() -> None:
    journeys = default_retail_trader_journey_placeholders()
    assert journeys
    for journey in journeys:
        assert journey.planning_only is True
        assert journey.active_ui is False
        assert journey.unavailable is True
        assert journey.recommendation_journey is False
        assert journey.trading_advice_journey is False
        assert journey.execution_journey is False


def test_retail_trader_journey_rejects_unknown_kind() -> None:
    data = default_retail_trader_journey_placeholders()[0].model_dump()
    data["journey_kind"] = RetailTraderJourneyKind.UNKNOWN
    with pytest.raises(ValidationError):
        RetailTraderJourneyPlaceholder(**data)


@pytest.mark.parametrize(
    "field_name",
    [
        "planning_only",
        "active_ui",
        "unavailable",
        "recommendation_journey",
        "trading_advice_journey",
        "broker_control_journey",
        "execution_journey",
        "readiness_to_trade_journey",
        "approval_journey",
        "override_journey",
    ],
)
def test_retail_trader_journey_enforces_safe_flags(field_name: str) -> None:
    data = default_retail_trader_journey_placeholders()[0].model_dump()
    data[field_name] = False if field_name in {"planning_only", "unavailable"} else True
    with pytest.raises(ValidationError):
        RetailTraderJourneyPlaceholder(**data)
