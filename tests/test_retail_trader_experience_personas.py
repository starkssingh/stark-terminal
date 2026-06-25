from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience.personas import (
    RetailTraderPersonaPlaceholder,
    default_retail_trader_persona_placeholders,
)
from stark_terminal_core.retail_trader_experience.planning import RetailTraderPersonaKind


def test_retail_trader_persona_placeholders_default_validate() -> None:
    personas = default_retail_trader_persona_placeholders()
    assert len(personas) >= 6
    for persona in personas:
        assert persona.planning_only is True
        assert persona.active_profile is False
        assert persona.suitability_profile is False
        assert persona.trading_permission_profile is False
        assert persona.recommendations_allowed is False
        assert persona.execution_allowed is False


def test_retail_trader_persona_rejects_unknown_kind() -> None:
    data = default_retail_trader_persona_placeholders()[0].model_dump()
    data["persona_kind"] = RetailTraderPersonaKind.UNKNOWN
    with pytest.raises(ValidationError):
        RetailTraderPersonaPlaceholder(**data)


@pytest.mark.parametrize(
    "field_name",
    [
        "planning_only",
        "active_profile",
        "suitability_profile",
        "trading_permission_profile",
        "recommendations_allowed",
        "action_generation_allowed",
        "confidence_scoring_allowed",
        "decision_object_generation_allowed",
        "readiness_to_trade_allowed",
        "broker_controls_allowed",
        "execution_allowed",
    ],
)
def test_retail_trader_persona_enforces_safe_flags(field_name: str) -> None:
    data = default_retail_trader_persona_placeholders()[0].model_dump()
    data[field_name] = False if field_name == "planning_only" else True
    with pytest.raises(ValidationError):
        RetailTraderPersonaPlaceholder(**data)
