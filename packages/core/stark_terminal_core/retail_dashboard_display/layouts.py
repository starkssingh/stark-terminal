from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_dashboard_display.contracts import (
    RetailDashboardDisplaySafetyLabel,
    RetailDashboardLayoutKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_dashboard_display_notes,
)


class RetailDashboardLayoutPlaceholder(BaseModel):
    layout_id: str
    layout_kind: RetailDashboardLayoutKind
    title: str
    description: str
    section_ids: list[str] = Field(default_factory=list)
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
    safety_label: RetailDashboardDisplaySafetyLabel = RetailDashboardDisplaySafetyLabel.DISPLAY_CONTRACT_ONLY
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("layout_id", "title", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard display layout text fields")

    @field_validator("section_ids", "notes")
    @classmethod
    def list_fields_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_dashboard_display_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def layout_placeholder_must_fail_closed(self) -> RetailDashboardLayoutPlaceholder:
        if self.layout_kind == RetailDashboardLayoutKind.UNKNOWN:
            raise ValueError("UNKNOWN Retail Dashboard layout kind is not allowed")
        if self.active_ui:
            raise ValueError("Retail Dashboard Display layout cannot be active UI in Prompt 51")
        if self.rendered_now:
            raise ValueError("Retail Dashboard Display layout cannot be rendered in Prompt 51")
        if not self.unavailable:
            raise ValueError("Retail Dashboard Display layout must remain unavailable")
        if not self.display_contract_only:
            raise ValueError("Retail Dashboard Display layout must remain contract-only")
        if self.recommendations_allowed:
            raise ValueError("Retail Dashboard Display layout cannot allow recommendations")
        if self.action_generation_allowed:
            raise ValueError("Retail Dashboard Display layout cannot allow action generation")
        if self.confidence_scoring_allowed:
            raise ValueError("Retail Dashboard Display layout cannot allow confidence scoring")
        if self.decision_object_generation_allowed:
            raise ValueError("Retail Dashboard Display layout cannot allow DecisionObject generation")
        if self.readiness_to_trade_allowed:
            raise ValueError("Retail Dashboard Display layout cannot allow readiness-to-trade")
        if self.broker_controls_allowed:
            raise ValueError("Retail Dashboard Display layout cannot allow broker controls")
        if self.execution_allowed:
            raise ValueError("Retail Dashboard Display layout cannot allow execution")
        if self.safety_label == RetailDashboardDisplaySafetyLabel.UNKNOWN:
            raise ValueError("Retail Dashboard Display layout safety label cannot be UNKNOWN")
        return self


def default_retail_dashboard_layout_placeholders() -> list[RetailDashboardLayoutPlaceholder]:
    return [
        RetailDashboardLayoutPlaceholder(
            layout_id="retail-dashboard-desktop-shell-layout-placeholder",
            layout_kind=RetailDashboardLayoutKind.DESKTOP_SHELL_PLACEHOLDER,
            title="Desktop shell layout placeholder",
            description="Contract placeholder for a future Windows-native shell; no frontend or desktop UI is rendered.",
            section_ids=["header", "overview", "unavailable_notice"],
            notes=["Display contract only; not active UI."],
        ),
        RetailDashboardLayoutPlaceholder(
            layout_id="retail-dashboard-overview-layout-placeholder",
            layout_kind=RetailDashboardLayoutKind.RETAIL_OVERVIEW_PLACEHOLDER,
            title="Retail overview layout placeholder",
            description="Contract placeholder for future overview composition; unavailable by default.",
            section_ids=["overview", "data_quality", "market_context"],
        ),
        RetailDashboardLayoutPlaceholder(
            layout_id="retail-dashboard-instrument-detail-layout-placeholder",
            layout_kind=RetailDashboardLayoutKind.INSTRUMENT_DETAIL_PLACEHOLDER,
            title="Instrument detail layout placeholder",
            description="Contract placeholder for future instrument context; no live or real market data display.",
            section_ids=["market_context", "risk_context", "safety_status"],
        ),
        RetailDashboardLayoutPlaceholder(
            layout_id="retail-dashboard-risk-context-layout-placeholder",
            layout_kind=RetailDashboardLayoutKind.RISK_CONTEXT_PLACEHOLDER,
            title="Risk context layout placeholder",
            description="Contract placeholder for future risk context; not a recommendation or readiness-to-trade surface.",
            section_ids=["risk_context", "safety_status"],
        ),
        RetailDashboardLayoutPlaceholder(
            layout_id="retail-dashboard-safety-layout-placeholder",
            layout_kind=RetailDashboardLayoutKind.SAFETY_PLACEHOLDER,
            title="Safety layout placeholder",
            description="Contract placeholder for future safety messaging; no approval, override, broker, or execution controls.",
            section_ids=["safety_status", "human_review"],
        ),
        RetailDashboardLayoutPlaceholder(
            layout_id="retail-dashboard-unavailable-layout-placeholder",
            layout_kind=RetailDashboardLayoutKind.UNAVAILABLE,
            title="Unavailable layout placeholder",
            description="Fail-closed layout placeholder expected during the display contract skeleton phase.",
            section_ids=["unavailable_notice"],
        ),
    ]
