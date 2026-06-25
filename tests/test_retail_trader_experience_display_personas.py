from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience_display.contracts import (
    RetailTraderExperienceDisplayPersonaKind,
)
from stark_terminal_core.retail_trader_experience_display.personas import (
    RetailTraderExperienceDisplayPersonaPlaceholder,
    default_retail_trader_experience_display_persona_placeholders,
)


def _persona_kwargs(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "persona_id": "persona-test",
        "persona_kind": RetailTraderExperienceDisplayPersonaKind.RETAIL_TRADER_VISUAL_PLACEHOLDER,
        "name": "Persona test",
        "description": "Display placeholder only.",
    }
    values.update(overrides)
    return values


def test_retail_trader_experience_display_persona_placeholder_validates() -> None:
    persona = RetailTraderExperienceDisplayPersonaPlaceholder(**_persona_kwargs())

    assert persona.display_contract_only is True
    assert persona.active_ui is False
    assert persona.rendered_now is False
    assert persona.suitability_profile is False
    assert persona.trading_permission_profile is False
    assert persona.execution_allowed is False


@pytest.mark.parametrize(
    "field",
    [
        "display_contract_only",
        "active_ui",
        "rendered_now",
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
def test_retail_trader_experience_display_persona_rejects_unsafe_flags(field: str) -> None:
    value = False if field == "display_contract_only" else True
    with pytest.raises(ValidationError):
        RetailTraderExperienceDisplayPersonaPlaceholder(**_persona_kwargs(**{field: value}))


def test_retail_trader_experience_display_persona_rejects_unknown_kind() -> None:
    with pytest.raises(ValidationError):
        RetailTraderExperienceDisplayPersonaPlaceholder(
            **_persona_kwargs(persona_kind=RetailTraderExperienceDisplayPersonaKind.UNKNOWN)
        )


def test_default_retail_trader_experience_display_personas_validate() -> None:
    personas = default_retail_trader_experience_display_persona_placeholders()

    assert len(personas) >= 6
    assert all(persona.display_contract_only for persona in personas)
    assert all(not persona.suitability_profile for persona in personas)
