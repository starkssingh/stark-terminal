from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_dashboard_display.contracts import (
    RetailDashboardDisplayBadgeKind,
    RetailDashboardDisplaySafetyLabel,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_dashboard_display_notes,
)


class RetailDashboardDisplayBadgePlaceholder(BaseModel):
    badge_id: str
    badge_kind: RetailDashboardDisplayBadgeKind
    label: str
    description: str
    visible: bool = True
    active_ui: bool = False
    unavailable: bool = True
    recommendation: bool = False
    action_signal: bool = False
    confidence_signal: bool = False
    decision_object_signal: bool = False
    readiness_to_trade: bool = False
    broker_control: bool = False
    execution_ready: bool = False
    safety_label: RetailDashboardDisplaySafetyLabel = RetailDashboardDisplaySafetyLabel.NOT_A_RECOMMENDATION
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("badge_id", "label", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard display badge text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_dashboard_display_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def badge_placeholder_must_fail_closed(self) -> RetailDashboardDisplayBadgePlaceholder:
        if self.badge_kind == RetailDashboardDisplayBadgeKind.UNKNOWN:
            raise ValueError("UNKNOWN Retail Dashboard display badge kind is not allowed")
        if self.active_ui:
            raise ValueError("Retail Dashboard Display badge cannot be active UI in Prompt 51")
        if not self.unavailable:
            raise ValueError("Retail Dashboard Display badge must remain unavailable")
        if self.recommendation:
            raise ValueError("Retail Dashboard Display recommendation badges are forbidden")
        if self.action_signal:
            raise ValueError("Retail Dashboard Display action badges are forbidden")
        if self.confidence_signal:
            raise ValueError("Retail Dashboard Display confidence badges are forbidden")
        if self.decision_object_signal:
            raise ValueError("Retail Dashboard Display DecisionObject badges are forbidden")
        if self.readiness_to_trade:
            raise ValueError("Retail Dashboard Display readiness-to-trade badges are forbidden")
        if self.broker_control:
            raise ValueError("Retail Dashboard Display broker control badges are forbidden")
        if self.execution_ready:
            raise ValueError("Retail Dashboard Display execution-ready badges are forbidden")
        if self.safety_label == RetailDashboardDisplaySafetyLabel.UNKNOWN:
            raise ValueError("Retail Dashboard Display badge safety label cannot be UNKNOWN")
        return self


def default_retail_dashboard_display_badges() -> list[RetailDashboardDisplayBadgePlaceholder]:
    return [
        RetailDashboardDisplayBadgePlaceholder(
            badge_id="retail-dashboard-planning-only-badge",
            badge_kind=RetailDashboardDisplayBadgeKind.PLANNING_ONLY,
            label="Planning only",
            description="Contract placeholder badge; not active UI and not a recommendation.",
            safety_label=RetailDashboardDisplaySafetyLabel.DISPLAY_CONTRACT_ONLY,
        ),
        RetailDashboardDisplayBadgePlaceholder(
            badge_id="retail-dashboard-unavailable-badge",
            badge_kind=RetailDashboardDisplayBadgeKind.UNAVAILABLE,
            label="Unavailable",
            description="Fail-closed badge placeholder expected during Prompt 51.",
            safety_label=RetailDashboardDisplaySafetyLabel.DISPLAY_CONTRACT_ONLY,
        ),
        RetailDashboardDisplayBadgePlaceholder(
            badge_id="retail-dashboard-not-active-ui-badge",
            badge_kind=RetailDashboardDisplayBadgeKind.NOT_ACTIVE_UI,
            label="Not active UI",
            description="Badge placeholder marks that no frontend or desktop component is rendered.",
            safety_label=RetailDashboardDisplaySafetyLabel.NOT_ACTIVE_UI,
        ),
        RetailDashboardDisplayBadgePlaceholder(
            badge_id="retail-dashboard-not-recommendation-badge",
            badge_kind=RetailDashboardDisplayBadgeKind.NOT_A_RECOMMENDATION,
            label="Not a recommendation",
            description="Badge placeholder cannot be interpreted as buy, sell, hold, watch, or avoid output.",
            safety_label=RetailDashboardDisplaySafetyLabel.NOT_A_RECOMMENDATION,
        ),
        RetailDashboardDisplayBadgePlaceholder(
            badge_id="retail-dashboard-not-readiness-to-trade-badge",
            badge_kind=RetailDashboardDisplayBadgeKind.NOT_READINESS_TO_TRADE,
            label="Not readiness-to-trade",
            description="Badge placeholder does not generate readiness-to-trade status.",
            safety_label=RetailDashboardDisplaySafetyLabel.NOT_READINESS_TO_TRADE,
        ),
        RetailDashboardDisplayBadgePlaceholder(
            badge_id="retail-dashboard-no-broker-control-badge",
            badge_kind=RetailDashboardDisplayBadgeKind.NO_BROKER_CONTROL,
            label="No broker control",
            description="Badge placeholder has no broker linkage, order button, or trading control.",
            safety_label=RetailDashboardDisplaySafetyLabel.NO_BROKER_CONTROL,
        ),
        RetailDashboardDisplayBadgePlaceholder(
            badge_id="retail-dashboard-no-execution-badge",
            badge_kind=RetailDashboardDisplayBadgeKind.NO_EXECUTION,
            label="No execution",
            description="Badge placeholder cannot execute, route, approve, or override trades.",
            safety_label=RetailDashboardDisplaySafetyLabel.NO_EXECUTION,
        ),
    ]
