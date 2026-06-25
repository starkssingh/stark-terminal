from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience_api.references import (
    default_retail_trader_experience_api_dashboard_reference,
    default_retail_trader_experience_api_decision_reference,
    default_retail_trader_experience_api_journey_reference,
    default_retail_trader_experience_api_persona_reference,
    default_retail_trader_experience_api_safety_reference,
)
from stark_terminal_core.retail_trader_experience_api.responses import (
    RetailTraderExperienceAPIResponsePlaceholder,
    default_retail_trader_experience_api_response_placeholder,
)
from stark_terminal_core.retail_trader_experience_api.unavailable import (
    default_retail_trader_experience_api_unavailable_response,
)


def _base_response_kwargs() -> dict[str, object]:
    return {
        "response_id": "response-placeholder",
        "persona_reference": default_retail_trader_experience_api_persona_reference(),
        "journey_reference": default_retail_trader_experience_api_journey_reference(),
        "dashboard_reference": default_retail_trader_experience_api_dashboard_reference(),
        "decision_reference": default_retail_trader_experience_api_decision_reference(),
        "safety_reference": default_retail_trader_experience_api_safety_reference(),
        "unavailable_response": default_retail_trader_experience_api_unavailable_response(),
    }


def test_retail_trader_experience_api_response_placeholder_validates() -> None:
    response = default_retail_trader_experience_api_response_placeholder(request_id="request-1")

    assert response.request_id == "request-1"
    assert response.api_contract_skeleton_only is True
    assert response.active_ui_generated is False
    assert response.recommendation_generated is False
    assert response.action_generated is False
    assert response.confidence_generated is False
    assert response.decision_object_generated is False
    assert response.readiness_to_trade_generated is False
    assert response.broker_control_generated is False
    assert response.suitability_profile_generated is False
    assert response.execution_ready is False
    assert response.approval_granted is False
    assert response.override_granted is False


@pytest.mark.parametrize(
    "field_name",
    [
        "active_ui_generated",
        "frontend_component_generated",
        "desktop_component_generated",
        "recommendation_generated",
        "action_generated",
        "confidence_generated",
        "decision_object_generated",
        "readiness_to_trade_generated",
        "broker_control_generated",
        "suitability_profile_generated",
        "execution_ready",
        "approval_granted",
        "override_granted",
    ],
)
def test_retail_trader_experience_api_response_placeholder_rejects_generated_outputs(field_name: str) -> None:
    with pytest.raises(ValidationError):
        RetailTraderExperienceAPIResponsePlaceholder(**_base_response_kwargs(), **{field_name: True})


def test_retail_trader_experience_api_response_placeholder_rejects_active_contract_skeleton_flag() -> None:
    with pytest.raises(ValidationError):
        RetailTraderExperienceAPIResponsePlaceholder(
            **_base_response_kwargs(),
            api_contract_skeleton_only=False,
        )
