from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_trader_experience_display.contracts import (
    RetailTraderExperienceDisplaySafetyLabel,
    RetailTraderExperienceDisplayWidgetKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_trader_experience_display_notes,
)


class RetailTraderExperienceDisplayWidgetPlaceholder(BaseModel):
    widget_id: str
    widget_kind: RetailTraderExperienceDisplayWidgetKind
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
    suitability_profile_widget: bool = False
    safety_label: RetailTraderExperienceDisplaySafetyLabel = (
        RetailTraderExperienceDisplaySafetyLabel.NOT_A_RECOMMENDATION
    )
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("widget_id", "title", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience display widget text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_trader_experience_display_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def widget_placeholder_must_fail_closed(self) -> RetailTraderExperienceDisplayWidgetPlaceholder:
        if self.widget_kind == RetailTraderExperienceDisplayWidgetKind.UNKNOWN:
            raise ValueError("UNKNOWN Retail Trader Experience Display widget kind is not allowed")
        if self.active_ui or self.rendered_now:
            raise ValueError("Retail Trader Experience Display widget cannot be active or rendered")
        if not self.unavailable:
            raise ValueError("Retail Trader Experience Display widget must remain unavailable")
        if not self.display_contract_only:
            raise ValueError("Retail Trader Experience Display widget must remain display-contract-only")
        if (
            self.recommendation_widget
            or self.action_widget
            or self.confidence_widget
            or self.decision_object_widget
            or self.readiness_to_trade_widget
            or self.broker_control_widget
            or self.execution_widget
            or self.approval_widget
            or self.override_widget
            or self.suitability_profile_widget
        ):
            raise ValueError("Retail Trader Experience Display widget dangerous flags must be false")
        if self.safety_label == RetailTraderExperienceDisplaySafetyLabel.UNKNOWN:
            raise ValueError("Retail Trader Experience Display widget safety label cannot be UNKNOWN")
        return self


def default_retail_trader_experience_display_widget_placeholders() -> list[
    RetailTraderExperienceDisplayWidgetPlaceholder
]:
    return [
        RetailTraderExperienceDisplayWidgetPlaceholder(
            widget_id="placeholder-widget",
            widget_kind=RetailTraderExperienceDisplayWidgetKind.PLACEHOLDER,
            title="Generic display widget placeholder",
            description="Display contract placeholder only; no active widget is rendered.",
        ),
        RetailTraderExperienceDisplayWidgetPlaceholder(
            widget_id="persona-placeholder-widget",
            widget_kind=RetailTraderExperienceDisplayWidgetKind.PERSONA_PLACEHOLDER,
            title="Persona placeholder widget",
            description="Placeholder only; not suitability profiling or trading permission display.",
            safety_label=RetailTraderExperienceDisplaySafetyLabel.NOT_SUITABILITY_PROFILING,
        ),
        RetailTraderExperienceDisplayWidgetPlaceholder(
            widget_id="journey-placeholder-widget",
            widget_kind=RetailTraderExperienceDisplayWidgetKind.JOURNEY_PLACEHOLDER,
            title="Journey placeholder widget",
            description="Placeholder only; not trading advice, readiness-to-trade, or execution.",
        ),
        RetailTraderExperienceDisplayWidgetPlaceholder(
            widget_id="trader-context-placeholder-widget",
            widget_kind=RetailTraderExperienceDisplayWidgetKind.TRADER_CONTEXT_PLACEHOLDER,
            title="Trader context placeholder widget",
            description="Placeholder only; no active personalization, recommendation, or broker linkage.",
        ),
        RetailTraderExperienceDisplayWidgetPlaceholder(
            widget_id="dashboard-context-placeholder-widget",
            widget_kind=RetailTraderExperienceDisplayWidgetKind.DASHBOARD_CONTEXT_PLACEHOLDER,
            title="Dashboard context placeholder widget",
            description="Placeholder only; no active dashboard output, live data, or decision display.",
        ),
        RetailTraderExperienceDisplayWidgetPlaceholder(
            widget_id="data-quality-placeholder-widget",
            widget_kind=RetailTraderExperienceDisplayWidgetKind.DATA_QUALITY_PLACEHOLDER,
            title="Data quality placeholder widget",
            description="Placeholder only; no quality gate can authorize recommendation or execution.",
        ),
        RetailTraderExperienceDisplayWidgetPlaceholder(
            widget_id="safety-placeholder-widget",
            widget_kind=RetailTraderExperienceDisplayWidgetKind.SAFETY_PLACEHOLDER,
            title="Safety placeholder widget",
            description="Placeholder only; no safety pass, approval, override, or readiness-to-trade.",
        ),
        RetailTraderExperienceDisplayWidgetPlaceholder(
            widget_id="educational-placeholder-widget",
            widget_kind=RetailTraderExperienceDisplayWidgetKind.EDUCATIONAL_PLACEHOLDER,
            title="Educational placeholder widget",
            description="Placeholder only; no trading advice, recommendation, or suitability profile.",
        ),
        RetailTraderExperienceDisplayWidgetPlaceholder(
            widget_id="review-placeholder-widget",
            widget_kind=RetailTraderExperienceDisplayWidgetKind.REVIEW_PLACEHOLDER,
            title="Review placeholder widget",
            description="Placeholder only; no active workflow, approval, override, or task assignment.",
        ),
        RetailTraderExperienceDisplayWidgetPlaceholder(
            widget_id="unavailable-widget",
            widget_kind=RetailTraderExperienceDisplayWidgetKind.UNAVAILABLE,
            title="Unavailable widget placeholder",
            description="Fail-closed widget placeholder expected during Prompt 58.",
            safety_label=RetailTraderExperienceDisplaySafetyLabel.DISPLAY_CONTRACT_ONLY,
        ),
    ]
