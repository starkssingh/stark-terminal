from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience_api.requests import (
    RetailTraderExperienceAPIUnavailableReason,
)
from stark_terminal_core.retail_trader_experience_api.unavailable import (
    RetailTraderExperienceAPIUnavailableResponse,
    default_retail_trader_experience_api_unavailable_response,
)


def test_retail_trader_experience_api_unavailable_response_validates() -> None:
    response = default_retail_trader_experience_api_unavailable_response()

    assert response.unavailable is True
    assert response.reason == RetailTraderExperienceAPIUnavailableReason.API_CONTRACT_SKELETON_ONLY
    assert response.api_contract_skeleton_only is True
    assert response.active_ui_allowed is False
    assert response.recommendations_allowed is False
    assert response.execution_allowed is False
    assert response.suitability_profiling_allowed is False
    assert response.notes


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
        "approval_granted",
        "override_granted",
        "suitability_profiling_allowed",
    ],
)
def test_retail_trader_experience_api_unavailable_response_rejects_unsafe_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        RetailTraderExperienceAPIUnavailableResponse(
            response_id="unavailable-unsafe",
            reason=RetailTraderExperienceAPIUnavailableReason.API_CONTRACT_SKELETON_ONLY,
            message="Unavailable.",
            **{field_name: True},
        )


def test_retail_trader_experience_api_unavailable_response_rejects_non_unavailable_unknown_and_active_contract() -> None:
    with pytest.raises(ValidationError):
        RetailTraderExperienceAPIUnavailableResponse(
            response_id="unavailable-false",
            unavailable=False,
            reason=RetailTraderExperienceAPIUnavailableReason.API_CONTRACT_SKELETON_ONLY,
            message="Unavailable.",
        )
    with pytest.raises(ValidationError):
        RetailTraderExperienceAPIUnavailableResponse(
            response_id="unavailable-unknown",
            reason=RetailTraderExperienceAPIUnavailableReason.UNKNOWN,
            message="Unavailable.",
        )
    with pytest.raises(ValidationError):
        RetailTraderExperienceAPIUnavailableResponse(
            response_id="unavailable-active-contract",
            reason=RetailTraderExperienceAPIUnavailableReason.API_CONTRACT_SKELETON_ONLY,
            message="Unavailable.",
            api_contract_skeleton_only=False,
        )
