from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience.planning import (
    RetailTraderExperienceForbiddenInteractionKind,
    RetailTraderExperiencePlanningContract,
    default_retail_trader_experience_planning_contract,
)


def test_retail_trader_experience_planning_contract_default_is_safe() -> None:
    contract = default_retail_trader_experience_planning_contract()

    assert contract.plan_id
    assert contract.planned_personas
    assert contract.planned_journeys
    assert contract.planned_sections
    assert contract.planned_cards
    assert contract.active_ui_allowed is False
    assert contract.frontend_components_allowed is False
    assert contract.desktop_components_allowed is False
    assert contract.suitability_profiling_allowed is False
    assert contract.returns_unavailable_by_default is True
    required = {
        RetailTraderExperienceForbiddenInteractionKind.RECOMMENDATION_CARD,
        RetailTraderExperienceForbiddenInteractionKind.ACTION_BUTTON,
        RetailTraderExperienceForbiddenInteractionKind.CONFIDENCE_SCORE,
        RetailTraderExperienceForbiddenInteractionKind.DECISION_OBJECT_DISPLAY,
        RetailTraderExperienceForbiddenInteractionKind.READINESS_TO_TRADE_BADGE,
        RetailTraderExperienceForbiddenInteractionKind.BROKER_CONTROL,
        RetailTraderExperienceForbiddenInteractionKind.ORDER_BUTTON,
        RetailTraderExperienceForbiddenInteractionKind.APPROVAL_CONTROL,
        RetailTraderExperienceForbiddenInteractionKind.OVERRIDE_CONTROL,
        RetailTraderExperienceForbiddenInteractionKind.SUITABILITY_PROFILING,
    }
    assert required.issubset(set(contract.forbidden_interactions))


@pytest.mark.parametrize(
    "field_name",
    [
        "active_ui_allowed",
        "frontend_components_allowed",
        "desktop_components_allowed",
        "recommendations_allowed",
        "action_generation_allowed",
        "confidence_scoring_allowed",
        "decision_object_generation_allowed",
        "readiness_to_trade_allowed",
        "broker_controls_allowed",
        "execution_allowed",
        "approval_allowed",
        "override_allowed",
        "suitability_profiling_allowed",
    ],
)
def test_retail_trader_experience_planning_contract_rejects_dangerous_flags(field_name: str) -> None:
    data = default_retail_trader_experience_planning_contract().model_dump()
    data[field_name] = True
    with pytest.raises(ValidationError):
        RetailTraderExperiencePlanningContract(**data)


def test_retail_trader_experience_planning_contract_requires_unavailable_by_default() -> None:
    data = default_retail_trader_experience_planning_contract().model_dump()
    data["returns_unavailable_by_default"] = False
    with pytest.raises(ValidationError):
        RetailTraderExperiencePlanningContract(**data)
