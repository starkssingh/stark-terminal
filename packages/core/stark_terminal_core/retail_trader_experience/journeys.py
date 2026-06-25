from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_trader_experience.planning import (
    RetailTraderJourneyKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_trader_experience_notes,
)


class RetailTraderJourneyPlaceholder(BaseModel):
    journey_id: str
    journey_kind: RetailTraderJourneyKind
    title: str
    description: str
    planning_only: bool = True
    active_ui: bool = False
    unavailable: bool = True
    recommendation_journey: bool = False
    trading_advice_journey: bool = False
    broker_control_journey: bool = False
    execution_journey: bool = False
    readiness_to_trade_journey: bool = False
    approval_journey: bool = False
    override_journey: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("journey_id", "title", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader journey text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_trader_experience_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def journey_placeholder_must_fail_closed(self) -> RetailTraderJourneyPlaceholder:
        if self.journey_kind == RetailTraderJourneyKind.UNKNOWN:
            raise ValueError("UNKNOWN retail trader journey kind is not allowed")
        if not self.planning_only:
            raise ValueError("retail trader journey placeholder must remain planning-only")
        if self.active_ui:
            raise ValueError("retail trader journey placeholder cannot be active UI")
        if not self.unavailable:
            raise ValueError("retail trader journey placeholder must remain unavailable")
        if self.recommendation_journey:
            raise ValueError("retail trader recommendation journeys are forbidden")
        if self.trading_advice_journey:
            raise ValueError("retail trader trading advice journeys are forbidden")
        if self.broker_control_journey:
            raise ValueError("retail trader broker control journeys are forbidden")
        if self.execution_journey:
            raise ValueError("retail trader execution journeys are forbidden")
        if self.readiness_to_trade_journey:
            raise ValueError("retail trader readiness-to-trade journeys are forbidden")
        if self.approval_journey:
            raise ValueError("retail trader approval journeys are forbidden")
        if self.override_journey:
            raise ValueError("retail trader override journeys are forbidden")
        return self


def default_retail_trader_journey_placeholders() -> list[RetailTraderJourneyPlaceholder]:
    specs = [
        (
            "retail-trader-journey-onboarding-placeholder-v1",
            RetailTraderJourneyKind.ONBOARDING_PLACEHOLDER,
            "Onboarding Placeholder",
            "Planning-only onboarding journey with no active UI.",
        ),
        (
            "retail-trader-journey-instrument-review-placeholder-v1",
            RetailTraderJourneyKind.INSTRUMENT_REVIEW_PLACEHOLDER,
            "Instrument Review Placeholder",
            "Planning-only instrument review journey with no trading advice.",
        ),
        (
            "retail-trader-journey-dashboard-context-placeholder-v1",
            RetailTraderJourneyKind.DASHBOARD_CONTEXT_REVIEW_PLACEHOLDER,
            "Dashboard Context Review Placeholder",
            "Planning-only dashboard context journey with no active dashboard output.",
        ),
        (
            "retail-trader-journey-safety-context-placeholder-v1",
            RetailTraderJourneyKind.SAFETY_CONTEXT_REVIEW_PLACEHOLDER,
            "Safety Context Review Placeholder",
            "Planning-only safety context journey with no readiness-to-trade.",
        ),
        (
            "retail-trader-journey-evidence-review-placeholder-v1",
            RetailTraderJourneyKind.EVIDENCE_REVIEW_PLACEHOLDER,
            "Evidence Review Placeholder",
            "Planning-only evidence review journey with no active DecisionObject display.",
        ),
        (
            "retail-trader-journey-human-review-placeholder-v1",
            RetailTraderJourneyKind.HUMAN_REVIEW_PLACEHOLDER,
            "Human Review Placeholder",
            "Planning-only human review journey with no approval or override.",
        ),
        (
            "retail-trader-journey-unavailable-placeholder-v1",
            RetailTraderJourneyKind.UNAVAILABLE_NOTICE,
            "Unavailable Notice Placeholder",
            "Unavailable-by-default journey for Prompt 56 planning.",
        ),
    ]
    return [
        RetailTraderJourneyPlaceholder(
            journey_id=journey_id,
            journey_kind=journey_kind,
            title=title,
            description=description,
            notes=["Journey placeholder is not trading advice, broker control, readiness-to-trade, or execution."],
        )
        for journey_id, journey_kind, title, description in specs
    ]
