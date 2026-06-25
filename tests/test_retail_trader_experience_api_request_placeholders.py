from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_trader_experience_api.requests import (
    RetailTraderExperienceAPIRequestKind,
    RetailTraderExperienceAPIRequestPlaceholder,
    create_retail_trader_experience_api_request_placeholder,
    default_retail_trader_experience_api_request_placeholder,
)


def test_retail_trader_experience_api_request_placeholder_validates() -> None:
    placeholder = create_retail_trader_experience_api_request_placeholder(
        request_id="request-1",
        request_kind=RetailTraderExperienceAPIRequestKind.PERSONA_CONTEXT_REQUEST,
        requested_personas=["  retail_trader_placeholder  "],
        notes=["  contract only  ", ""],
    )

    assert placeholder.request_id == "request-1"
    assert placeholder.request_kind == RetailTraderExperienceAPIRequestKind.PERSONA_CONTEXT_REQUEST
    assert placeholder.requested_personas == ["retail_trader_placeholder"]
    assert placeholder.dashboard_reference_required is True
    assert placeholder.decision_reference_required is False
    assert placeholder.safety_reference_required is True
    assert placeholder.notes == ["contract only"]
    assert placeholder.active_ui_allowed is False
    assert placeholder.suitability_profiling_allowed is False


def test_retail_trader_experience_api_default_request_validates() -> None:
    placeholder = default_retail_trader_experience_api_request_placeholder()

    assert placeholder.dashboard_reference_required is True
    assert placeholder.safety_reference_required is True
    assert placeholder.decision_reference_required is False
    assert placeholder.requested_personas
    assert placeholder.requested_journeys
    assert placeholder.requested_sections
    assert placeholder.requested_cards


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
def test_retail_trader_experience_api_request_rejects_unsafe_flags(field_name: str) -> None:
    with pytest.raises(ValidationError):
        RetailTraderExperienceAPIRequestPlaceholder(
            request_id="request-unsafe",
            request_kind=RetailTraderExperienceAPIRequestKind.EXPERIENCE_OVERVIEW_REQUEST,
            **{field_name: True},
        )


def test_retail_trader_experience_api_request_rejects_unknown_kind_and_missing_required_references() -> None:
    with pytest.raises(ValidationError):
        RetailTraderExperienceAPIRequestPlaceholder(
            request_id="request-unknown",
            request_kind=RetailTraderExperienceAPIRequestKind.UNKNOWN,
        )
    with pytest.raises(ValidationError):
        RetailTraderExperienceAPIRequestPlaceholder(
            request_id="request-no-dashboard",
            request_kind=RetailTraderExperienceAPIRequestKind.EXPERIENCE_OVERVIEW_REQUEST,
            dashboard_reference_required=False,
        )
    with pytest.raises(ValidationError):
        RetailTraderExperienceAPIRequestPlaceholder(
            request_id="request-no-safety",
            request_kind=RetailTraderExperienceAPIRequestKind.EXPERIENCE_OVERVIEW_REQUEST,
            safety_reference_required=False,
        )
