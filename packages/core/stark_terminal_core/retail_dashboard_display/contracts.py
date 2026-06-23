from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator


class RetailDashboardDisplayStage(StrEnum):
    DISPLAY_CONTRACT_SKELETON = "DISPLAY_CONTRACT_SKELETON"
    UNAVAILABLE_ONLY = "UNAVAILABLE_ONLY"
    LAYOUT_PLACEHOLDERS = "LAYOUT_PLACEHOLDERS"
    WIDGET_PLACEHOLDERS = "WIDGET_PLACEHOLDERS"
    ACTIVE_UI_PLANNED = "ACTIVE_UI_PLANNED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class RetailDashboardLayoutKind(StrEnum):
    DESKTOP_SHELL_PLACEHOLDER = "DESKTOP_SHELL_PLACEHOLDER"
    RETAIL_OVERVIEW_PLACEHOLDER = "RETAIL_OVERVIEW_PLACEHOLDER"
    INSTRUMENT_DETAIL_PLACEHOLDER = "INSTRUMENT_DETAIL_PLACEHOLDER"
    RISK_CONTEXT_PLACEHOLDER = "RISK_CONTEXT_PLACEHOLDER"
    SAFETY_PLACEHOLDER = "SAFETY_PLACEHOLDER"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"


class RetailDashboardWidgetKind(StrEnum):
    PLACEHOLDER = "PLACEHOLDER"
    DATA_QUALITY_WIDGET_PLACEHOLDER = "DATA_QUALITY_WIDGET_PLACEHOLDER"
    MARKET_CONTEXT_WIDGET_PLACEHOLDER = "MARKET_CONTEXT_WIDGET_PLACEHOLDER"
    DECISION_PLACEHOLDER = "DECISION_PLACEHOLDER"
    RISK_PLACEHOLDER = "RISK_PLACEHOLDER"
    SAFETY_PLACEHOLDER = "SAFETY_PLACEHOLDER"
    REVIEW_PLACEHOLDER = "REVIEW_PLACEHOLDER"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"


class RetailDashboardVisualSectionKind(StrEnum):
    HEADER = "HEADER"
    OVERVIEW = "OVERVIEW"
    DATA_QUALITY = "DATA_QUALITY"
    MARKET_CONTEXT = "MARKET_CONTEXT"
    DECISION_PLACEHOLDER = "DECISION_PLACEHOLDER"
    RISK_CONTEXT = "RISK_CONTEXT"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    SAFETY_STATUS = "SAFETY_STATUS"
    UNAVAILABLE_NOTICE = "UNAVAILABLE_NOTICE"
    UNKNOWN = "UNKNOWN"


class RetailDashboardDisplayBadgeKind(StrEnum):
    PLANNING_ONLY = "PLANNING_ONLY"
    UNAVAILABLE = "UNAVAILABLE"
    NOT_ACTIVE_UI = "NOT_ACTIVE_UI"
    NOT_A_RECOMMENDATION = "NOT_A_RECOMMENDATION"
    NOT_READINESS_TO_TRADE = "NOT_READINESS_TO_TRADE"
    NO_BROKER_CONTROL = "NO_BROKER_CONTROL"
    NO_EXECUTION = "NO_EXECUTION"
    UNKNOWN = "UNKNOWN"


class RetailDashboardDisplaySafetyLabel(StrEnum):
    DISPLAY_CONTRACT_ONLY = "DISPLAY_CONTRACT_ONLY"
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


def sanitize_retail_dashboard_display_notes(values: list[str]) -> list[str]:
    sanitized: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized:
            sanitized.append(normalized)
    return sanitized


RETAIL_DASHBOARD_DISPLAY_FORBIDDEN_OUTPUTS = [
    "active UI",
    "recommendation_cards",
    "action_generation",
    "confidence_scoring",
    "DecisionObject_generation_or_display",
    "readiness-to-trade",
    "broker_controls",
    "execution_apis",
    "approval_controls",
    "override_controls",
]


class RetailDashboardDisplayContractMetadata(BaseModel):
    contract_id: str
    service_name: str = "stark-terminal-retail-dashboard-display"
    stage: RetailDashboardDisplayStage = RetailDashboardDisplayStage.DISPLAY_CONTRACT_SKELETON
    layout_kinds: list[RetailDashboardLayoutKind]
    widget_kinds: list[RetailDashboardWidgetKind]
    section_kinds: list[RetailDashboardVisualSectionKind]
    badge_kinds: list[RetailDashboardDisplayBadgeKind]
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
    returns_unavailable_by_default: bool = True
    forbidden_outputs: list[str]
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("contract_id", "service_name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard display contract metadata text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def contract_metadata_must_fail_closed(self) -> RetailDashboardDisplayContractMetadata:
        if self.stage == RetailDashboardDisplayStage.UNKNOWN:
            raise ValueError("UNKNOWN Retail Dashboard Display stage is not allowed")
        if not self.layout_kinds:
            raise ValueError("Retail Dashboard Display metadata requires layout kinds")
        if RetailDashboardLayoutKind.UNKNOWN in self.layout_kinds:
            raise ValueError("UNKNOWN Retail Dashboard layout kind is not allowed")
        if not self.widget_kinds:
            raise ValueError("Retail Dashboard Display metadata requires widget kinds")
        if RetailDashboardWidgetKind.UNKNOWN in self.widget_kinds:
            raise ValueError("UNKNOWN Retail Dashboard widget kind is not allowed")
        if not self.section_kinds:
            raise ValueError("Retail Dashboard Display metadata requires visual section kinds")
        if RetailDashboardVisualSectionKind.UNKNOWN in self.section_kinds:
            raise ValueError("UNKNOWN Retail Dashboard visual section kind is not allowed")
        if not self.badge_kinds:
            raise ValueError("Retail Dashboard Display metadata requires badge kinds")
        if RetailDashboardDisplayBadgeKind.UNKNOWN in self.badge_kinds:
            raise ValueError("UNKNOWN Retail Dashboard display badge kind is not allowed")
        if self.active_ui_allowed:
            raise ValueError("Retail Dashboard Display active UI is forbidden in Prompt 51")
        if self.recommendations_allowed:
            raise ValueError("Retail Dashboard Display recommendations are forbidden in Prompt 51")
        if self.action_generation_allowed:
            raise ValueError("Retail Dashboard Display action generation is forbidden in Prompt 51")
        if self.confidence_scoring_allowed:
            raise ValueError("Retail Dashboard Display confidence scoring is forbidden in Prompt 51")
        if self.decision_object_generation_allowed:
            raise ValueError("Retail Dashboard Display DecisionObject generation is forbidden in Prompt 51")
        if self.readiness_to_trade_allowed:
            raise ValueError("Retail Dashboard Display readiness-to-trade is forbidden in Prompt 51")
        if self.broker_controls_allowed:
            raise ValueError("Retail Dashboard Display broker controls are forbidden in Prompt 51")
        if self.execution_allowed:
            raise ValueError("Retail Dashboard Display execution is forbidden in Prompt 51")
        if self.approval_allowed:
            raise ValueError("Retail Dashboard Display approval is forbidden in Prompt 51")
        if self.override_allowed:
            raise ValueError("Retail Dashboard Display override is forbidden in Prompt 51")
        if not self.returns_unavailable_by_default:
            raise ValueError("Retail Dashboard Display skeleton must return unavailable by default")
        required_terms = [
            "active ui",
            "recommendation",
            "action",
            "confidence",
            "decisionobject",
            "readiness-to-trade",
            "broker",
            "execution",
            "approval",
            "override",
        ]
        normalized_outputs = " ".join(self.forbidden_outputs).lower().replace("_", " ")
        missing = [term for term in required_terms if term not in normalized_outputs]
        if missing:
            raise ValueError(f"forbidden outputs missing required concepts: {', '.join(missing)}")
        return self


def default_retail_dashboard_display_contract_metadata() -> RetailDashboardDisplayContractMetadata:
    return RetailDashboardDisplayContractMetadata(
        contract_id="retail-dashboard-display-contract-metadata-v1",
        layout_kinds=[
            RetailDashboardLayoutKind.DESKTOP_SHELL_PLACEHOLDER,
            RetailDashboardLayoutKind.RETAIL_OVERVIEW_PLACEHOLDER,
            RetailDashboardLayoutKind.INSTRUMENT_DETAIL_PLACEHOLDER,
            RetailDashboardLayoutKind.RISK_CONTEXT_PLACEHOLDER,
            RetailDashboardLayoutKind.SAFETY_PLACEHOLDER,
            RetailDashboardLayoutKind.UNAVAILABLE,
        ],
        widget_kinds=[
            RetailDashboardWidgetKind.PLACEHOLDER,
            RetailDashboardWidgetKind.DATA_QUALITY_WIDGET_PLACEHOLDER,
            RetailDashboardWidgetKind.MARKET_CONTEXT_WIDGET_PLACEHOLDER,
            RetailDashboardWidgetKind.DECISION_PLACEHOLDER,
            RetailDashboardWidgetKind.RISK_PLACEHOLDER,
            RetailDashboardWidgetKind.SAFETY_PLACEHOLDER,
            RetailDashboardWidgetKind.REVIEW_PLACEHOLDER,
            RetailDashboardWidgetKind.UNAVAILABLE,
        ],
        section_kinds=[
            RetailDashboardVisualSectionKind.HEADER,
            RetailDashboardVisualSectionKind.OVERVIEW,
            RetailDashboardVisualSectionKind.DATA_QUALITY,
            RetailDashboardVisualSectionKind.MARKET_CONTEXT,
            RetailDashboardVisualSectionKind.DECISION_PLACEHOLDER,
            RetailDashboardVisualSectionKind.RISK_CONTEXT,
            RetailDashboardVisualSectionKind.HUMAN_REVIEW,
            RetailDashboardVisualSectionKind.SAFETY_STATUS,
            RetailDashboardVisualSectionKind.UNAVAILABLE_NOTICE,
        ],
        badge_kinds=[
            RetailDashboardDisplayBadgeKind.PLANNING_ONLY,
            RetailDashboardDisplayBadgeKind.UNAVAILABLE,
            RetailDashboardDisplayBadgeKind.NOT_ACTIVE_UI,
            RetailDashboardDisplayBadgeKind.NOT_A_RECOMMENDATION,
            RetailDashboardDisplayBadgeKind.NOT_READINESS_TO_TRADE,
            RetailDashboardDisplayBadgeKind.NO_BROKER_CONTROL,
            RetailDashboardDisplayBadgeKind.NO_EXECUTION,
        ],
        forbidden_outputs=list(RETAIL_DASHBOARD_DISPLAY_FORBIDDEN_OUTPUTS),
    )
