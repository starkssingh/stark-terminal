from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience_api.references import (
    RetailTraderExperienceAPIDashboardReference,
    RetailTraderExperienceAPIDecisionReference,
    RetailTraderExperienceAPIJourneyReference,
    RetailTraderExperienceAPIPersonaReference,
    RetailTraderExperienceAPISafetyReference,
    default_retail_trader_experience_api_dashboard_reference,
    default_retail_trader_experience_api_decision_reference,
    default_retail_trader_experience_api_journey_reference,
    default_retail_trader_experience_api_persona_reference,
    default_retail_trader_experience_api_safety_reference,
)


def test_retail_trader_experience_api_default_references_validate() -> None:
    assert default_retail_trader_experience_api_persona_reference().active_profile is False
    assert default_retail_trader_experience_api_journey_reference().active_journey is False
    assert default_retail_trader_experience_api_dashboard_reference().active_dashboard is False
    assert default_retail_trader_experience_api_decision_reference().active_decision_object is False
    assert default_retail_trader_experience_api_safety_reference().safety_passed is False


@pytest.mark.parametrize(
    ("model", "field_name"),
    [
        (RetailTraderExperienceAPIPersonaReference, "active_profile"),
        (RetailTraderExperienceAPIPersonaReference, "suitability_profile"),
        (RetailTraderExperienceAPIPersonaReference, "trading_permission_profile"),
        (RetailTraderExperienceAPIPersonaReference, "recommendation_available"),
        (RetailTraderExperienceAPIPersonaReference, "broker_controls_available"),
        (RetailTraderExperienceAPIPersonaReference, "execution_available"),
        (RetailTraderExperienceAPIPersonaReference, "display_ready"),
        (RetailTraderExperienceAPIJourneyReference, "active_journey"),
        (RetailTraderExperienceAPIJourneyReference, "trading_advice_journey"),
        (RetailTraderExperienceAPIJourneyReference, "readiness_to_trade_journey"),
        (RetailTraderExperienceAPIJourneyReference, "broker_control_journey"),
        (RetailTraderExperienceAPIJourneyReference, "execution_journey"),
        (RetailTraderExperienceAPIJourneyReference, "display_ready"),
        (RetailTraderExperienceAPIDashboardReference, "active_dashboard"),
        (RetailTraderExperienceAPIDashboardReference, "active_ui"),
        (RetailTraderExperienceAPIDashboardReference, "recommendation_available"),
        (RetailTraderExperienceAPIDashboardReference, "readiness_to_trade_available"),
        (RetailTraderExperienceAPIDashboardReference, "broker_controls_available"),
        (RetailTraderExperienceAPIDashboardReference, "execution_available"),
        (RetailTraderExperienceAPIDashboardReference, "display_ready"),
        (RetailTraderExperienceAPIDecisionReference, "active_decision_object"),
        (RetailTraderExperienceAPIDecisionReference, "recommendation_available"),
        (RetailTraderExperienceAPIDecisionReference, "action_available"),
        (RetailTraderExperienceAPIDecisionReference, "confidence_available"),
        (RetailTraderExperienceAPIDecisionReference, "readiness_to_trade_available"),
        (RetailTraderExperienceAPIDecisionReference, "broker_controls_available"),
        (RetailTraderExperienceAPIDecisionReference, "execution_available"),
        (RetailTraderExperienceAPIDecisionReference, "display_ready"),
        (RetailTraderExperienceAPISafetyReference, "safety_passed"),
        (RetailTraderExperienceAPISafetyReference, "approval_granted"),
        (RetailTraderExperienceAPISafetyReference, "override_granted"),
        (RetailTraderExperienceAPISafetyReference, "readiness_to_trade_allowed"),
        (RetailTraderExperienceAPISafetyReference, "broker_controls_allowed"),
        (RetailTraderExperienceAPISafetyReference, "execution_allowed"),
        (RetailTraderExperienceAPISafetyReference, "suitability_profiling_allowed"),
    ],
)
def test_retail_trader_experience_api_references_reject_unsafe_flags(model: type, field_name: str) -> None:
    with pytest.raises(ValidationError):
        model(reference_id="reference-unsafe", **{field_name: True})
