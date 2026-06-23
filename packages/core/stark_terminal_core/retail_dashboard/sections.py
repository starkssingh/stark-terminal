from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_dashboard.planning import (
    RetailDashboardSafetyLabel,
    RetailDashboardSectionKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_dashboard_notes,
)


class RetailDashboardSectionPlaceholder(BaseModel):
    section_id: str
    section_kind: RetailDashboardSectionKind
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
    safety_label: RetailDashboardSafetyLabel = RetailDashboardSafetyLabel.PLANNING_ONLY
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("section_id", "title", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard section text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_dashboard_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def section_placeholder_must_fail_closed(self) -> RetailDashboardSectionPlaceholder:
        if self.section_kind == RetailDashboardSectionKind.UNKNOWN:
            raise ValueError("UNKNOWN retail dashboard section kind is not allowed")
        if self.active_ui:
            raise ValueError("retail dashboard section placeholder cannot be active UI")
        if not self.unavailable:
            raise ValueError("retail dashboard section placeholder must remain unavailable")
        if not self.planning_only:
            raise ValueError("retail dashboard section placeholder must remain planning-only")
        if self.recommendations_allowed:
            raise ValueError("retail dashboard section cannot allow recommendations")
        if self.action_generation_allowed:
            raise ValueError("retail dashboard section cannot allow action generation")
        if self.confidence_scoring_allowed:
            raise ValueError("retail dashboard section cannot allow confidence scoring")
        if self.decision_object_generation_allowed:
            raise ValueError("retail dashboard section cannot allow DecisionObject generation")
        if self.readiness_to_trade_allowed:
            raise ValueError("retail dashboard section cannot allow readiness-to-trade")
        if self.broker_controls_allowed:
            raise ValueError("retail dashboard section cannot allow broker controls")
        if self.execution_allowed:
            raise ValueError("retail dashboard section cannot allow execution")
        if self.safety_label == RetailDashboardSafetyLabel.UNKNOWN:
            raise ValueError("retail dashboard section safety label cannot be UNKNOWN")
        return self


def default_retail_dashboard_section_placeholders() -> list[RetailDashboardSectionPlaceholder]:
    specs = [
        (
            "retail-dashboard-section-overview-v1",
            RetailDashboardSectionKind.OVERVIEW,
            "Overview Placeholder",
            "Planning-only overview section with no active dashboard UI.",
        ),
        (
            "retail-dashboard-section-instrument-context-v1",
            RetailDashboardSectionKind.INSTRUMENT_CONTEXT,
            "Instrument Context Placeholder",
            "Planning-only instrument context section with no real market data display.",
        ),
        (
            "retail-dashboard-section-data-quality-v1",
            RetailDashboardSectionKind.DATA_QUALITY,
            "Data Quality Placeholder",
            "Planning-only data quality section with no dashboard decision output.",
        ),
        (
            "retail-dashboard-section-market-context-v1",
            RetailDashboardSectionKind.MARKET_CONTEXT,
            "Market Context Placeholder",
            "Planning-only market context section with no recommendation or signal.",
        ),
        (
            "retail-dashboard-section-decision-v1",
            RetailDashboardSectionKind.DECISION_PLACEHOLDER,
            "Decision Placeholder",
            "Planning-only decision reference section with no active DecisionObject display.",
        ),
        (
            "retail-dashboard-section-risk-v1",
            RetailDashboardSectionKind.RISK_PLACEHOLDER,
            "Risk Placeholder",
            "Planning-only risk reference section with no readiness-to-trade.",
        ),
        (
            "retail-dashboard-section-human-review-v1",
            RetailDashboardSectionKind.HUMAN_REVIEW_PLACEHOLDER,
            "Human Review Placeholder",
            "Planning-only human-review reference section with no approval.",
        ),
        (
            "retail-dashboard-section-safety-v1",
            RetailDashboardSectionKind.SAFETY_PLACEHOLDER,
            "Safety Placeholder",
            "Planning-only safety reference section with no safety pass or override.",
        ),
        (
            "retail-dashboard-section-unavailable-v1",
            RetailDashboardSectionKind.UNAVAILABLE_NOTICE,
            "Unavailable Notice Placeholder",
            "Unavailable-by-default section for Prompt 49 planning.",
        ),
    ]
    return [
        RetailDashboardSectionPlaceholder(
            section_id=section_id,
            section_kind=section_kind,
            title=title,
            description=description,
            notes=["Section placeholder is not active UI and not a recommendation surface."],
        )
        for section_id, section_kind, title, description in specs
    ]
