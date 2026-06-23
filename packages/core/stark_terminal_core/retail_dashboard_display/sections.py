from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_dashboard_display.contracts import (
    RetailDashboardVisualSectionKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_dashboard_display_notes,
)


class RetailDashboardVisualSectionPlaceholder(BaseModel):
    section_id: str
    section_kind: RetailDashboardVisualSectionKind
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
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("section_id", "title", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard display visual section text fields")

    @field_validator("widget_ids", "notes")
    @classmethod
    def list_fields_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_dashboard_display_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def section_placeholder_must_fail_closed(self) -> RetailDashboardVisualSectionPlaceholder:
        if self.section_kind == RetailDashboardVisualSectionKind.UNKNOWN:
            raise ValueError("UNKNOWN Retail Dashboard visual section kind is not allowed")
        if self.active_ui:
            raise ValueError("Retail Dashboard Display section cannot be active UI in Prompt 51")
        if self.rendered_now:
            raise ValueError("Retail Dashboard Display section cannot be rendered in Prompt 51")
        if not self.unavailable:
            raise ValueError("Retail Dashboard Display section must remain unavailable")
        if not self.display_contract_only:
            raise ValueError("Retail Dashboard Display section must remain contract-only")
        if self.recommendations_allowed:
            raise ValueError("Retail Dashboard Display section cannot allow recommendations")
        if self.action_generation_allowed:
            raise ValueError("Retail Dashboard Display section cannot allow action generation")
        if self.confidence_scoring_allowed:
            raise ValueError("Retail Dashboard Display section cannot allow confidence scoring")
        if self.decision_object_generation_allowed:
            raise ValueError("Retail Dashboard Display section cannot allow DecisionObject generation")
        if self.readiness_to_trade_allowed:
            raise ValueError("Retail Dashboard Display section cannot allow readiness-to-trade")
        if self.broker_controls_allowed:
            raise ValueError("Retail Dashboard Display section cannot allow broker controls")
        if self.execution_allowed:
            raise ValueError("Retail Dashboard Display section cannot allow execution")
        return self


def default_retail_dashboard_visual_section_placeholders() -> list[RetailDashboardVisualSectionPlaceholder]:
    return [
        RetailDashboardVisualSectionPlaceholder(
            section_id="header",
            section_kind=RetailDashboardVisualSectionKind.HEADER,
            title="Header visual section placeholder",
            description="Placeholder for a future header; no active UI or frontend component is produced.",
            widget_ids=["retail-dashboard-generic-widget-placeholder"],
        ),
        RetailDashboardVisualSectionPlaceholder(
            section_id="overview",
            section_kind=RetailDashboardVisualSectionKind.OVERVIEW,
            title="Overview visual section placeholder",
            description="Placeholder for future overview layout; unavailable by default.",
            widget_ids=["retail-dashboard-market-context-widget-placeholder"],
        ),
        RetailDashboardVisualSectionPlaceholder(
            section_id="data_quality",
            section_kind=RetailDashboardVisualSectionKind.DATA_QUALITY,
            title="Data quality visual section placeholder",
            description="Placeholder for future data quality display; not a live data display.",
            widget_ids=["retail-dashboard-data-quality-widget-placeholder"],
        ),
        RetailDashboardVisualSectionPlaceholder(
            section_id="market_context",
            section_kind=RetailDashboardVisualSectionKind.MARKET_CONTEXT,
            title="Market context visual section placeholder",
            description="Placeholder for future market context; no recommendation or signal is generated.",
            widget_ids=["retail-dashboard-market-context-widget-placeholder"],
        ),
        RetailDashboardVisualSectionPlaceholder(
            section_id="decision_placeholder",
            section_kind=RetailDashboardVisualSectionKind.DECISION_PLACEHOLDER,
            title="Decision visual section placeholder",
            description="Placeholder only; no active DecisionObject, confidence, action, or recommendation display.",
            widget_ids=["retail-dashboard-decision-widget-placeholder"],
        ),
        RetailDashboardVisualSectionPlaceholder(
            section_id="risk_context",
            section_kind=RetailDashboardVisualSectionKind.RISK_CONTEXT,
            title="Risk context visual section placeholder",
            description="Placeholder only; no readiness-to-trade, broker controls, or execution controls.",
            widget_ids=["retail-dashboard-risk-widget-placeholder"],
        ),
        RetailDashboardVisualSectionPlaceholder(
            section_id="human_review",
            section_kind=RetailDashboardVisualSectionKind.HUMAN_REVIEW,
            title="Human review visual section placeholder",
            description="Placeholder only; no active workflow, approval, override, or task assignment.",
            widget_ids=["retail-dashboard-review-widget-placeholder"],
        ),
        RetailDashboardVisualSectionPlaceholder(
            section_id="safety_status",
            section_kind=RetailDashboardVisualSectionKind.SAFETY_STATUS,
            title="Safety status visual section placeholder",
            description="Placeholder only; no safety pass, approval, readiness-to-trade, or execution permission.",
            widget_ids=["retail-dashboard-safety-widget-placeholder"],
        ),
        RetailDashboardVisualSectionPlaceholder(
            section_id="unavailable_notice",
            section_kind=RetailDashboardVisualSectionKind.UNAVAILABLE_NOTICE,
            title="Unavailable notice visual section placeholder",
            description="Fail-closed display section placeholder expected during Prompt 51.",
            widget_ids=["retail-dashboard-unavailable-widget-placeholder"],
        ),
    ]
