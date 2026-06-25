from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_trader_experience_api.requests import _non_empty_text, _utc_datetime, _utc_now


def _optional_trimmed(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None


class RetailTraderExperienceAPIPersonaReference(BaseModel):
    reference_id: str
    persona_id: str | None = None
    required: bool = False
    active_profile: bool = False
    suitability_profile: bool = False
    trading_permission_profile: bool = False
    recommendation_available: bool = False
    broker_controls_available: bool = False
    execution_available: bool = False
    display_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience API persona reference text fields")

    @field_validator("persona_id")
    @classmethod
    def optional_text_fields_must_be_trimmed(cls, value: str | None) -> str | None:
        return _optional_trimmed(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def persona_reference_must_fail_closed(self) -> RetailTraderExperienceAPIPersonaReference:
        if self.active_profile:
            raise ValueError("Retail Trader Experience API persona reference cannot be active")
        if self.suitability_profile:
            raise ValueError("Retail Trader Experience API persona reference cannot be a suitability profile")
        if self.trading_permission_profile:
            raise ValueError("Retail Trader Experience API persona reference cannot be a trading permission profile")
        if self.recommendation_available:
            raise ValueError("Retail Trader Experience API persona reference cannot expose recommendations")
        if self.broker_controls_available:
            raise ValueError("Retail Trader Experience API persona reference cannot expose broker controls")
        if self.execution_available:
            raise ValueError("Retail Trader Experience API persona reference cannot expose execution")
        if self.display_ready:
            raise ValueError("Retail Trader Experience API persona reference cannot be display-ready")
        return self


class RetailTraderExperienceAPIJourneyReference(BaseModel):
    reference_id: str
    journey_id: str | None = None
    required: bool = False
    active_journey: bool = False
    trading_advice_journey: bool = False
    readiness_to_trade_journey: bool = False
    broker_control_journey: bool = False
    execution_journey: bool = False
    display_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience API journey reference text fields")

    @field_validator("journey_id")
    @classmethod
    def optional_text_fields_must_be_trimmed(cls, value: str | None) -> str | None:
        return _optional_trimmed(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def journey_reference_must_fail_closed(self) -> RetailTraderExperienceAPIJourneyReference:
        if self.active_journey:
            raise ValueError("Retail Trader Experience API journey reference cannot be active")
        if self.trading_advice_journey:
            raise ValueError("Retail Trader Experience API journey reference cannot be trading advice")
        if self.readiness_to_trade_journey:
            raise ValueError("Retail Trader Experience API journey reference cannot be readiness-to-trade")
        if self.broker_control_journey:
            raise ValueError("Retail Trader Experience API journey reference cannot expose broker controls")
        if self.execution_journey:
            raise ValueError("Retail Trader Experience API journey reference cannot expose execution")
        if self.display_ready:
            raise ValueError("Retail Trader Experience API journey reference cannot be display-ready")
        return self


class RetailTraderExperienceAPIDashboardReference(BaseModel):
    reference_id: str
    dashboard_id: str | None = None
    required: bool = True
    active_dashboard: bool = False
    active_ui: bool = False
    recommendation_available: bool = False
    readiness_to_trade_available: bool = False
    broker_controls_available: bool = False
    execution_available: bool = False
    display_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience API dashboard reference text fields")

    @field_validator("dashboard_id")
    @classmethod
    def optional_text_fields_must_be_trimmed(cls, value: str | None) -> str | None:
        return _optional_trimmed(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def dashboard_reference_must_fail_closed(self) -> RetailTraderExperienceAPIDashboardReference:
        if self.active_dashboard:
            raise ValueError("Retail Trader Experience API dashboard reference cannot be active")
        if self.active_ui:
            raise ValueError("Retail Trader Experience API dashboard reference cannot expose active UI")
        if self.recommendation_available:
            raise ValueError("Retail Trader Experience API dashboard reference cannot expose recommendations")
        if self.readiness_to_trade_available:
            raise ValueError("Retail Trader Experience API dashboard reference cannot expose readiness-to-trade")
        if self.broker_controls_available:
            raise ValueError("Retail Trader Experience API dashboard reference cannot expose broker controls")
        if self.execution_available:
            raise ValueError("Retail Trader Experience API dashboard reference cannot expose execution")
        if self.display_ready:
            raise ValueError("Retail Trader Experience API dashboard reference cannot be display-ready")
        return self


class RetailTraderExperienceAPIDecisionReference(BaseModel):
    reference_id: str
    decision_object_id: str | None = None
    required: bool = False
    active_decision_object: bool = False
    recommendation_available: bool = False
    action_available: bool = False
    confidence_available: bool = False
    readiness_to_trade_available: bool = False
    broker_controls_available: bool = False
    execution_available: bool = False
    display_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience API decision reference text fields")

    @field_validator("decision_object_id")
    @classmethod
    def optional_text_fields_must_be_trimmed(cls, value: str | None) -> str | None:
        return _optional_trimmed(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def decision_reference_must_fail_closed(self) -> RetailTraderExperienceAPIDecisionReference:
        if self.active_decision_object:
            raise ValueError("Retail Trader Experience API decision reference cannot be an active DecisionObject")
        if self.recommendation_available:
            raise ValueError("Retail Trader Experience API decision reference cannot expose recommendations")
        if self.action_available:
            raise ValueError("Retail Trader Experience API decision reference cannot expose actions")
        if self.confidence_available:
            raise ValueError("Retail Trader Experience API decision reference cannot expose confidence")
        if self.readiness_to_trade_available:
            raise ValueError("Retail Trader Experience API decision reference cannot expose readiness-to-trade")
        if self.broker_controls_available:
            raise ValueError("Retail Trader Experience API decision reference cannot expose broker controls")
        if self.execution_available:
            raise ValueError("Retail Trader Experience API decision reference cannot expose execution")
        if self.display_ready:
            raise ValueError("Retail Trader Experience API decision reference cannot be display-ready")
        return self


class RetailTraderExperienceAPISafetyReference(BaseModel):
    reference_id: str
    boundary_policy_id: str | None = None
    required: bool = True
    safety_passed: bool = False
    approval_granted: bool = False
    override_granted: bool = False
    readiness_to_trade_allowed: bool = False
    broker_controls_allowed: bool = False
    execution_allowed: bool = False
    suitability_profiling_allowed: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience API safety reference text fields")

    @field_validator("boundary_policy_id")
    @classmethod
    def optional_text_fields_must_be_trimmed(cls, value: str | None) -> str | None:
        return _optional_trimmed(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def safety_reference_must_fail_closed(self) -> RetailTraderExperienceAPISafetyReference:
        if self.safety_passed:
            raise ValueError("Retail Trader Experience API safety reference cannot pass in Prompt 57")
        if self.approval_granted:
            raise ValueError("Retail Trader Experience API safety reference cannot grant approval")
        if self.override_granted:
            raise ValueError("Retail Trader Experience API safety reference cannot grant override")
        if self.readiness_to_trade_allowed:
            raise ValueError("Retail Trader Experience API safety reference cannot allow readiness-to-trade")
        if self.broker_controls_allowed:
            raise ValueError("Retail Trader Experience API safety reference cannot allow broker controls")
        if self.execution_allowed:
            raise ValueError("Retail Trader Experience API safety reference cannot allow execution")
        if self.suitability_profiling_allowed:
            raise ValueError("Retail Trader Experience API safety reference cannot allow suitability profiling")
        return self


def default_retail_trader_experience_api_persona_reference() -> RetailTraderExperienceAPIPersonaReference:
    return RetailTraderExperienceAPIPersonaReference(
        reference_id="retail-trader-experience-api-persona-reference-v1",
        persona_id="retail-trader-placeholder-reference",
    )


def default_retail_trader_experience_api_journey_reference() -> RetailTraderExperienceAPIJourneyReference:
    return RetailTraderExperienceAPIJourneyReference(
        reference_id="retail-trader-experience-api-journey-reference-v1",
        journey_id="retail-trader-journey-placeholder-reference",
    )


def default_retail_trader_experience_api_dashboard_reference() -> RetailTraderExperienceAPIDashboardReference:
    return RetailTraderExperienceAPIDashboardReference(
        reference_id="retail-trader-experience-api-dashboard-reference-v1",
        dashboard_id="retail-dashboard-placeholder-reference",
    )


def default_retail_trader_experience_api_decision_reference() -> RetailTraderExperienceAPIDecisionReference:
    return RetailTraderExperienceAPIDecisionReference(
        reference_id="retail-trader-experience-api-decision-reference-v1",
    )


def default_retail_trader_experience_api_safety_reference() -> RetailTraderExperienceAPISafetyReference:
    return RetailTraderExperienceAPISafetyReference(
        reference_id="retail-trader-experience-api-safety-reference-v1",
        boundary_policy_id="retail-trader-experience-api-boundary-policy-v1",
    )
