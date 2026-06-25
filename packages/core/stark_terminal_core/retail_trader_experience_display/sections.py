from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_trader_experience_display.contracts import (
    RetailTraderExperienceDisplaySectionKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_trader_experience_display_notes,
)


class RetailTraderExperienceDisplaySectionPlaceholder(BaseModel):
    section_id: str
    section_kind: RetailTraderExperienceDisplaySectionKind
    title: str
    description: str
    widget_ids: list[str] = Field(default_factory=list)
    active_ui: bool = False
    rendered_now: bool = False
    unavailable: bool = True
    display_contract_only: bool = True
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    readiness_to_trade_allowed: bool = False
    broker_controls_allowed: bool = False
    execution_allowed: bool = False
    suitability_profiling_allowed: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("section_id", "title", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience display section text fields")

    @field_validator("widget_ids", "notes")
    @classmethod
    def list_fields_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_trader_experience_display_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def section_placeholder_must_fail_closed(self) -> RetailTraderExperienceDisplaySectionPlaceholder:
        if self.section_kind == RetailTraderExperienceDisplaySectionKind.UNKNOWN:
            raise ValueError("UNKNOWN Retail Trader Experience Display section kind is not allowed")
        if self.active_ui or self.rendered_now:
            raise ValueError("Retail Trader Experience Display section cannot be active or rendered")
        if not self.unavailable:
            raise ValueError("Retail Trader Experience Display section must remain unavailable")
        if not self.display_contract_only:
            raise ValueError("Retail Trader Experience Display section must remain display-contract-only")
        if (
            self.recommendations_allowed
            or self.action_generation_allowed
            or self.confidence_scoring_allowed
            or self.decision_object_generation_allowed
            or self.readiness_to_trade_allowed
            or self.broker_controls_allowed
            or self.execution_allowed
            or self.suitability_profiling_allowed
        ):
            raise ValueError("Retail Trader Experience Display section dangerous flags must be false")
        return self


def default_retail_trader_experience_display_section_placeholders() -> list[
    RetailTraderExperienceDisplaySectionPlaceholder
]:
    return [
        RetailTraderExperienceDisplaySectionPlaceholder(
            section_id="header",
            section_kind=RetailTraderExperienceDisplaySectionKind.HEADER,
            title="Header display section placeholder",
            description="Display contract placeholder only; no active UI, frontend component, or desktop component.",
            widget_ids=["planning-only-badge-widget"],
        ),
        RetailTraderExperienceDisplaySectionPlaceholder(
            section_id="overview",
            section_kind=RetailTraderExperienceDisplaySectionKind.OVERVIEW,
            title="Overview display section placeholder",
            description="Placeholder for future overview; unavailable by default and not a recommendation section.",
            widget_ids=["placeholder-widget"],
        ),
        RetailTraderExperienceDisplaySectionPlaceholder(
            section_id="trader_context",
            section_kind=RetailTraderExperienceDisplaySectionKind.TRADER_CONTEXT,
            title="Trader context display section placeholder",
            description="Placeholder only; not suitability profiling and not active personalization.",
            widget_ids=["trader-context-placeholder-widget", "persona-placeholder-widget"],
        ),
        RetailTraderExperienceDisplaySectionPlaceholder(
            section_id="instrument_context",
            section_kind=RetailTraderExperienceDisplaySectionKind.INSTRUMENT_CONTEXT,
            title="Instrument context display section placeholder",
            description="Placeholder only; no live market data, signal, or decision output.",
            widget_ids=["dashboard-context-placeholder-widget"],
        ),
        RetailTraderExperienceDisplaySectionPlaceholder(
            section_id="dashboard_context",
            section_kind=RetailTraderExperienceDisplaySectionKind.DASHBOARD_CONTEXT,
            title="Dashboard context display section placeholder",
            description="Placeholder only; no active Retail Dashboard output is rendered.",
            widget_ids=["dashboard-context-placeholder-widget"],
        ),
        RetailTraderExperienceDisplaySectionPlaceholder(
            section_id="data_quality_context",
            section_kind=RetailTraderExperienceDisplaySectionKind.DATA_QUALITY_CONTEXT,
            title="Data quality context display section placeholder",
            description="Placeholder only; no data-quality pass is a recommendation, approval, or execution gate.",
            widget_ids=["data-quality-placeholder-widget"],
        ),
        RetailTraderExperienceDisplaySectionPlaceholder(
            section_id="safety_context",
            section_kind=RetailTraderExperienceDisplaySectionKind.SAFETY_CONTEXT,
            title="Safety context display section placeholder",
            description="Placeholder only; no safety pass, readiness-to-trade, approval, override, or broker control.",
            widget_ids=["safety-placeholder-widget"],
        ),
        RetailTraderExperienceDisplaySectionPlaceholder(
            section_id="educational_context",
            section_kind=RetailTraderExperienceDisplaySectionKind.EDUCATIONAL_CONTEXT,
            title="Educational context display section placeholder",
            description="Placeholder only; no trading advice, recommendation, or suitability profile.",
            widget_ids=["educational-placeholder-widget"],
        ),
        RetailTraderExperienceDisplaySectionPlaceholder(
            section_id="human_review_context",
            section_kind=RetailTraderExperienceDisplaySectionKind.HUMAN_REVIEW_CONTEXT,
            title="Human review context display section placeholder",
            description="Placeholder only; no active workflow, approval, override, or task assignment.",
            widget_ids=["review-placeholder-widget"],
        ),
        RetailTraderExperienceDisplaySectionPlaceholder(
            section_id="unavailable_notice",
            section_kind=RetailTraderExperienceDisplaySectionKind.UNAVAILABLE_NOTICE,
            title="Unavailable notice display section placeholder",
            description="Fail-closed section placeholder expected during Prompt 58.",
            widget_ids=["unavailable-widget"],
        ),
    ]
