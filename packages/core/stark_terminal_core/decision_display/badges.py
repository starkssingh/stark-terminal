from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_display.contracts import (
    DecisionDisplayBadgeKind,
    DecisionDisplaySafetyLabel,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_decision_display_notes,
)


class DecisionDisplayBadgePlaceholder(BaseModel):
    badge_id: str
    badge_kind: DecisionDisplayBadgeKind
    label: str
    description: str
    visible: bool = True
    unavailable: bool = True
    planning_only: bool = True
    recommendation: bool = False
    action_signal: bool = False
    confidence_signal: bool = False
    readiness_to_trade: bool = False
    approval_granted: bool = False
    execution_ready: bool = False
    safety_label: DecisionDisplaySafetyLabel = DecisionDisplaySafetyLabel.NOT_A_RECOMMENDATION
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("badge_id", "label", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision display badge text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_display_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def badge_placeholder_must_fail_closed(self) -> DecisionDisplayBadgePlaceholder:
        if self.badge_kind == DecisionDisplayBadgeKind.UNKNOWN:
            raise ValueError("UNKNOWN display badge kind is not allowed")
        if not self.unavailable:
            raise ValueError("Decision display badges must remain unavailable in Prompt 43")
        if not self.planning_only:
            raise ValueError("Decision display badges must remain planning-only")
        if self.recommendation:
            raise ValueError("recommendation badges are forbidden in Prompt 43")
        if self.action_signal:
            raise ValueError("action signal badges are forbidden in Prompt 43")
        if self.confidence_signal:
            raise ValueError("confidence signal badges are forbidden in Prompt 43")
        if self.readiness_to_trade:
            raise ValueError("readiness-to-trade badges are forbidden in Prompt 43")
        if self.approval_granted:
            raise ValueError("approval cannot be granted in Prompt 43")
        if self.execution_ready:
            raise ValueError("execution readiness is forbidden in Prompt 43")
        if self.safety_label == DecisionDisplaySafetyLabel.UNKNOWN:
            raise ValueError("display badge safety label cannot be UNKNOWN")
        return self


def default_decision_display_badges() -> list[DecisionDisplayBadgePlaceholder]:
    return [
        DecisionDisplayBadgePlaceholder(
            badge_id="decision-display-badge-unavailable-v1",
            badge_kind=DecisionDisplayBadgeKind.UNAVAILABLE,
            label="Unavailable",
            description="Display output is unavailable in Prompt 43.",
        ),
        DecisionDisplayBadgePlaceholder(
            badge_id="decision-display-badge-planning-only-v1",
            badge_kind=DecisionDisplayBadgeKind.PLANNING_ONLY,
            label="Planning Only",
            description="Display output is contract metadata only.",
        ),
        DecisionDisplayBadgePlaceholder(
            badge_id="decision-display-badge-not-recommendation-v1",
            badge_kind=DecisionDisplayBadgeKind.NOT_A_RECOMMENDATION,
            label="Not A Recommendation",
            description="Display placeholder is not a recommendation.",
        ),
        DecisionDisplayBadgePlaceholder(
            badge_id="decision-display-badge-human-review-v1",
            badge_kind=DecisionDisplayBadgeKind.HUMAN_REVIEW_REQUIRED,
            label="Human Review Required",
            description="Human review remains required and is not approval.",
        ),
        DecisionDisplayBadgePlaceholder(
            badge_id="decision-display-badge-safety-gated-v1",
            badge_kind=DecisionDisplayBadgeKind.SAFETY_GATED,
            label="Safety Gated",
            description="Safety gates remain fail-closed.",
        ),
    ]

