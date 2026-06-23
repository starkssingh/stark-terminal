from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_dashboard_api.requests import _non_empty_text, _utc_datetime, _utc_now


class RetailDashboardAPIDataReference(BaseModel):
    reference_id: str
    source_name: str
    required: bool = True
    real_market_data: bool = False
    live_data: bool = False
    validated: bool = False
    display_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("reference_id", "source_name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard API data reference text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def data_reference_must_fail_closed(self) -> RetailDashboardAPIDataReference:
        if self.real_market_data:
            raise ValueError("Retail Dashboard API data reference cannot represent real market data in Prompt 50")
        if self.live_data:
            raise ValueError("Retail Dashboard API data reference cannot represent live data in Prompt 50")
        if self.display_ready:
            raise ValueError("Retail Dashboard API data reference cannot be display-ready in Prompt 50")
        return self


class RetailDashboardAPIDecisionReference(BaseModel):
    reference_id: str
    decision_object_id: str | None = None
    required: bool = False
    active_decision_object: bool = False
    recommendation_available: bool = False
    action_available: bool = False
    confidence_available: bool = False
    readiness_to_trade_available: bool = False
    display_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard API decision reference text fields")

    @field_validator("decision_object_id")
    @classmethod
    def optional_text_fields_must_be_trimmed(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def decision_reference_must_fail_closed(self) -> RetailDashboardAPIDecisionReference:
        if self.active_decision_object:
            raise ValueError("Retail Dashboard API decision reference cannot be an active DecisionObject")
        if self.recommendation_available:
            raise ValueError("Retail Dashboard API decision reference cannot expose recommendations")
        if self.action_available:
            raise ValueError("Retail Dashboard API decision reference cannot expose actions")
        if self.confidence_available:
            raise ValueError("Retail Dashboard API decision reference cannot expose confidence")
        if self.readiness_to_trade_available:
            raise ValueError("Retail Dashboard API decision reference cannot expose readiness-to-trade")
        if self.display_ready:
            raise ValueError("Retail Dashboard API decision reference cannot be display-ready")
        return self


class RetailDashboardAPISafetyReference(BaseModel):
    reference_id: str
    boundary_policy_id: str | None = None
    required: bool = True
    safety_passed: bool = False
    approval_granted: bool = False
    override_granted: bool = False
    execution_allowed: bool = False
    broker_controls_allowed: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard API safety reference text fields")

    @field_validator("boundary_policy_id")
    @classmethod
    def optional_text_fields_must_be_trimmed(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def safety_reference_must_fail_closed(self) -> RetailDashboardAPISafetyReference:
        if self.safety_passed:
            raise ValueError("Retail Dashboard API safety reference cannot pass in Prompt 50")
        if self.approval_granted:
            raise ValueError("Retail Dashboard API safety reference cannot grant approval")
        if self.override_granted:
            raise ValueError("Retail Dashboard API safety reference cannot grant override")
        if self.execution_allowed:
            raise ValueError("Retail Dashboard API safety reference cannot allow execution")
        if self.broker_controls_allowed:
            raise ValueError("Retail Dashboard API safety reference cannot allow broker controls")
        return self


def default_retail_dashboard_api_data_reference() -> RetailDashboardAPIDataReference:
    return RetailDashboardAPIDataReference(
        reference_id="retail-dashboard-api-data-reference-v1",
        source_name="retail-dashboard-data-reference-placeholder",
    )


def default_retail_dashboard_api_decision_reference() -> RetailDashboardAPIDecisionReference:
    return RetailDashboardAPIDecisionReference(
        reference_id="retail-dashboard-api-decision-reference-v1",
    )


def default_retail_dashboard_api_safety_reference() -> RetailDashboardAPISafetyReference:
    return RetailDashboardAPISafetyReference(
        reference_id="retail-dashboard-api-safety-reference-v1",
        boundary_policy_id="retail-dashboard-api-boundary-policy-v1",
    )
