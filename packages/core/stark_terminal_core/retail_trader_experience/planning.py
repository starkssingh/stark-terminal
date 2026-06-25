from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator


class RetailTraderExperienceStage(StrEnum):
    PLANNING_AND_GUARDRAILS = "PLANNING_AND_GUARDRAILS"
    UNAVAILABLE_ONLY = "UNAVAILABLE_ONLY"
    PERSONA_PLACEHOLDERS = "PERSONA_PLACEHOLDERS"
    JOURNEY_PLACEHOLDERS = "JOURNEY_PLACEHOLDERS"
    ACTIVE_UI_PLANNED = "ACTIVE_UI_PLANNED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class RetailTraderPersonaKind(StrEnum):
    RETAIL_TRADER_PLACEHOLDER = "RETAIL_TRADER_PLACEHOLDER"
    INTRADAY_TRADER_PLACEHOLDER = "INTRADAY_TRADER_PLACEHOLDER"
    SWING_TRADER_PLACEHOLDER = "SWING_TRADER_PLACEHOLDER"
    OPTIONS_CONTEXT_PLACEHOLDER = "OPTIONS_CONTEXT_PLACEHOLDER"
    RISK_AWARE_BEGINNER_PLACEHOLDER = "RISK_AWARE_BEGINNER_PLACEHOLDER"
    QUANT_CURIOUS_TRADER_PLACEHOLDER = "QUANT_CURIOUS_TRADER_PLACEHOLDER"
    UNKNOWN = "UNKNOWN"


class RetailTraderJourneyKind(StrEnum):
    ONBOARDING_PLACEHOLDER = "ONBOARDING_PLACEHOLDER"
    INSTRUMENT_REVIEW_PLACEHOLDER = "INSTRUMENT_REVIEW_PLACEHOLDER"
    DASHBOARD_CONTEXT_REVIEW_PLACEHOLDER = "DASHBOARD_CONTEXT_REVIEW_PLACEHOLDER"
    SAFETY_CONTEXT_REVIEW_PLACEHOLDER = "SAFETY_CONTEXT_REVIEW_PLACEHOLDER"
    EVIDENCE_REVIEW_PLACEHOLDER = "EVIDENCE_REVIEW_PLACEHOLDER"
    HUMAN_REVIEW_PLACEHOLDER = "HUMAN_REVIEW_PLACEHOLDER"
    UNAVAILABLE_NOTICE = "UNAVAILABLE_NOTICE"
    UNKNOWN = "UNKNOWN"


class RetailTraderExperienceSectionKind(StrEnum):
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


class RetailTraderExperienceCardKind(StrEnum):
    PLACEHOLDER = "PLACEHOLDER"
    TRADER_CONTEXT_PLACEHOLDER = "TRADER_CONTEXT_PLACEHOLDER"
    INSTRUMENT_CONTEXT_PLACEHOLDER = "INSTRUMENT_CONTEXT_PLACEHOLDER"
    DASHBOARD_CONTEXT_PLACEHOLDER = "DASHBOARD_CONTEXT_PLACEHOLDER"
    DATA_QUALITY_PLACEHOLDER = "DATA_QUALITY_PLACEHOLDER"
    SAFETY_PLACEHOLDER = "SAFETY_PLACEHOLDER"
    EDUCATIONAL_PLACEHOLDER = "EDUCATIONAL_PLACEHOLDER"
    REVIEW_PLACEHOLDER = "REVIEW_PLACEHOLDER"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"


class RetailTraderExperienceForbiddenInteractionKind(StrEnum):
    RECOMMENDATION_CARD = "RECOMMENDATION_CARD"
    ACTION_BUTTON = "ACTION_BUTTON"
    CONFIDENCE_SCORE = "CONFIDENCE_SCORE"
    DECISION_OBJECT_DISPLAY = "DECISION_OBJECT_DISPLAY"
    READINESS_TO_TRADE_BADGE = "READINESS_TO_TRADE_BADGE"
    BROKER_CONTROL = "BROKER_CONTROL"
    ORDER_BUTTON = "ORDER_BUTTON"
    APPROVAL_CONTROL = "APPROVAL_CONTROL"
    OVERRIDE_CONTROL = "OVERRIDE_CONTROL"
    SUITABILITY_PROFILING = "SUITABILITY_PROFILING"
    LIVE_DATA_CONTROL = "LIVE_DATA_CONTROL"
    UNKNOWN = "UNKNOWN"


class RetailTraderExperienceSafetyLabel(StrEnum):
    PLANNING_ONLY = "PLANNING_ONLY"
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


def sanitize_retail_trader_experience_notes(values: list[str]) -> list[str]:
    sanitized: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized:
            sanitized.append(normalized)
    return sanitized


REQUIRED_FORBIDDEN_INTERACTIONS = {
    RetailTraderExperienceForbiddenInteractionKind.RECOMMENDATION_CARD,
    RetailTraderExperienceForbiddenInteractionKind.ACTION_BUTTON,
    RetailTraderExperienceForbiddenInteractionKind.CONFIDENCE_SCORE,
    RetailTraderExperienceForbiddenInteractionKind.DECISION_OBJECT_DISPLAY,
    RetailTraderExperienceForbiddenInteractionKind.READINESS_TO_TRADE_BADGE,
    RetailTraderExperienceForbiddenInteractionKind.BROKER_CONTROL,
    RetailTraderExperienceForbiddenInteractionKind.ORDER_BUTTON,
    RetailTraderExperienceForbiddenInteractionKind.APPROVAL_CONTROL,
    RetailTraderExperienceForbiddenInteractionKind.OVERRIDE_CONTROL,
    RetailTraderExperienceForbiddenInteractionKind.SUITABILITY_PROFILING,
    RetailTraderExperienceForbiddenInteractionKind.LIVE_DATA_CONTROL,
}


class RetailTraderExperiencePlanningContract(BaseModel):
    plan_id: str
    name: str
    stage: RetailTraderExperienceStage = RetailTraderExperienceStage.PLANNING_AND_GUARDRAILS
    purpose: str
    planned_personas: list[RetailTraderPersonaKind]
    planned_journeys: list[RetailTraderJourneyKind]
    planned_sections: list[RetailTraderExperienceSectionKind]
    planned_cards: list[RetailTraderExperienceCardKind]
    forbidden_interactions: list[RetailTraderExperienceForbiddenInteractionKind]
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
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("plan_id", "name", "purpose", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience planning text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_trader_experience_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def planning_contract_must_fail_closed(self) -> RetailTraderExperiencePlanningContract:
        if self.stage == RetailTraderExperienceStage.UNKNOWN:
            raise ValueError("UNKNOWN retail trader experience stage is not allowed")
        if not self.planned_personas:
            raise ValueError("retail trader experience planning requires planned personas")
        if RetailTraderPersonaKind.UNKNOWN in self.planned_personas:
            raise ValueError("UNKNOWN retail trader persona kind is not allowed")
        if not self.planned_journeys:
            raise ValueError("retail trader experience planning requires planned journeys")
        if RetailTraderJourneyKind.UNKNOWN in self.planned_journeys:
            raise ValueError("UNKNOWN retail trader journey kind is not allowed")
        if not self.planned_sections:
            raise ValueError("retail trader experience planning requires planned sections")
        if RetailTraderExperienceSectionKind.UNKNOWN in self.planned_sections:
            raise ValueError("UNKNOWN retail trader experience section kind is not allowed")
        if not self.planned_cards:
            raise ValueError("retail trader experience planning requires planned cards")
        if RetailTraderExperienceCardKind.UNKNOWN in self.planned_cards:
            raise ValueError("UNKNOWN retail trader experience card kind is not allowed")
        if not self.forbidden_interactions:
            raise ValueError("retail trader experience planning requires forbidden interactions")
        if RetailTraderExperienceForbiddenInteractionKind.UNKNOWN in self.forbidden_interactions:
            raise ValueError("UNKNOWN retail trader experience forbidden interaction is not allowed")
        missing = sorted(kind.value for kind in REQUIRED_FORBIDDEN_INTERACTIONS - set(self.forbidden_interactions))
        if missing:
            raise ValueError(f"retail trader experience missing forbidden interactions: {', '.join(missing)}")
        if self.active_ui_allowed:
            raise ValueError("active Retail Trader Experience UI is forbidden in Prompt 56")
        if self.frontend_components_allowed:
            raise ValueError("Retail Trader Experience frontend components are forbidden in Prompt 56")
        if self.desktop_components_allowed:
            raise ValueError("Retail Trader Experience desktop components are forbidden in Prompt 56")
        if self.recommendations_allowed:
            raise ValueError("Retail Trader Experience recommendations are forbidden in Prompt 56")
        if self.action_generation_allowed:
            raise ValueError("Retail Trader Experience action generation is forbidden in Prompt 56")
        if self.confidence_scoring_allowed:
            raise ValueError("Retail Trader Experience confidence scoring is forbidden in Prompt 56")
        if self.decision_object_generation_allowed:
            raise ValueError("Retail Trader Experience DecisionObject generation is forbidden in Prompt 56")
        if self.readiness_to_trade_allowed:
            raise ValueError("Retail Trader Experience readiness-to-trade is forbidden in Prompt 56")
        if self.broker_controls_allowed:
            raise ValueError("Retail Trader Experience broker controls are forbidden in Prompt 56")
        if self.execution_allowed:
            raise ValueError("Retail Trader Experience execution is forbidden in Prompt 56")
        if self.approval_allowed:
            raise ValueError("Retail Trader Experience approvals are forbidden in Prompt 56")
        if self.override_allowed:
            raise ValueError("Retail Trader Experience overrides are forbidden in Prompt 56")
        if self.suitability_profiling_allowed:
            raise ValueError("Retail Trader Experience suitability profiling is forbidden in Prompt 56")
        if not self.returns_unavailable_by_default:
            raise ValueError("Retail Trader Experience must return unavailable by default in Prompt 56")
        return self


def default_retail_trader_experience_planning_contract() -> RetailTraderExperiencePlanningContract:
    return RetailTraderExperiencePlanningContract(
        plan_id="retail-trader-experience-planning-guardrails-v1",
        name="Retail Trader Experience Planning and Guardrails",
        purpose=(
            "Define planning-only personas, journeys, sections, cards, references, and forbidden interactions "
            "without active UI, suitability profiling, recommendations, broker controls, or execution."
        ),
        planned_personas=[
            RetailTraderPersonaKind.RETAIL_TRADER_PLACEHOLDER,
            RetailTraderPersonaKind.INTRADAY_TRADER_PLACEHOLDER,
            RetailTraderPersonaKind.SWING_TRADER_PLACEHOLDER,
            RetailTraderPersonaKind.OPTIONS_CONTEXT_PLACEHOLDER,
            RetailTraderPersonaKind.RISK_AWARE_BEGINNER_PLACEHOLDER,
            RetailTraderPersonaKind.QUANT_CURIOUS_TRADER_PLACEHOLDER,
        ],
        planned_journeys=[
            RetailTraderJourneyKind.ONBOARDING_PLACEHOLDER,
            RetailTraderJourneyKind.INSTRUMENT_REVIEW_PLACEHOLDER,
            RetailTraderJourneyKind.DASHBOARD_CONTEXT_REVIEW_PLACEHOLDER,
            RetailTraderJourneyKind.SAFETY_CONTEXT_REVIEW_PLACEHOLDER,
            RetailTraderJourneyKind.EVIDENCE_REVIEW_PLACEHOLDER,
            RetailTraderJourneyKind.HUMAN_REVIEW_PLACEHOLDER,
            RetailTraderJourneyKind.UNAVAILABLE_NOTICE,
        ],
        planned_sections=[
            RetailTraderExperienceSectionKind.OVERVIEW,
            RetailTraderExperienceSectionKind.TRADER_CONTEXT,
            RetailTraderExperienceSectionKind.INSTRUMENT_CONTEXT,
            RetailTraderExperienceSectionKind.DASHBOARD_CONTEXT,
            RetailTraderExperienceSectionKind.DATA_QUALITY_CONTEXT,
            RetailTraderExperienceSectionKind.SAFETY_CONTEXT,
            RetailTraderExperienceSectionKind.EDUCATIONAL_CONTEXT,
            RetailTraderExperienceSectionKind.HUMAN_REVIEW_CONTEXT,
            RetailTraderExperienceSectionKind.UNAVAILABLE_NOTICE,
        ],
        planned_cards=[
            RetailTraderExperienceCardKind.PLACEHOLDER,
            RetailTraderExperienceCardKind.TRADER_CONTEXT_PLACEHOLDER,
            RetailTraderExperienceCardKind.INSTRUMENT_CONTEXT_PLACEHOLDER,
            RetailTraderExperienceCardKind.DASHBOARD_CONTEXT_PLACEHOLDER,
            RetailTraderExperienceCardKind.DATA_QUALITY_PLACEHOLDER,
            RetailTraderExperienceCardKind.SAFETY_PLACEHOLDER,
            RetailTraderExperienceCardKind.EDUCATIONAL_PLACEHOLDER,
            RetailTraderExperienceCardKind.REVIEW_PLACEHOLDER,
            RetailTraderExperienceCardKind.UNAVAILABLE,
        ],
        forbidden_interactions=[
            RetailTraderExperienceForbiddenInteractionKind.RECOMMENDATION_CARD,
            RetailTraderExperienceForbiddenInteractionKind.ACTION_BUTTON,
            RetailTraderExperienceForbiddenInteractionKind.CONFIDENCE_SCORE,
            RetailTraderExperienceForbiddenInteractionKind.DECISION_OBJECT_DISPLAY,
            RetailTraderExperienceForbiddenInteractionKind.READINESS_TO_TRADE_BADGE,
            RetailTraderExperienceForbiddenInteractionKind.BROKER_CONTROL,
            RetailTraderExperienceForbiddenInteractionKind.ORDER_BUTTON,
            RetailTraderExperienceForbiddenInteractionKind.APPROVAL_CONTROL,
            RetailTraderExperienceForbiddenInteractionKind.OVERRIDE_CONTROL,
            RetailTraderExperienceForbiddenInteractionKind.SUITABILITY_PROFILING,
            RetailTraderExperienceForbiddenInteractionKind.LIVE_DATA_CONTROL,
        ],
        notes=[
            "Planning contract is not active UI.",
            "Personas are placeholders, not suitability profiles or trading permission profiles.",
            "Experience placeholders are not recommendations, approvals, readiness-to-trade, broker controls, or execution.",
        ],
    )
