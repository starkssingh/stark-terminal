from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator


class RetailTraderExperienceDisplayStage(StrEnum):
    DISPLAY_CONTRACT_SKELETON = "DISPLAY_CONTRACT_SKELETON"
    UNAVAILABLE_ONLY = "UNAVAILABLE_ONLY"
    PERSONA_PLACEHOLDERS = "PERSONA_PLACEHOLDERS"
    JOURNEY_PLACEHOLDERS = "JOURNEY_PLACEHOLDERS"
    ACTIVE_UI_PLANNED = "ACTIVE_UI_PLANNED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class RetailTraderExperienceDisplayPersonaKind(StrEnum):
    RETAIL_TRADER_VISUAL_PLACEHOLDER = "RETAIL_TRADER_VISUAL_PLACEHOLDER"
    INTRADAY_TRADER_VISUAL_PLACEHOLDER = "INTRADAY_TRADER_VISUAL_PLACEHOLDER"
    SWING_TRADER_VISUAL_PLACEHOLDER = "SWING_TRADER_VISUAL_PLACEHOLDER"
    OPTIONS_CONTEXT_VISUAL_PLACEHOLDER = "OPTIONS_CONTEXT_VISUAL_PLACEHOLDER"
    RISK_AWARE_BEGINNER_VISUAL_PLACEHOLDER = "RISK_AWARE_BEGINNER_VISUAL_PLACEHOLDER"
    QUANT_CURIOUS_TRADER_VISUAL_PLACEHOLDER = "QUANT_CURIOUS_TRADER_VISUAL_PLACEHOLDER"
    UNKNOWN = "UNKNOWN"


class RetailTraderExperienceDisplayJourneyKind(StrEnum):
    ONBOARDING_VISUAL_PLACEHOLDER = "ONBOARDING_VISUAL_PLACEHOLDER"
    INSTRUMENT_REVIEW_VISUAL_PLACEHOLDER = "INSTRUMENT_REVIEW_VISUAL_PLACEHOLDER"
    DASHBOARD_CONTEXT_VISUAL_PLACEHOLDER = "DASHBOARD_CONTEXT_VISUAL_PLACEHOLDER"
    SAFETY_CONTEXT_VISUAL_PLACEHOLDER = "SAFETY_CONTEXT_VISUAL_PLACEHOLDER"
    EVIDENCE_REVIEW_VISUAL_PLACEHOLDER = "EVIDENCE_REVIEW_VISUAL_PLACEHOLDER"
    HUMAN_REVIEW_VISUAL_PLACEHOLDER = "HUMAN_REVIEW_VISUAL_PLACEHOLDER"
    UNAVAILABLE_NOTICE = "UNAVAILABLE_NOTICE"
    UNKNOWN = "UNKNOWN"


class RetailTraderExperienceDisplaySectionKind(StrEnum):
    HEADER = "HEADER"
    OVERVIEW = "OVERVIEW"
    TRADER_CONTEXT = "TRADER_CONTEXT"
    INSTRUMENT_CONTEXT = "INSTRUMENT_CONTEXT"
    DASHBOARD_CONTEXT = "DASHBOARD_CONTEXT"
    DATA_QUALITY_CONTEXT = "DATA_QUALITY_CONTEXT"
    SAFETY_CONTEXT = "SAFETY_CONTEXT"
    EDUCATIONAL_CONTEXT = "EDUCATIONAL_CONTEXT"
    HUMAN_REVIEW_CONTEXT = "HUMAN_REVIEW_CONTEXT"
    UNAVAILABLE_NOTICE = "UNAVAILABLE_NOTICE"
    UNKNOWN = "UNKNOWN"


class RetailTraderExperienceDisplayWidgetKind(StrEnum):
    PLACEHOLDER = "PLACEHOLDER"
    PERSONA_PLACEHOLDER = "PERSONA_PLACEHOLDER"
    JOURNEY_PLACEHOLDER = "JOURNEY_PLACEHOLDER"
    TRADER_CONTEXT_PLACEHOLDER = "TRADER_CONTEXT_PLACEHOLDER"
    DASHBOARD_CONTEXT_PLACEHOLDER = "DASHBOARD_CONTEXT_PLACEHOLDER"
    DATA_QUALITY_PLACEHOLDER = "DATA_QUALITY_PLACEHOLDER"
    SAFETY_PLACEHOLDER = "SAFETY_PLACEHOLDER"
    EDUCATIONAL_PLACEHOLDER = "EDUCATIONAL_PLACEHOLDER"
    REVIEW_PLACEHOLDER = "REVIEW_PLACEHOLDER"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"


class RetailTraderExperienceDisplayBadgeKind(StrEnum):
    PLANNING_ONLY = "PLANNING_ONLY"
    UNAVAILABLE = "UNAVAILABLE"
    NOT_ACTIVE_UI = "NOT_ACTIVE_UI"
    NOT_A_RECOMMENDATION = "NOT_A_RECOMMENDATION"
    NOT_READINESS_TO_TRADE = "NOT_READINESS_TO_TRADE"
    NO_BROKER_CONTROL = "NO_BROKER_CONTROL"
    NO_EXECUTION = "NO_EXECUTION"
    NOT_SUITABILITY_PROFILING = "NOT_SUITABILITY_PROFILING"
    UNKNOWN = "UNKNOWN"


class RetailTraderExperienceDisplaySafetyLabel(StrEnum):
    DISPLAY_CONTRACT_ONLY = "DISPLAY_CONTRACT_ONLY"
    NOT_ACTIVE_UI = "NOT_ACTIVE_UI"
    NOT_A_RECOMMENDATION = "NOT_A_RECOMMENDATION"
    NOT_READINESS_TO_TRADE = "NOT_READINESS_TO_TRADE"
    NO_BROKER_CONTROL = "NO_BROKER_CONTROL"
    NO_EXECUTION = "NO_EXECUTION"
    NOT_SUITABILITY_PROFILING = "NOT_SUITABILITY_PROFILING"
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


def sanitize_retail_trader_experience_display_notes(values: list[str]) -> list[str]:
    sanitized: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized:
            sanitized.append(normalized)
    return sanitized


RETAIL_TRADER_EXPERIENCE_DISPLAY_FORBIDDEN_OUTPUTS = [
    "active UI",
    "frontend_components",
    "desktop_components",
    "recommendation_cards_or_widgets",
    "action_generation",
    "confidence_scoring",
    "DecisionObject_generation_or_display",
    "readiness-to-trade",
    "broker_controls",
    "execution_apis",
    "approval_controls",
    "override_controls",
    "suitability_profiling",
]


class RetailTraderExperienceDisplayContractMetadata(BaseModel):
    contract_id: str
    service_name: str = "stark-terminal-retail-trader-experience-display"
    stage: RetailTraderExperienceDisplayStage = (
        RetailTraderExperienceDisplayStage.DISPLAY_CONTRACT_SKELETON
    )
    persona_kinds: list[RetailTraderExperienceDisplayPersonaKind]
    journey_kinds: list[RetailTraderExperienceDisplayJourneyKind]
    section_kinds: list[RetailTraderExperienceDisplaySectionKind]
    widget_kinds: list[RetailTraderExperienceDisplayWidgetKind]
    badge_kinds: list[RetailTraderExperienceDisplayBadgeKind]
    active_ui_allowed: bool = False
    frontend_components_allowed: bool = False
    desktop_components_allowed: bool = False
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    readiness_to_trade_allowed: bool = False
    broker_controls_allowed: bool = False
    execution_allowed: bool = False
    approval_allowed: bool = False
    override_allowed: bool = False
    suitability_profiling_allowed: bool = False
    returns_unavailable_by_default: bool = True
    forbidden_outputs: list[str]
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("contract_id", "service_name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience display contract metadata text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def contract_metadata_must_fail_closed(self) -> RetailTraderExperienceDisplayContractMetadata:
        if self.stage == RetailTraderExperienceDisplayStage.UNKNOWN:
            raise ValueError("UNKNOWN Retail Trader Experience Display stage is not allowed")
        if not self.persona_kinds or RetailTraderExperienceDisplayPersonaKind.UNKNOWN in self.persona_kinds:
            raise ValueError("Retail Trader Experience Display metadata requires known persona kinds")
        if not self.journey_kinds or RetailTraderExperienceDisplayJourneyKind.UNKNOWN in self.journey_kinds:
            raise ValueError("Retail Trader Experience Display metadata requires known journey kinds")
        if not self.section_kinds or RetailTraderExperienceDisplaySectionKind.UNKNOWN in self.section_kinds:
            raise ValueError("Retail Trader Experience Display metadata requires known section kinds")
        if not self.widget_kinds or RetailTraderExperienceDisplayWidgetKind.UNKNOWN in self.widget_kinds:
            raise ValueError("Retail Trader Experience Display metadata requires known widget kinds")
        if not self.badge_kinds or RetailTraderExperienceDisplayBadgeKind.UNKNOWN in self.badge_kinds:
            raise ValueError("Retail Trader Experience Display metadata requires known badge kinds")
        dangerous_flags = {
            "active UI": self.active_ui_allowed,
            "frontend components": self.frontend_components_allowed,
            "desktop components": self.desktop_components_allowed,
            "recommendations": self.recommendations_allowed,
            "action generation": self.action_generation_allowed,
            "confidence scoring": self.confidence_scoring_allowed,
            "DecisionObject generation": self.decision_object_generation_allowed,
            "readiness-to-trade": self.readiness_to_trade_allowed,
            "broker controls": self.broker_controls_allowed,
            "execution": self.execution_allowed,
            "approval": self.approval_allowed,
            "override": self.override_allowed,
            "suitability profiling": self.suitability_profiling_allowed,
        }
        enabled = [name for name, enabled_now in dangerous_flags.items() if enabled_now]
        if enabled:
            raise ValueError(f"Retail Trader Experience Display forbids: {', '.join(enabled)}")
        if not self.returns_unavailable_by_default:
            raise ValueError("Retail Trader Experience Display skeleton must return unavailable by default")
        required_terms = [
            "active ui",
            "frontend",
            "desktop",
            "recommendation",
            "action",
            "confidence",
            "decisionobject",
            "readiness-to-trade",
            "broker",
            "execution",
            "approval",
            "override",
            "suitability",
        ]
        normalized_outputs = " ".join(self.forbidden_outputs).lower().replace("_", " ")
        missing = [term for term in required_terms if term not in normalized_outputs]
        if missing:
            raise ValueError(f"forbidden outputs missing required concepts: {', '.join(missing)}")
        return self


def default_retail_trader_experience_display_contract_metadata() -> (
    RetailTraderExperienceDisplayContractMetadata
):
    return RetailTraderExperienceDisplayContractMetadata(
        contract_id="retail-trader-experience-display-contract-metadata-v1",
        persona_kinds=[
            RetailTraderExperienceDisplayPersonaKind.RETAIL_TRADER_VISUAL_PLACEHOLDER,
            RetailTraderExperienceDisplayPersonaKind.INTRADAY_TRADER_VISUAL_PLACEHOLDER,
            RetailTraderExperienceDisplayPersonaKind.SWING_TRADER_VISUAL_PLACEHOLDER,
            RetailTraderExperienceDisplayPersonaKind.OPTIONS_CONTEXT_VISUAL_PLACEHOLDER,
            RetailTraderExperienceDisplayPersonaKind.RISK_AWARE_BEGINNER_VISUAL_PLACEHOLDER,
            RetailTraderExperienceDisplayPersonaKind.QUANT_CURIOUS_TRADER_VISUAL_PLACEHOLDER,
        ],
        journey_kinds=[
            RetailTraderExperienceDisplayJourneyKind.ONBOARDING_VISUAL_PLACEHOLDER,
            RetailTraderExperienceDisplayJourneyKind.INSTRUMENT_REVIEW_VISUAL_PLACEHOLDER,
            RetailTraderExperienceDisplayJourneyKind.DASHBOARD_CONTEXT_VISUAL_PLACEHOLDER,
            RetailTraderExperienceDisplayJourneyKind.SAFETY_CONTEXT_VISUAL_PLACEHOLDER,
            RetailTraderExperienceDisplayJourneyKind.EVIDENCE_REVIEW_VISUAL_PLACEHOLDER,
            RetailTraderExperienceDisplayJourneyKind.HUMAN_REVIEW_VISUAL_PLACEHOLDER,
            RetailTraderExperienceDisplayJourneyKind.UNAVAILABLE_NOTICE,
        ],
        section_kinds=[
            RetailTraderExperienceDisplaySectionKind.HEADER,
            RetailTraderExperienceDisplaySectionKind.OVERVIEW,
            RetailTraderExperienceDisplaySectionKind.TRADER_CONTEXT,
            RetailTraderExperienceDisplaySectionKind.INSTRUMENT_CONTEXT,
            RetailTraderExperienceDisplaySectionKind.DASHBOARD_CONTEXT,
            RetailTraderExperienceDisplaySectionKind.DATA_QUALITY_CONTEXT,
            RetailTraderExperienceDisplaySectionKind.SAFETY_CONTEXT,
            RetailTraderExperienceDisplaySectionKind.EDUCATIONAL_CONTEXT,
            RetailTraderExperienceDisplaySectionKind.HUMAN_REVIEW_CONTEXT,
            RetailTraderExperienceDisplaySectionKind.UNAVAILABLE_NOTICE,
        ],
        widget_kinds=[
            RetailTraderExperienceDisplayWidgetKind.PLACEHOLDER,
            RetailTraderExperienceDisplayWidgetKind.PERSONA_PLACEHOLDER,
            RetailTraderExperienceDisplayWidgetKind.JOURNEY_PLACEHOLDER,
            RetailTraderExperienceDisplayWidgetKind.TRADER_CONTEXT_PLACEHOLDER,
            RetailTraderExperienceDisplayWidgetKind.DASHBOARD_CONTEXT_PLACEHOLDER,
            RetailTraderExperienceDisplayWidgetKind.DATA_QUALITY_PLACEHOLDER,
            RetailTraderExperienceDisplayWidgetKind.SAFETY_PLACEHOLDER,
            RetailTraderExperienceDisplayWidgetKind.EDUCATIONAL_PLACEHOLDER,
            RetailTraderExperienceDisplayWidgetKind.REVIEW_PLACEHOLDER,
            RetailTraderExperienceDisplayWidgetKind.UNAVAILABLE,
        ],
        badge_kinds=[
            RetailTraderExperienceDisplayBadgeKind.PLANNING_ONLY,
            RetailTraderExperienceDisplayBadgeKind.UNAVAILABLE,
            RetailTraderExperienceDisplayBadgeKind.NOT_ACTIVE_UI,
            RetailTraderExperienceDisplayBadgeKind.NOT_A_RECOMMENDATION,
            RetailTraderExperienceDisplayBadgeKind.NOT_READINESS_TO_TRADE,
            RetailTraderExperienceDisplayBadgeKind.NO_BROKER_CONTROL,
            RetailTraderExperienceDisplayBadgeKind.NO_EXECUTION,
            RetailTraderExperienceDisplayBadgeKind.NOT_SUITABILITY_PROFILING,
        ],
        forbidden_outputs=list(RETAIL_TRADER_EXPERIENCE_DISPLAY_FORBIDDEN_OUTPUTS),
    )
