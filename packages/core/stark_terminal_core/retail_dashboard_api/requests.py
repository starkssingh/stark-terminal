from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator


class RetailDashboardAPIStage(StrEnum):
    API_CONTRACT_SKELETON = "API_CONTRACT_SKELETON"
    UNAVAILABLE_ONLY = "UNAVAILABLE_ONLY"
    REFERENCE_PLACEHOLDERS = "REFERENCE_PLACEHOLDERS"
    ACTIVE_UI_PLANNED = "ACTIVE_UI_PLANNED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class RetailDashboardAPIRequestKind(StrEnum):
    DASHBOARD_OVERVIEW_REQUEST = "DASHBOARD_OVERVIEW_REQUEST"
    DASHBOARD_LAYOUT_REQUEST = "DASHBOARD_LAYOUT_REQUEST"
    DASHBOARD_SECTION_REQUEST = "DASHBOARD_SECTION_REQUEST"
    DASHBOARD_CARD_REQUEST = "DASHBOARD_CARD_REQUEST"
    DASHBOARD_REFERENCE_REQUEST = "DASHBOARD_REFERENCE_REQUEST"
    DASHBOARD_READINESS_REQUEST = "DASHBOARD_READINESS_REQUEST"
    UNKNOWN = "UNKNOWN"


class RetailDashboardAPIUnavailableReason(StrEnum):
    ACTIVE_UI_DISABLED = "ACTIVE_UI_DISABLED"
    RECOMMENDATIONS_DISABLED = "RECOMMENDATIONS_DISABLED"
    ACTION_GENERATION_DISABLED = "ACTION_GENERATION_DISABLED"
    CONFIDENCE_SCORING_DISABLED = "CONFIDENCE_SCORING_DISABLED"
    DECISION_OBJECT_GENERATION_DISABLED = "DECISION_OBJECT_GENERATION_DISABLED"
    READINESS_TO_TRADE_DISABLED = "READINESS_TO_TRADE_DISABLED"
    BROKER_CONTROLS_DISABLED = "BROKER_CONTROLS_DISABLED"
    EXECUTION_DISABLED = "EXECUTION_DISABLED"
    API_CONTRACT_SKELETON_ONLY = "API_CONTRACT_SKELETON_ONLY"
    UNKNOWN = "UNKNOWN"


class RetailDashboardAPISafetyLabel(StrEnum):
    API_CONTRACT_SKELETON_ONLY = "API_CONTRACT_SKELETON_ONLY"
    UNAVAILABLE = "UNAVAILABLE"
    NOT_ACTIVE_UI = "NOT_ACTIVE_UI"
    NOT_A_RECOMMENDATION = "NOT_A_RECOMMENDATION"
    NOT_READINESS_TO_TRADE = "NOT_READINESS_TO_TRADE"
    NO_BROKER_CONTROL = "NO_BROKER_CONTROL"
    NO_EXECUTION = "NO_EXECUTION"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _utc_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _non_empty_text(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} cannot be empty")
    return normalized


def sanitize_retail_dashboard_api_notes(values: list[str]) -> list[str]:
    sanitized: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized:
            sanitized.append(normalized)
    return sanitized


class RetailDashboardAPIRequestPlaceholder(BaseModel):
    request_id: str
    request_kind: RetailDashboardAPIRequestKind
    requested_sections: list[str] = Field(default_factory=list)
    requested_cards: list[str] = Field(default_factory=list)
    data_reference_required: bool = True
    decision_reference_required: bool = False
    safety_reference_required: bool = True
    active_ui_allowed: bool = False
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    readiness_to_trade_allowed: bool = False
    broker_controls_allowed: bool = False
    execution_allowed: bool = False
    approval_allowed: bool = False
    override_allowed: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("request_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard API request placeholder text fields")

    @field_validator("requested_sections", "requested_cards", "notes")
    @classmethod
    def list_fields_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_dashboard_api_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def request_placeholder_must_fail_closed(self) -> RetailDashboardAPIRequestPlaceholder:
        if self.request_kind == RetailDashboardAPIRequestKind.UNKNOWN:
            raise ValueError("UNKNOWN retail dashboard API request kind is not allowed")
        if not self.data_reference_required:
            raise ValueError("Retail Dashboard API data references are required in Prompt 50")
        if not self.safety_reference_required:
            raise ValueError("Retail Dashboard API safety references are required in Prompt 50")
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
        if self.approval_allowed:
            raise ValueError("Retail Dashboard API approval is forbidden in Prompt 50")
        if self.override_allowed:
            raise ValueError("Retail Dashboard API override is forbidden in Prompt 50")
        return self


def create_retail_dashboard_api_request_placeholder(
    request_id: str,
    request_kind: RetailDashboardAPIRequestKind = RetailDashboardAPIRequestKind.DASHBOARD_OVERVIEW_REQUEST,
    requested_sections: list[str] | None = None,
    requested_cards: list[str] | None = None,
    notes: list[str] | None = None,
) -> RetailDashboardAPIRequestPlaceholder:
    return RetailDashboardAPIRequestPlaceholder(
        request_id=request_id,
        request_kind=request_kind,
        requested_sections=list(requested_sections or []),
        requested_cards=list(requested_cards or []),
        notes=list(notes or ["API contract skeleton request placeholder; not an active UI request."]),
    )


def default_retail_dashboard_api_request_placeholder() -> RetailDashboardAPIRequestPlaceholder:
    return create_retail_dashboard_api_request_placeholder(
        request_id="retail-dashboard-api-request-placeholder-v1",
        request_kind=RetailDashboardAPIRequestKind.DASHBOARD_OVERVIEW_REQUEST,
        requested_sections=[
            "overview_placeholder",
            "data_reference_placeholder",
            "decision_reference_placeholder",
            "safety_reference_placeholder",
            "unavailable_response",
        ],
        requested_cards=[
            "placeholder_card",
            "data_quality_placeholder_card",
            "decision_placeholder_card",
            "safety_placeholder_card",
        ],
    )
