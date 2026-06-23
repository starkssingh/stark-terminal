from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator


class RetailDashboardStage(StrEnum):
    PLANNING_AND_GUARDRAILS = "PLANNING_AND_GUARDRAILS"
    UNAVAILABLE_ONLY = "UNAVAILABLE_ONLY"
    SECTION_PLACEHOLDERS = "SECTION_PLACEHOLDERS"
    CARD_PLACEHOLDERS = "CARD_PLACEHOLDERS"
    ACTIVE_UI_PLANNED = "ACTIVE_UI_PLANNED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class RetailDashboardSectionKind(StrEnum):
    OVERVIEW = "OVERVIEW"
    INSTRUMENT_CONTEXT = "INSTRUMENT_CONTEXT"
    DATA_QUALITY = "DATA_QUALITY"
    MARKET_CONTEXT = "MARKET_CONTEXT"
    DECISION_PLACEHOLDER = "DECISION_PLACEHOLDER"
    RISK_PLACEHOLDER = "RISK_PLACEHOLDER"
    HUMAN_REVIEW_PLACEHOLDER = "HUMAN_REVIEW_PLACEHOLDER"
    SAFETY_PLACEHOLDER = "SAFETY_PLACEHOLDER"
    UNAVAILABLE_NOTICE = "UNAVAILABLE_NOTICE"
    UNKNOWN = "UNKNOWN"


class RetailDashboardCardKind(StrEnum):
    PLACEHOLDER = "PLACEHOLDER"
    DATA_QUALITY_PLACEHOLDER = "DATA_QUALITY_PLACEHOLDER"
    MARKET_CONTEXT_PLACEHOLDER = "MARKET_CONTEXT_PLACEHOLDER"
    DECISION_PLACEHOLDER = "DECISION_PLACEHOLDER"
    RISK_PLACEHOLDER = "RISK_PLACEHOLDER"
    REVIEW_PLACEHOLDER = "REVIEW_PLACEHOLDER"
    SAFETY_PLACEHOLDER = "SAFETY_PLACEHOLDER"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"


class RetailDashboardForbiddenInteractionKind(StrEnum):
    RECOMMENDATION_CARD = "RECOMMENDATION_CARD"
    ACTION_BUTTON = "ACTION_BUTTON"
    CONFIDENCE_SCORE = "CONFIDENCE_SCORE"
    DECISION_OBJECT_DISPLAY = "DECISION_OBJECT_DISPLAY"
    READINESS_TO_TRADE_BADGE = "READINESS_TO_TRADE_BADGE"
    BROKER_CONTROL = "BROKER_CONTROL"
    ORDER_BUTTON = "ORDER_BUTTON"
    APPROVAL_CONTROL = "APPROVAL_CONTROL"
    OVERRIDE_CONTROL = "OVERRIDE_CONTROL"
    LIVE_DATA_CONTROL = "LIVE_DATA_CONTROL"
    UNKNOWN = "UNKNOWN"


class RetailDashboardSafetyLabel(StrEnum):
    PLANNING_ONLY = "PLANNING_ONLY"
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


def sanitize_retail_dashboard_notes(values: list[str]) -> list[str]:
    sanitized: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized:
            sanitized.append(normalized)
    return sanitized


REQUIRED_FORBIDDEN_INTERACTIONS = {
    RetailDashboardForbiddenInteractionKind.RECOMMENDATION_CARD,
    RetailDashboardForbiddenInteractionKind.ACTION_BUTTON,
    RetailDashboardForbiddenInteractionKind.CONFIDENCE_SCORE,
    RetailDashboardForbiddenInteractionKind.DECISION_OBJECT_DISPLAY,
    RetailDashboardForbiddenInteractionKind.READINESS_TO_TRADE_BADGE,
    RetailDashboardForbiddenInteractionKind.BROKER_CONTROL,
    RetailDashboardForbiddenInteractionKind.ORDER_BUTTON,
    RetailDashboardForbiddenInteractionKind.APPROVAL_CONTROL,
    RetailDashboardForbiddenInteractionKind.OVERRIDE_CONTROL,
}


class RetailDashboardPlanningContract(BaseModel):
    plan_id: str
    name: str
    stage: RetailDashboardStage = RetailDashboardStage.PLANNING_AND_GUARDRAILS
    purpose: str
    planned_sections: list[RetailDashboardSectionKind]
    planned_cards: list[RetailDashboardCardKind]
    forbidden_interactions: list[RetailDashboardForbiddenInteractionKind]
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
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("plan_id", "name", "purpose", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard planning text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_dashboard_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def planning_contract_must_fail_closed(self) -> RetailDashboardPlanningContract:
        if self.stage == RetailDashboardStage.UNKNOWN:
            raise ValueError("UNKNOWN retail dashboard stage is not allowed")
        if not self.planned_sections:
            raise ValueError("retail dashboard planning requires planned sections")
        if RetailDashboardSectionKind.UNKNOWN in self.planned_sections:
            raise ValueError("UNKNOWN retail dashboard section kind is not allowed")
        if not self.planned_cards:
            raise ValueError("retail dashboard planning requires planned cards")
        if RetailDashboardCardKind.UNKNOWN in self.planned_cards:
            raise ValueError("UNKNOWN retail dashboard card kind is not allowed")
        if not self.forbidden_interactions:
            raise ValueError("retail dashboard planning requires forbidden interactions")
        if RetailDashboardForbiddenInteractionKind.UNKNOWN in self.forbidden_interactions:
            raise ValueError("UNKNOWN retail dashboard forbidden interaction is not allowed")
        missing = sorted(kind.value for kind in REQUIRED_FORBIDDEN_INTERACTIONS - set(self.forbidden_interactions))
        if missing:
            raise ValueError(f"retail dashboard planning missing forbidden interactions: {', '.join(missing)}")
        if self.active_ui_allowed:
            raise ValueError("active Retail Dashboard UI is forbidden in Prompt 49")
        if self.recommendations_allowed:
            raise ValueError("Retail Dashboard recommendations are forbidden in Prompt 49")
        if self.action_generation_allowed:
            raise ValueError("Retail Dashboard action generation is forbidden in Prompt 49")
        if self.confidence_scoring_allowed:
            raise ValueError("Retail Dashboard confidence scoring is forbidden in Prompt 49")
        if self.decision_object_generation_allowed:
            raise ValueError("Retail Dashboard DecisionObject generation is forbidden in Prompt 49")
        if self.readiness_to_trade_allowed:
            raise ValueError("Retail Dashboard readiness-to-trade is forbidden in Prompt 49")
        if self.broker_controls_allowed:
            raise ValueError("Retail Dashboard broker controls are forbidden in Prompt 49")
        if self.execution_allowed:
            raise ValueError("Retail Dashboard execution is forbidden in Prompt 49")
        if self.approval_allowed:
            raise ValueError("Retail Dashboard approvals are forbidden in Prompt 49")
        if self.override_allowed:
            raise ValueError("Retail Dashboard overrides are forbidden in Prompt 49")
        if not self.returns_unavailable_by_default:
            raise ValueError("Retail Dashboard must return unavailable by default in Prompt 49")
        return self


def default_retail_dashboard_planning_contract() -> RetailDashboardPlanningContract:
    return RetailDashboardPlanningContract(
        plan_id="retail-dashboard-planning-guardrails-v1",
        name="Retail Dashboard Planning and Guardrails",
        purpose=(
            "Define planning-only Retail Dashboard sections, cards, references, and forbidden interactions "
            "without active UI, recommendations, broker controls, readiness-to-trade, or execution."
        ),
        planned_sections=[
            RetailDashboardSectionKind.OVERVIEW,
            RetailDashboardSectionKind.INSTRUMENT_CONTEXT,
            RetailDashboardSectionKind.DATA_QUALITY,
            RetailDashboardSectionKind.MARKET_CONTEXT,
            RetailDashboardSectionKind.DECISION_PLACEHOLDER,
            RetailDashboardSectionKind.RISK_PLACEHOLDER,
            RetailDashboardSectionKind.HUMAN_REVIEW_PLACEHOLDER,
            RetailDashboardSectionKind.SAFETY_PLACEHOLDER,
            RetailDashboardSectionKind.UNAVAILABLE_NOTICE,
        ],
        planned_cards=[
            RetailDashboardCardKind.PLACEHOLDER,
            RetailDashboardCardKind.DATA_QUALITY_PLACEHOLDER,
            RetailDashboardCardKind.MARKET_CONTEXT_PLACEHOLDER,
            RetailDashboardCardKind.DECISION_PLACEHOLDER,
            RetailDashboardCardKind.RISK_PLACEHOLDER,
            RetailDashboardCardKind.REVIEW_PLACEHOLDER,
            RetailDashboardCardKind.SAFETY_PLACEHOLDER,
            RetailDashboardCardKind.UNAVAILABLE,
        ],
        forbidden_interactions=[
            RetailDashboardForbiddenInteractionKind.RECOMMENDATION_CARD,
            RetailDashboardForbiddenInteractionKind.ACTION_BUTTON,
            RetailDashboardForbiddenInteractionKind.CONFIDENCE_SCORE,
            RetailDashboardForbiddenInteractionKind.DECISION_OBJECT_DISPLAY,
            RetailDashboardForbiddenInteractionKind.READINESS_TO_TRADE_BADGE,
            RetailDashboardForbiddenInteractionKind.BROKER_CONTROL,
            RetailDashboardForbiddenInteractionKind.ORDER_BUTTON,
            RetailDashboardForbiddenInteractionKind.APPROVAL_CONTROL,
            RetailDashboardForbiddenInteractionKind.OVERRIDE_CONTROL,
            RetailDashboardForbiddenInteractionKind.LIVE_DATA_CONTROL,
        ],
        notes=[
            "Planning contract is not an active UI.",
            "Dashboard placeholders are not recommendations, approvals, readiness-to-trade, broker controls, or execution.",
        ],
    )
