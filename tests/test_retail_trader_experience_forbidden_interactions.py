from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience.interactions import (
    RetailTraderExperienceForbiddenInteraction,
    default_retail_trader_experience_forbidden_interactions,
)
from stark_terminal_core.retail_trader_experience.planning import (
    RetailTraderExperienceForbiddenInteractionKind,
)


def test_retail_trader_forbidden_interactions_default_validate() -> None:
    interactions = default_retail_trader_experience_forbidden_interactions()
    kinds = {interaction.kind for interaction in interactions}
    assert RetailTraderExperienceForbiddenInteractionKind.RECOMMENDATION_CARD in kinds
    assert RetailTraderExperienceForbiddenInteractionKind.ACTION_BUTTON in kinds
    assert RetailTraderExperienceForbiddenInteractionKind.CONFIDENCE_SCORE in kinds
    assert RetailTraderExperienceForbiddenInteractionKind.DECISION_OBJECT_DISPLAY in kinds
    assert RetailTraderExperienceForbiddenInteractionKind.READINESS_TO_TRADE_BADGE in kinds
    assert RetailTraderExperienceForbiddenInteractionKind.BROKER_CONTROL in kinds
    assert RetailTraderExperienceForbiddenInteractionKind.ORDER_BUTTON in kinds
    assert RetailTraderExperienceForbiddenInteractionKind.APPROVAL_CONTROL in kinds
    assert RetailTraderExperienceForbiddenInteractionKind.OVERRIDE_CONTROL in kinds
    assert RetailTraderExperienceForbiddenInteractionKind.SUITABILITY_PROFILING in kinds
    for interaction in interactions:
        assert interaction.forbidden_now is True
        assert interaction.requires_future_prompt is True
        assert interaction.requires_audit_before_unlock is True


@pytest.mark.parametrize(
    "field_name",
    ["forbidden_now", "requires_future_prompt", "requires_audit_before_unlock"],
)
def test_retail_trader_forbidden_interactions_enforce_lock_flags(field_name: str) -> None:
    data = default_retail_trader_experience_forbidden_interactions()[0].model_dump()
    data[field_name] = False
    with pytest.raises(ValidationError):
        RetailTraderExperienceForbiddenInteraction(**data)


def test_retail_trader_forbidden_interactions_reject_unknown_kind() -> None:
    data = default_retail_trader_experience_forbidden_interactions()[0].model_dump()
    data["kind"] = RetailTraderExperienceForbiddenInteractionKind.UNKNOWN
    with pytest.raises(ValidationError):
        RetailTraderExperienceForbiddenInteraction(**data)
