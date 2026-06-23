from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_dashboard_api.requests import (
    RetailDashboardAPISafetyLabel,
    RetailDashboardAPIUnavailableReason,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_dashboard_api_notes,
)


class RetailDashboardAPIUnavailableResponse(BaseModel):
    response_id: str
    unavailable: bool = True
    reason: RetailDashboardAPIUnavailableReason
    message: str
    api_contract_skeleton_only: bool = True
    active_ui_allowed: bool = False
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    readiness_to_trade_allowed: bool = False
    broker_controls_allowed: bool = False
    execution_allowed: bool = False
    approval_granted: bool = False
    override_granted: bool = False
    safety_label: RetailDashboardAPISafetyLabel = RetailDashboardAPISafetyLabel.UNAVAILABLE
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("response_id", "message", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard API unavailable response text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_dashboard_api_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def unavailable_response_must_fail_closed(self) -> RetailDashboardAPIUnavailableResponse:
        if not self.unavailable:
            raise ValueError("Retail Dashboard API skeleton responses must be unavailable")
        if self.reason == RetailDashboardAPIUnavailableReason.UNKNOWN:
            raise ValueError("UNKNOWN Retail Dashboard API unavailable reason is not allowed")
        if not self.api_contract_skeleton_only:
            raise ValueError("Retail Dashboard API responses must remain contract-skeleton-only")
        if self.active_ui_allowed:
            raise ValueError("Retail Dashboard API active UI is forbidden in Prompt 50")
        if self.recommendations_allowed:
            raise ValueError("Retail Dashboard API recommendations are forbidden in Prompt 50")
        if self.action_generation_allowed:
            raise ValueError("Retail Dashboard API action generation is forbidden in Prompt 50")
        if self.confidence_scoring_allowed:
            raise ValueError("Retail Dashboard API confidence scoring is forbidden in Prompt 50")
        if self.decision_object_generation_allowed:
            raise ValueError("Retail Dashboard API DecisionObject generation is forbidden in Prompt 50")
        if self.readiness_to_trade_allowed:
            raise ValueError("Retail Dashboard API readiness-to-trade is forbidden in Prompt 50")
        if self.broker_controls_allowed:
            raise ValueError("Retail Dashboard API broker controls are forbidden in Prompt 50")
        if self.execution_allowed:
            raise ValueError("Retail Dashboard API execution is forbidden in Prompt 50")
        if self.approval_granted:
            raise ValueError("Retail Dashboard API approval cannot be granted in Prompt 50")
        if self.override_granted:
            raise ValueError("Retail Dashboard API override cannot be granted in Prompt 50")
        if self.safety_label == RetailDashboardAPISafetyLabel.UNKNOWN:
            raise ValueError("Retail Dashboard API safety label cannot be UNKNOWN")
        return self


def default_retail_dashboard_api_unavailable_response(
    reason: RetailDashboardAPIUnavailableReason = RetailDashboardAPIUnavailableReason.API_CONTRACT_SKELETON_ONLY,
) -> RetailDashboardAPIUnavailableResponse:
    return RetailDashboardAPIUnavailableResponse(
        response_id="retail-dashboard-api-unavailable-response-v1",
        reason=reason,
        message=(
            "Retail Dashboard API is an API contract skeleton only and returns unavailable responses in Prompt 50."
        ),
        notes=[
            "Unavailable-by-default; not active UI, not a recommendation, not readiness-to-trade, and not execution.",
        ],
    )
