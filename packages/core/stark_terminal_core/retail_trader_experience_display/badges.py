from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_trader_experience_display.contracts import (
    RetailTraderExperienceDisplayBadgeKind,
    RetailTraderExperienceDisplaySafetyLabel,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_trader_experience_display_notes,
)


class RetailTraderExperienceDisplayBadgePlaceholder(BaseModel):
    badge_id: str
    badge_kind: RetailTraderExperienceDisplayBadgeKind
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
    suitability_profile: bool = False
    safety_label: RetailTraderExperienceDisplaySafetyLabel = (
        RetailTraderExperienceDisplaySafetyLabel.NOT_A_RECOMMENDATION
    )
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("badge_id", "label", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience display badge text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_trader_experience_display_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def badge_placeholder_must_fail_closed(self) -> RetailTraderExperienceDisplayBadgePlaceholder:
        if self.badge_kind == RetailTraderExperienceDisplayBadgeKind.UNKNOWN:
            raise ValueError("UNKNOWN Retail Trader Experience Display badge kind is not allowed")
        if self.active_ui:
            raise ValueError("Retail Trader Experience Display badge cannot be active UI")
        if not self.unavailable:
            raise ValueError("Retail Trader Experience Display badge must remain unavailable")
        if (
            self.recommendation
            or self.action_signal
            or self.confidence_signal
            or self.decision_object_signal
            or self.readiness_to_trade
            or self.broker_control
            or self.execution_ready
            or self.suitability_profile
        ):
            raise ValueError("Retail Trader Experience Display badge dangerous flags must be false")
        if self.safety_label == RetailTraderExperienceDisplaySafetyLabel.UNKNOWN:
            raise ValueError("Retail Trader Experience Display badge safety label cannot be UNKNOWN")
        return self


def default_retail_trader_experience_display_badges() -> list[
    RetailTraderExperienceDisplayBadgePlaceholder
]:
    return [
        RetailTraderExperienceDisplayBadgePlaceholder(
            badge_id="planning-only-badge",
            badge_kind=RetailTraderExperienceDisplayBadgeKind.PLANNING_ONLY,
            label="Planning only",
            description="Display contract badge placeholder; not active UI and not a recommendation.",
            safety_label=RetailTraderExperienceDisplaySafetyLabel.DISPLAY_CONTRACT_ONLY,
        ),
        RetailTraderExperienceDisplayBadgePlaceholder(
            badge_id="unavailable-badge",
            badge_kind=RetailTraderExperienceDisplayBadgeKind.UNAVAILABLE,
            label="Unavailable",
            description="Fail-closed badge placeholder expected during Prompt 58.",
            safety_label=RetailTraderExperienceDisplaySafetyLabel.DISPLAY_CONTRACT_ONLY,
        ),
        RetailTraderExperienceDisplayBadgePlaceholder(
            badge_id="not-active-ui-badge",
            badge_kind=RetailTraderExperienceDisplayBadgeKind.NOT_ACTIVE_UI,
            label="Not active UI",
            description="Badge placeholder marks that no frontend or desktop component is rendered.",
            safety_label=RetailTraderExperienceDisplaySafetyLabel.NOT_ACTIVE_UI,
        ),
        RetailTraderExperienceDisplayBadgePlaceholder(
            badge_id="not-recommendation-badge",
            badge_kind=RetailTraderExperienceDisplayBadgeKind.NOT_A_RECOMMENDATION,
            label="Not a recommendation",
            description="Badge placeholder cannot be interpreted as buy, sell, hold, watch, or avoid output.",
            safety_label=RetailTraderExperienceDisplaySafetyLabel.NOT_A_RECOMMENDATION,
        ),
        RetailTraderExperienceDisplayBadgePlaceholder(
            badge_id="not-readiness-to-trade-badge",
            badge_kind=RetailTraderExperienceDisplayBadgeKind.NOT_READINESS_TO_TRADE,
            label="Not readiness-to-trade",
            description="Badge placeholder does not generate readiness-to-trade status.",
            safety_label=RetailTraderExperienceDisplaySafetyLabel.NOT_READINESS_TO_TRADE,
        ),
        RetailTraderExperienceDisplayBadgePlaceholder(
            badge_id="no-broker-control-badge",
            badge_kind=RetailTraderExperienceDisplayBadgeKind.NO_BROKER_CONTROL,
            label="No broker control",
            description="Badge placeholder has no broker linkage, order button, or trading control.",
            safety_label=RetailTraderExperienceDisplaySafetyLabel.NO_BROKER_CONTROL,
        ),
        RetailTraderExperienceDisplayBadgePlaceholder(
            badge_id="no-execution-badge",
            badge_kind=RetailTraderExperienceDisplayBadgeKind.NO_EXECUTION,
            label="No execution",
            description="Badge placeholder cannot execute, route, approve, or override trades.",
            safety_label=RetailTraderExperienceDisplaySafetyLabel.NO_EXECUTION,
        ),
        RetailTraderExperienceDisplayBadgePlaceholder(
            badge_id="not-suitability-profiling-badge",
            badge_kind=RetailTraderExperienceDisplayBadgeKind.NOT_SUITABILITY_PROFILING,
            label="Not suitability profiling",
            description="Badge placeholder is not a suitability profile or trading permission profile.",
            safety_label=RetailTraderExperienceDisplaySafetyLabel.NOT_SUITABILITY_PROFILING,
        ),
    ]
