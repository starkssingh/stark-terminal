from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_dashboard.planning import (
    RetailDashboardCardKind,
    RetailDashboardSafetyLabel,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_dashboard_notes,
)


class RetailDashboardCardPlaceholder(BaseModel):
    card_id: str
    card_kind: RetailDashboardCardKind
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
    safety_label: RetailDashboardSafetyLabel = RetailDashboardSafetyLabel.NOT_A_RECOMMENDATION
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("card_id", "title", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard card text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_dashboard_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def card_placeholder_must_fail_closed(self) -> RetailDashboardCardPlaceholder:
        if self.card_kind == RetailDashboardCardKind.UNKNOWN:
            raise ValueError("UNKNOWN retail dashboard card kind is not allowed")
        if self.active_ui:
            raise ValueError("retail dashboard card placeholder cannot be active UI")
        if not self.unavailable:
            raise ValueError("retail dashboard card placeholder must remain unavailable")
        if not self.planning_only:
            raise ValueError("retail dashboard card placeholder must remain planning-only")
        if self.recommendation_card:
            raise ValueError("retail dashboard recommendation cards are forbidden")
        if self.action_card:
            raise ValueError("retail dashboard action cards are forbidden")
        if self.confidence_display:
            raise ValueError("retail dashboard confidence display is forbidden")
        if self.decision_object_display:
            raise ValueError("retail dashboard DecisionObject display is forbidden")
        if self.readiness_to_trade_display:
            raise ValueError("retail dashboard readiness-to-trade display is forbidden")
        if self.broker_control:
            raise ValueError("retail dashboard broker controls are forbidden")
        if self.execution_control:
            raise ValueError("retail dashboard execution controls are forbidden")
        if self.approval_control:
            raise ValueError("retail dashboard approval controls are forbidden")
        if self.override_control:
            raise ValueError("retail dashboard override controls are forbidden")
        if self.safety_label == RetailDashboardSafetyLabel.UNKNOWN:
            raise ValueError("retail dashboard card safety label cannot be UNKNOWN")
        return self


def default_retail_dashboard_card_placeholders() -> list[RetailDashboardCardPlaceholder]:
    specs = [
        (
            "retail-dashboard-card-placeholder-v1",
            RetailDashboardCardKind.PLACEHOLDER,
            "Dashboard Placeholder",
            "Generic planning-only dashboard card placeholder.",
        ),
        (
            "retail-dashboard-card-data-quality-v1",
            RetailDashboardCardKind.DATA_QUALITY_PLACEHOLDER,
            "Data Quality Placeholder",
            "Planning-only data quality card with no active data display.",
        ),
        (
            "retail-dashboard-card-market-context-v1",
            RetailDashboardCardKind.MARKET_CONTEXT_PLACEHOLDER,
            "Market Context Placeholder",
            "Planning-only market context card with no live market data or signal.",
        ),
        (
            "retail-dashboard-card-decision-v1",
            RetailDashboardCardKind.DECISION_PLACEHOLDER,
            "Decision Placeholder",
            "Planning-only decision reference card with no DecisionObject display.",
        ),
        (
            "retail-dashboard-card-risk-v1",
            RetailDashboardCardKind.RISK_PLACEHOLDER,
            "Risk Placeholder",
            "Planning-only risk card with no readiness-to-trade display.",
        ),
        (
            "retail-dashboard-card-review-v1",
            RetailDashboardCardKind.REVIEW_PLACEHOLDER,
            "Review Placeholder",
            "Planning-only review card with no approval or override.",
        ),
        (
            "retail-dashboard-card-safety-v1",
            RetailDashboardCardKind.SAFETY_PLACEHOLDER,
            "Safety Placeholder",
            "Planning-only safety card with no active safety pass.",
        ),
        (
            "retail-dashboard-card-unavailable-v1",
            RetailDashboardCardKind.UNAVAILABLE,
            "Unavailable Placeholder",
            "Unavailable-by-default card for Prompt 49 planning.",
        ),
    ]
    return [
        RetailDashboardCardPlaceholder(
            card_id=card_id,
            card_kind=card_kind,
            title=title,
            description=description,
            notes=["Card placeholder is not a recommendation card, action card, broker control, or execution control."],
        )
        for card_id, card_kind, title, description in specs
    ]
