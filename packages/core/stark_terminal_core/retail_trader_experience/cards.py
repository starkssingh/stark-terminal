from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_trader_experience.planning import (
    RetailTraderExperienceCardKind,
    RetailTraderExperienceSafetyLabel,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_trader_experience_notes,
)


class RetailTraderExperienceCardPlaceholder(BaseModel):
    card_id: str
    card_kind: RetailTraderExperienceCardKind
    title: str
    description: str
    visible: bool = True
    active_ui: bool = False
    unavailable: bool = True
    planning_only: bool = True
    recommendation_card: bool = False
    action_card: bool = False
    confidence_display: bool = False
    decision_object_display: bool = False
    readiness_to_trade_display: bool = False
    broker_control: bool = False
    execution_control: bool = False
    approval_control: bool = False
    override_control: bool = False
    suitability_profile_display: bool = False
    safety_label: RetailTraderExperienceSafetyLabel = RetailTraderExperienceSafetyLabel.NOT_A_RECOMMENDATION
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("card_id", "title", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience card text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_trader_experience_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def card_placeholder_must_fail_closed(self) -> RetailTraderExperienceCardPlaceholder:
        if self.card_kind == RetailTraderExperienceCardKind.UNKNOWN:
            raise ValueError("UNKNOWN retail trader experience card kind is not allowed")
        if self.active_ui:
            raise ValueError("retail trader experience card placeholder cannot be active UI")
        if not self.unavailable:
            raise ValueError("retail trader experience card placeholder must remain unavailable")
        if not self.planning_only:
            raise ValueError("retail trader experience card placeholder must remain planning-only")
        if self.recommendation_card:
            raise ValueError("retail trader experience recommendation cards are forbidden")
        if self.action_card:
            raise ValueError("retail trader experience action cards are forbidden")
        if self.confidence_display:
            raise ValueError("retail trader experience confidence displays are forbidden")
        if self.decision_object_display:
            raise ValueError("retail trader experience DecisionObject displays are forbidden")
        if self.readiness_to_trade_display:
            raise ValueError("retail trader experience readiness-to-trade displays are forbidden")
        if self.broker_control:
            raise ValueError("retail trader experience broker controls are forbidden")
        if self.execution_control:
            raise ValueError("retail trader experience execution controls are forbidden")
        if self.approval_control:
            raise ValueError("retail trader experience approval controls are forbidden")
        if self.override_control:
            raise ValueError("retail trader experience override controls are forbidden")
        if self.suitability_profile_display:
            raise ValueError("retail trader experience suitability profile displays are forbidden")
        if self.safety_label == RetailTraderExperienceSafetyLabel.UNKNOWN:
            raise ValueError("retail trader experience card safety label cannot be UNKNOWN")
        return self


def default_retail_trader_experience_card_placeholders() -> list[RetailTraderExperienceCardPlaceholder]:
    specs = [
        (
            "retail-trader-experience-card-placeholder-v1",
            RetailTraderExperienceCardKind.PLACEHOLDER,
            "Experience Placeholder",
            "Generic planning-only experience card placeholder.",
        ),
        (
            "retail-trader-experience-card-trader-context-v1",
            RetailTraderExperienceCardKind.TRADER_CONTEXT_PLACEHOLDER,
            "Trader Context Placeholder",
            "Planning-only trader context card with no suitability profile.",
        ),
        (
            "retail-trader-experience-card-instrument-context-v1",
            RetailTraderExperienceCardKind.INSTRUMENT_CONTEXT_PLACEHOLDER,
            "Instrument Context Placeholder",
            "Planning-only instrument context card with no live market data.",
        ),
        (
            "retail-trader-experience-card-dashboard-context-v1",
            RetailTraderExperienceCardKind.DASHBOARD_CONTEXT_PLACEHOLDER,
            "Dashboard Context Placeholder",
            "Planning-only dashboard context card with no active dashboard output.",
        ),
        (
            "retail-trader-experience-card-data-quality-v1",
            RetailTraderExperienceCardKind.DATA_QUALITY_PLACEHOLDER,
            "Data Quality Placeholder",
            "Planning-only data quality card with no validated recommendation.",
        ),
        (
            "retail-trader-experience-card-safety-v1",
            RetailTraderExperienceCardKind.SAFETY_PLACEHOLDER,
            "Safety Placeholder",
            "Planning-only safety card with no readiness-to-trade or safety pass.",
        ),
        (
            "retail-trader-experience-card-education-v1",
            RetailTraderExperienceCardKind.EDUCATIONAL_PLACEHOLDER,
            "Educational Placeholder",
            "Planning-only education card with no trading advice.",
        ),
        (
            "retail-trader-experience-card-review-v1",
            RetailTraderExperienceCardKind.REVIEW_PLACEHOLDER,
            "Review Placeholder",
            "Planning-only review card with no approval or override.",
        ),
        (
            "retail-trader-experience-card-unavailable-v1",
            RetailTraderExperienceCardKind.UNAVAILABLE,
            "Unavailable Placeholder",
            "Unavailable-by-default card for Prompt 56 planning.",
        ),
    ]
    return [
        RetailTraderExperienceCardPlaceholder(
            card_id=card_id,
            card_kind=card_kind,
            title=title,
            description=description,
            notes=["Card placeholder is not a recommendation card, action card, suitability profile, or execution control."],
        )
        for card_id, card_kind, title, description in specs
    ]
