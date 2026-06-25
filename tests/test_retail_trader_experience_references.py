from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience.references import (
    RetailTraderExperienceDashboardReference,
    RetailTraderExperienceDecisionReference,
    RetailTraderExperienceSafetyReference,
    default_retail_trader_experience_dashboard_reference,
    default_retail_trader_experience_decision_reference,
    default_retail_trader_experience_safety_reference,
)


@pytest.mark.parametrize(
    "field_name",
    [
        "active_dashboard",
        "active_ui",
        "recommendation_available",
        "readiness_to_trade_available",
        "broker_controls_available",
        "execution_available",
        "display_ready",
    ],
)
def test_retail_trader_dashboard_reference_rejects_dangerous_availability(field_name: str) -> None:
    reference = default_retail_trader_experience_dashboard_reference()
    assert reference.display_ready is False
    data = reference.model_dump()
    data[field_name] = True
    with pytest.raises(ValidationError):
        RetailTraderExperienceDashboardReference(**data)


@pytest.mark.parametrize(
    "field_name",
    [
        "active_decision_object",
        "recommendation_available",
        "action_available",
        "confidence_available",
        "readiness_to_trade_available",
        "broker_controls_available",
        "execution_available",
        "display_ready",
    ],
)
def test_retail_trader_decision_reference_rejects_dangerous_availability(field_name: str) -> None:
    reference = default_retail_trader_experience_decision_reference()
    assert reference.display_ready is False
    data = reference.model_dump()
    data[field_name] = True
    with pytest.raises(ValidationError):
        RetailTraderExperienceDecisionReference(**data)


@pytest.mark.parametrize(
    "field_name",
    [
        "safety_passed",
        "approval_granted",
        "override_granted",
        "readiness_to_trade_allowed",
        "broker_controls_allowed",
        "execution_allowed",
    ],
)
def test_retail_trader_safety_reference_rejects_dangerous_flags(field_name: str) -> None:
    reference = default_retail_trader_experience_safety_reference()
    assert reference.safety_passed is False
    data = reference.model_dump()
    data[field_name] = True
    with pytest.raises(ValidationError):
        RetailTraderExperienceSafetyReference(**data)
