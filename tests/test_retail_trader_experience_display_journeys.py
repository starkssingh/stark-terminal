from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience_display.contracts import (
    RetailTraderExperienceDisplayJourneyKind,
)
from stark_terminal_core.retail_trader_experience_display.journeys import (
    RetailTraderExperienceDisplayJourneyPlaceholder,
    default_retail_trader_experience_display_journey_placeholders,
)


def _journey_kwargs(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "journey_id": "journey-test",
        "journey_kind": RetailTraderExperienceDisplayJourneyKind.ONBOARDING_VISUAL_PLACEHOLDER,
        "title": "Journey test",
        "description": "Display placeholder only.",
    }
    values.update(overrides)
    return values


def test_retail_trader_experience_display_journey_placeholder_validates() -> None:
    journey = RetailTraderExperienceDisplayJourneyPlaceholder(**_journey_kwargs())

    assert journey.display_contract_only is True
    assert journey.active_ui is False
    assert journey.rendered_now is False
    assert journey.unavailable is True
    assert journey.execution_journey is False


@pytest.mark.parametrize(
    "field",
    [
        "display_contract_only",
        "active_ui",
        "rendered_now",
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
def test_retail_trader_experience_display_journey_rejects_unsafe_flags(field: str) -> None:
    value = False if field in {"display_contract_only", "unavailable"} else True
    with pytest.raises(ValidationError):
        RetailTraderExperienceDisplayJourneyPlaceholder(**_journey_kwargs(**{field: value}))


def test_retail_trader_experience_display_journey_rejects_unknown_kind() -> None:
    with pytest.raises(ValidationError):
        RetailTraderExperienceDisplayJourneyPlaceholder(
            **_journey_kwargs(journey_kind=RetailTraderExperienceDisplayJourneyKind.UNKNOWN)
        )


def test_default_retail_trader_experience_display_journeys_validate() -> None:
    journeys = default_retail_trader_experience_display_journey_placeholders()

    assert len(journeys) >= 7
    assert all(journey.display_contract_only for journey in journeys)
    assert all(journey.unavailable for journey in journeys)
