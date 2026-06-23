from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_dashboard_display.contracts import (
    RetailDashboardDisplaySafetyLabel,
    RetailDashboardWidgetKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_dashboard_display_notes,
)


class RetailDashboardWidgetPlaceholder(BaseModel):
    widget_id: str
    widget_kind: RetailDashboardWidgetKind
    title: str
    description: str
    active_ui: bool = False
    rendered_now: bool = False
    unavailable: bool = True
    display_contract_only: bool = True
    recommendation_widget: bool = False
    action_widget: bool = False
    confidence_widget: bool = False
    decision_object_widget: bool = False
    readiness_to_trade_widget: bool = False
    broker_control_widget: bool = False
    execution_widget: bool = False
    approval_widget: bool = False
    override_widget: bool = False
    safety_label: RetailDashboardDisplaySafetyLabel = RetailDashboardDisplaySafetyLabel.NOT_A_RECOMMENDATION
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("widget_id", "title", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard display widget text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_dashboard_display_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def widget_placeholder_must_fail_closed(self) -> RetailDashboardWidgetPlaceholder:
        if self.widget_kind == RetailDashboardWidgetKind.UNKNOWN:
            raise ValueError("UNKNOWN Retail Dashboard widget kind is not allowed")
        if self.active_ui:
            raise ValueError("Retail Dashboard Display widget cannot be active UI in Prompt 51")
        if self.rendered_now:
            raise ValueError("Retail Dashboard Display widget cannot be rendered in Prompt 51")
        if not self.unavailable:
            raise ValueError("Retail Dashboard Display widget must remain unavailable")
        if not self.display_contract_only:
            raise ValueError("Retail Dashboard Display widget must remain contract-only")
        if self.recommendation_widget:
            raise ValueError("Retail Dashboard Display recommendation widgets are forbidden")
        if self.action_widget:
            raise ValueError("Retail Dashboard Display action widgets are forbidden")
        if self.confidence_widget:
            raise ValueError("Retail Dashboard Display confidence widgets are forbidden")
        if self.decision_object_widget:
            raise ValueError("Retail Dashboard Display DecisionObject widgets are forbidden")
        if self.readiness_to_trade_widget:
            raise ValueError("Retail Dashboard Display readiness-to-trade widgets are forbidden")
        if self.broker_control_widget:
            raise ValueError("Retail Dashboard Display broker control widgets are forbidden")
        if self.execution_widget:
            raise ValueError("Retail Dashboard Display execution widgets are forbidden")
        if self.approval_widget:
            raise ValueError("Retail Dashboard Display approval widgets are forbidden")
        if self.override_widget:
            raise ValueError("Retail Dashboard Display override widgets are forbidden")
        if self.safety_label == RetailDashboardDisplaySafetyLabel.UNKNOWN:
            raise ValueError("Retail Dashboard Display widget safety label cannot be UNKNOWN")
        return self


def default_retail_dashboard_widget_placeholders() -> list[RetailDashboardWidgetPlaceholder]:
    return [
        RetailDashboardWidgetPlaceholder(
            widget_id="retail-dashboard-generic-widget-placeholder",
            widget_kind=RetailDashboardWidgetKind.PLACEHOLDER,
            title="Generic widget placeholder",
            description="Display contract placeholder only; no active widget is rendered.",
        ),
        RetailDashboardWidgetPlaceholder(
            widget_id="retail-dashboard-data-quality-widget-placeholder",
            widget_kind=RetailDashboardWidgetKind.DATA_QUALITY_WIDGET_PLACEHOLDER,
            title="Data quality widget placeholder",
            description="Placeholder for future data quality display; no live or real market data is displayed.",
        ),
        RetailDashboardWidgetPlaceholder(
            widget_id="retail-dashboard-market-context-widget-placeholder",
            widget_kind=RetailDashboardWidgetKind.MARKET_CONTEXT_WIDGET_PLACEHOLDER,
            title="Market context widget placeholder",
            description="Placeholder for future context display; not a signal, recommendation, or trading decision.",
        ),
        RetailDashboardWidgetPlaceholder(
            widget_id="retail-dashboard-decision-widget-placeholder",
            widget_kind=RetailDashboardWidgetKind.DECISION_PLACEHOLDER,
            title="Decision placeholder widget",
            description="Placeholder only; no active DecisionObject, recommendation, action, or confidence display.",
        ),
        RetailDashboardWidgetPlaceholder(
            widget_id="retail-dashboard-risk-widget-placeholder",
            widget_kind=RetailDashboardWidgetKind.RISK_PLACEHOLDER,
            title="Risk placeholder widget",
            description="Placeholder only; no readiness-to-trade, broker control, or execution path.",
        ),
        RetailDashboardWidgetPlaceholder(
            widget_id="retail-dashboard-safety-widget-placeholder",
            widget_kind=RetailDashboardWidgetKind.SAFETY_PLACEHOLDER,
            title="Safety placeholder widget",
            description="Placeholder only; no safety pass, approval, override, or execution permission.",
        ),
        RetailDashboardWidgetPlaceholder(
            widget_id="retail-dashboard-review-widget-placeholder",
            widget_kind=RetailDashboardWidgetKind.REVIEW_PLACEHOLDER,
            title="Review placeholder widget",
            description="Placeholder only; no active workflow, task assignment, approval, or override.",
        ),
        RetailDashboardWidgetPlaceholder(
            widget_id="retail-dashboard-unavailable-widget-placeholder",
            widget_kind=RetailDashboardWidgetKind.UNAVAILABLE,
            title="Unavailable widget placeholder",
            description="Fail-closed widget placeholder expected during Prompt 51.",
        ),
    ]
