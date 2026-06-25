from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_trader_experience.planning import (
    RetailTraderExperienceSafetyLabel,
    RetailTraderExperienceSectionKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_trader_experience_notes,
)


class RetailTraderExperienceSectionPlaceholder(BaseModel):
    section_id: str
    section_kind: RetailTraderExperienceSectionKind
    title: str
    description: str
    visible: bool = True
    active_ui: bool = False
    unavailable: bool = True
    planning_only: bool = True
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    readiness_to_trade_allowed: bool = False
    broker_controls_allowed: bool = False
    execution_allowed: bool = False
    suitability_profiling_allowed: bool = False
    safety_label: RetailTraderExperienceSafetyLabel = RetailTraderExperienceSafetyLabel.PLANNING_ONLY
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("section_id", "title", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience section text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_trader_experience_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def section_placeholder_must_fail_closed(self) -> RetailTraderExperienceSectionPlaceholder:
        if self.section_kind == RetailTraderExperienceSectionKind.UNKNOWN:
            raise ValueError("UNKNOWN retail trader experience section kind is not allowed")
        if self.active_ui:
            raise ValueError("retail trader experience section placeholder cannot be active UI")
        if not self.unavailable:
            raise ValueError("retail trader experience section placeholder must remain unavailable")
        if not self.planning_only:
            raise ValueError("retail trader experience section placeholder must remain planning-only")
        if self.recommendations_allowed:
            raise ValueError("retail trader experience section cannot allow recommendations")
        if self.action_generation_allowed:
            raise ValueError("retail trader experience section cannot allow action generation")
        if self.confidence_scoring_allowed:
            raise ValueError("retail trader experience section cannot allow confidence scoring")
        if self.decision_object_generation_allowed:
            raise ValueError("retail trader experience section cannot allow DecisionObject generation")
        if self.readiness_to_trade_allowed:
            raise ValueError("retail trader experience section cannot allow readiness-to-trade")
        if self.broker_controls_allowed:
            raise ValueError("retail trader experience section cannot allow broker controls")
        if self.execution_allowed:
            raise ValueError("retail trader experience section cannot allow execution")
        if self.suitability_profiling_allowed:
            raise ValueError("retail trader experience section cannot allow suitability profiling")
        if self.safety_label == RetailTraderExperienceSafetyLabel.UNKNOWN:
            raise ValueError("retail trader experience section safety label cannot be UNKNOWN")
        return self


def default_retail_trader_experience_section_placeholders() -> list[RetailTraderExperienceSectionPlaceholder]:
    specs = [
        (
            "retail-trader-experience-section-overview-v1",
            RetailTraderExperienceSectionKind.OVERVIEW,
            "Overview Placeholder",
            "Planning-only experience overview section with no active UI.",
        ),
        (
            "retail-trader-experience-section-trader-context-v1",
            RetailTraderExperienceSectionKind.TRADER_CONTEXT,
            "Trader Context Placeholder",
            "Planning-only trader context section with no suitability profiling.",
        ),
        (
            "retail-trader-experience-section-instrument-context-v1",
            RetailTraderExperienceSectionKind.INSTRUMENT_CONTEXT,
            "Instrument Context Placeholder",
            "Planning-only instrument context section with no live market data display.",
        ),
        (
            "retail-trader-experience-section-dashboard-context-v1",
            RetailTraderExperienceSectionKind.DASHBOARD_CONTEXT,
            "Dashboard Context Placeholder",
            "Planning-only dashboard context section with no active dashboard rendering.",
        ),
        (
            "retail-trader-experience-section-data-quality-v1",
            RetailTraderExperienceSectionKind.DATA_QUALITY_CONTEXT,
            "Data Quality Context Placeholder",
            "Planning-only data quality context section with no validated recommendation.",
        ),
        (
            "retail-trader-experience-section-safety-context-v1",
            RetailTraderExperienceSectionKind.SAFETY_CONTEXT,
            "Safety Context Placeholder",
            "Planning-only safety context section with no safety pass or readiness-to-trade.",
        ),
        (
            "retail-trader-experience-section-educational-context-v1",
            RetailTraderExperienceSectionKind.EDUCATIONAL_CONTEXT,
            "Educational Context Placeholder",
            "Planning-only educational context section with no trading advice.",
        ),
        (
            "retail-trader-experience-section-human-review-v1",
            RetailTraderExperienceSectionKind.HUMAN_REVIEW_CONTEXT,
            "Human Review Context Placeholder",
            "Planning-only human review context section with no approval or override.",
        ),
        (
            "retail-trader-experience-section-unavailable-v1",
            RetailTraderExperienceSectionKind.UNAVAILABLE_NOTICE,
            "Unavailable Notice Placeholder",
            "Unavailable-by-default section for Prompt 56 planning.",
        ),
    ]
    return [
        RetailTraderExperienceSectionPlaceholder(
            section_id=section_id,
            section_kind=section_kind,
            title=title,
            description=description,
            notes=["Section placeholder is not active UI, suitability profiling, recommendation, or execution."],
        )
        for section_id, section_kind, title, description in specs
    ]
