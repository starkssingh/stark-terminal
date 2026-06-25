from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

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
from stark_terminal_core.retail_trader_experience_api.requests import (
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_trader_experience_api_notes,
)
from stark_terminal_core.retail_trader_experience_api.unavailable import (
    RetailTraderExperienceAPIUnavailableResponse,
    default_retail_trader_experience_api_unavailable_response,
)


class RetailTraderExperienceAPIResponsePlaceholder(BaseModel):
    response_id: str
    request_id: str | None = None
    persona_reference: RetailTraderExperienceAPIPersonaReference
    journey_reference: RetailTraderExperienceAPIJourneyReference
    dashboard_reference: RetailTraderExperienceAPIDashboardReference
    decision_reference: RetailTraderExperienceAPIDecisionReference
    safety_reference: RetailTraderExperienceAPISafetyReference
    unavailable_response: RetailTraderExperienceAPIUnavailableResponse
    api_contract_skeleton_only: bool = True
    active_ui_generated: bool = False
    frontend_component_generated: bool = False
    desktop_component_generated: bool = False
    recommendation_generated: bool = False
    action_generated: bool = False
    confidence_generated: bool = False
    decision_object_generated: bool = False
    readiness_to_trade_generated: bool = False
    broker_control_generated: bool = False
    suitability_profile_generated: bool = False
    execution_ready: bool = False
    approval_granted: bool = False
    override_granted: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("response_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience API response placeholder text fields")

    @field_validator("request_id")
    @classmethod
    def optional_text_fields_must_be_trimmed(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_trader_experience_api_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def response_placeholder_must_fail_closed(self) -> RetailTraderExperienceAPIResponsePlaceholder:
        if not self.api_contract_skeleton_only:
            raise ValueError("Retail Trader Experience API response must remain contract-skeleton-only")
        if self.active_ui_generated:
            raise ValueError("Retail Trader Experience API active UI generation is forbidden")
        if self.frontend_component_generated:
            raise ValueError("Retail Trader Experience API frontend component generation is forbidden")
        if self.desktop_component_generated:
            raise ValueError("Retail Trader Experience API desktop component generation is forbidden")
        if self.recommendation_generated:
            raise ValueError("Retail Trader Experience API recommendation generation is forbidden")
        if self.action_generated:
            raise ValueError("Retail Trader Experience API action generation is forbidden")
        if self.confidence_generated:
            raise ValueError("Retail Trader Experience API confidence generation is forbidden")
        if self.decision_object_generated:
            raise ValueError("Retail Trader Experience API DecisionObject generation is forbidden")
        if self.readiness_to_trade_generated:
            raise ValueError("Retail Trader Experience API readiness-to-trade generation is forbidden")
        if self.broker_control_generated:
            raise ValueError("Retail Trader Experience API broker control generation is forbidden")
        if self.suitability_profile_generated:
            raise ValueError("Retail Trader Experience API suitability profile generation is forbidden")
        if self.execution_ready:
            raise ValueError("Retail Trader Experience API execution readiness is forbidden")
        if self.approval_granted:
            raise ValueError("Retail Trader Experience API approval cannot be granted")
        if self.override_granted:
            raise ValueError("Retail Trader Experience API override cannot be granted")
        return self


def default_retail_trader_experience_api_response_placeholder(
    request_id: str | None = None,
    persona_reference: RetailTraderExperienceAPIPersonaReference | None = None,
    journey_reference: RetailTraderExperienceAPIJourneyReference | None = None,
    dashboard_reference: RetailTraderExperienceAPIDashboardReference | None = None,
    decision_reference: RetailTraderExperienceAPIDecisionReference | None = None,
    safety_reference: RetailTraderExperienceAPISafetyReference | None = None,
    unavailable_response: RetailTraderExperienceAPIUnavailableResponse | None = None,
) -> RetailTraderExperienceAPIResponsePlaceholder:
    return RetailTraderExperienceAPIResponsePlaceholder(
        response_id="retail-trader-experience-api-response-placeholder-v1",
        request_id=request_id,
        persona_reference=persona_reference or default_retail_trader_experience_api_persona_reference(),
        journey_reference=journey_reference or default_retail_trader_experience_api_journey_reference(),
        dashboard_reference=dashboard_reference or default_retail_trader_experience_api_dashboard_reference(),
        decision_reference=decision_reference or default_retail_trader_experience_api_decision_reference(),
        safety_reference=safety_reference or default_retail_trader_experience_api_safety_reference(),
        unavailable_response=unavailable_response or default_retail_trader_experience_api_unavailable_response(),
        notes=["Response placeholder contains references only and no generated trader outputs."],
    )
