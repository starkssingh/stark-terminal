from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_dashboard_api.references import (
    RetailDashboardAPIDataReference,
    RetailDashboardAPIDecisionReference,
    RetailDashboardAPISafetyReference,
    default_retail_dashboard_api_data_reference,
    default_retail_dashboard_api_decision_reference,
    default_retail_dashboard_api_safety_reference,
)
from stark_terminal_core.retail_dashboard_api.requests import (
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_dashboard_api_notes,
)
from stark_terminal_core.retail_dashboard_api.unavailable import (
    RetailDashboardAPIUnavailableResponse,
    default_retail_dashboard_api_unavailable_response,
)


class RetailDashboardAPIResponsePlaceholder(BaseModel):
    response_id: str
    request_id: str | None = None
    data_reference: RetailDashboardAPIDataReference
    decision_reference: RetailDashboardAPIDecisionReference
    safety_reference: RetailDashboardAPISafetyReference
    unavailable_response: RetailDashboardAPIUnavailableResponse
    api_contract_skeleton_only: bool = True
    active_ui_generated: bool = False
    recommendation_generated: bool = False
    action_generated: bool = False
    confidence_generated: bool = False
    decision_object_generated: bool = False
    readiness_to_trade_generated: bool = False
    broker_control_generated: bool = False
    execution_ready: bool = False
    approval_granted: bool = False
    override_granted: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("response_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard API response placeholder text fields")

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
        return sanitize_retail_dashboard_api_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def response_placeholder_must_fail_closed(self) -> RetailDashboardAPIResponsePlaceholder:
        if not self.api_contract_skeleton_only:
            raise ValueError("Retail Dashboard API response must remain contract-skeleton-only")
        if self.active_ui_generated:
            raise ValueError("Retail Dashboard API active UI generation is forbidden")
        if self.recommendation_generated:
            raise ValueError("Retail Dashboard API recommendation generation is forbidden")
        if self.action_generated:
            raise ValueError("Retail Dashboard API action generation is forbidden")
        if self.confidence_generated:
            raise ValueError("Retail Dashboard API confidence generation is forbidden")
        if self.decision_object_generated:
            raise ValueError("Retail Dashboard API DecisionObject generation is forbidden")
        if self.readiness_to_trade_generated:
            raise ValueError("Retail Dashboard API readiness-to-trade generation is forbidden")
        if self.broker_control_generated:
            raise ValueError("Retail Dashboard API broker control generation is forbidden")
        if self.execution_ready:
            raise ValueError("Retail Dashboard API execution readiness is forbidden")
        if self.approval_granted:
            raise ValueError("Retail Dashboard API approval cannot be granted")
        if self.override_granted:
            raise ValueError("Retail Dashboard API override cannot be granted")
        return self


def default_retail_dashboard_api_response_placeholder(
    request_id: str | None = None,
    data_reference: RetailDashboardAPIDataReference | None = None,
    decision_reference: RetailDashboardAPIDecisionReference | None = None,
    safety_reference: RetailDashboardAPISafetyReference | None = None,
    unavailable_response: RetailDashboardAPIUnavailableResponse | None = None,
) -> RetailDashboardAPIResponsePlaceholder:
    return RetailDashboardAPIResponsePlaceholder(
        response_id="retail-dashboard-api-response-placeholder-v1",
        request_id=request_id,
        data_reference=data_reference or default_retail_dashboard_api_data_reference(),
        decision_reference=decision_reference or default_retail_dashboard_api_decision_reference(),
        safety_reference=safety_reference or default_retail_dashboard_api_safety_reference(),
        unavailable_response=unavailable_response or default_retail_dashboard_api_unavailable_response(),
        notes=["Response placeholder contains references only and no generated outputs."],
    )
