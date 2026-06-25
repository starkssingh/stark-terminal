from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_trader_experience.planning import _non_empty_text, _utc_datetime, _utc_now


class RetailTraderExperienceDashboardReference(BaseModel):
    reference_id: str
    source_name: str
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

    @field_validator("reference_id", "source_name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader dashboard reference text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def dashboard_reference_must_fail_closed(self) -> RetailTraderExperienceDashboardReference:
        if self.active_dashboard:
            raise ValueError("Retail Trader Experience dashboard references cannot be active dashboards")
        if self.active_ui:
            raise ValueError("Retail Trader Experience dashboard references cannot be active UI")
        if self.recommendation_available:
            raise ValueError("Retail Trader Experience dashboard references cannot expose recommendations")
        if self.readiness_to_trade_available:
            raise ValueError("Retail Trader Experience dashboard references cannot expose readiness-to-trade")
        if self.broker_controls_available:
            raise ValueError("Retail Trader Experience dashboard references cannot expose broker controls")
        if self.execution_available:
            raise ValueError("Retail Trader Experience dashboard references cannot expose execution")
        if self.display_ready:
            raise ValueError("Retail Trader Experience dashboard references are not display-ready in Prompt 56")
        return self


class RetailTraderExperienceDecisionReference(BaseModel):
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
        return _non_empty_text(value, "retail trader decision reference text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def decision_reference_must_fail_closed(self) -> RetailTraderExperienceDecisionReference:
        if self.active_decision_object:
            raise ValueError("Retail Trader Experience active DecisionObject references are forbidden")
        if self.recommendation_available:
            raise ValueError("Retail Trader Experience recommendation references are forbidden")
        if self.action_available:
            raise ValueError("Retail Trader Experience action references are forbidden")
        if self.confidence_available:
            raise ValueError("Retail Trader Experience confidence references are forbidden")
        if self.readiness_to_trade_available:
            raise ValueError("Retail Trader Experience readiness-to-trade references are forbidden")
        if self.broker_controls_available:
            raise ValueError("Retail Trader Experience broker control references are forbidden")
        if self.execution_available:
            raise ValueError("Retail Trader Experience execution references are forbidden")
        if self.display_ready:
            raise ValueError("Retail Trader Experience decision references are not display-ready in Prompt 56")
        return self


class RetailTraderExperienceSafetyReference(BaseModel):
    reference_id: str
    boundary_policy_id: str | None = None
    required: bool = True
    safety_passed: bool = False
    approval_granted: bool = False
    override_granted: bool = False
    readiness_to_trade_allowed: bool = False
    broker_controls_allowed: bool = False
    execution_allowed: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader safety reference text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def safety_reference_must_fail_closed(self) -> RetailTraderExperienceSafetyReference:
        if self.safety_passed:
            raise ValueError("Retail Trader Experience safety references cannot mark safety passed")
        if self.approval_granted:
            raise ValueError("Retail Trader Experience safety references cannot grant approval")
        if self.override_granted:
            raise ValueError("Retail Trader Experience safety references cannot grant override")
        if self.readiness_to_trade_allowed:
            raise ValueError("Retail Trader Experience safety references cannot allow readiness-to-trade")
        if self.broker_controls_allowed:
            raise ValueError("Retail Trader Experience safety references cannot allow broker controls")
        if self.execution_allowed:
            raise ValueError("Retail Trader Experience safety references cannot allow execution")
        return self


def default_retail_trader_experience_dashboard_reference() -> RetailTraderExperienceDashboardReference:
    return RetailTraderExperienceDashboardReference(
        reference_id="retail-trader-experience-dashboard-reference-placeholder-v1",
        source_name="retail-dashboard-contract-placeholder",
    )


def default_retail_trader_experience_decision_reference() -> RetailTraderExperienceDecisionReference:
    return RetailTraderExperienceDecisionReference(
        reference_id="retail-trader-experience-decision-reference-placeholder-v1",
        required=False,
    )


def default_retail_trader_experience_safety_reference() -> RetailTraderExperienceSafetyReference:
    return RetailTraderExperienceSafetyReference(
        reference_id="retail-trader-experience-safety-reference-placeholder-v1",
        boundary_policy_id="retail-trader-experience-planning-policy-v1",
    )
