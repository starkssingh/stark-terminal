from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_display.contracts import (
    DecisionDisplayCardKind,
    DecisionDisplaySafetyLabel,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_decision_display_notes,
)


class DecisionDisplayCardPlaceholder(BaseModel):
    card_id: str
    card_kind: DecisionDisplayCardKind
    title: str
    description: str
    visible: bool = True
    unavailable: bool = True
    planning_only: bool = True
    recommendation_generated: bool = False
    action_generated: bool = False
    confidence_generated: bool = False
    decision_object_generated: bool = False
    readiness_to_trade_generated: bool = False
    execution_ready: bool = False
    approval_granted: bool = False
    override_granted: bool = False
    safety_label: DecisionDisplaySafetyLabel = DecisionDisplaySafetyLabel.UNAVAILABLE
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("card_id", "title", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision display card text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_display_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def card_placeholder_must_fail_closed(self) -> DecisionDisplayCardPlaceholder:
        if self.card_kind == DecisionDisplayCardKind.UNKNOWN:
            raise ValueError("UNKNOWN display card kind is not allowed")
        if not self.unavailable:
            raise ValueError("Decision display cards must remain unavailable in Prompt 43")
        if not self.planning_only:
            raise ValueError("Decision display cards must remain planning-only")
        if self.recommendation_generated:
            raise ValueError("recommendation generation is forbidden in Prompt 43")
        if self.action_generated:
            raise ValueError("action generation is forbidden in Prompt 43")
        if self.confidence_generated:
            raise ValueError("confidence scoring is forbidden in Prompt 43")
        if self.decision_object_generated:
            raise ValueError("DecisionObject generation is forbidden in Prompt 43")
        if self.readiness_to_trade_generated:
            raise ValueError("readiness-to-trade is forbidden in Prompt 43")
        if self.execution_ready:
            raise ValueError("execution readiness is forbidden in Prompt 43")
        if self.approval_granted:
            raise ValueError("approval cannot be granted in Prompt 43")
        if self.override_granted:
            raise ValueError("override cannot be granted in Prompt 43")
        if self.safety_label == DecisionDisplaySafetyLabel.UNKNOWN:
            raise ValueError("display card safety label cannot be UNKNOWN")
        return self


def default_decision_display_card_placeholders() -> list[DecisionDisplayCardPlaceholder]:
    return [
        DecisionDisplayCardPlaceholder(
            card_id="decision-display-card-unavailable-v1",
            card_kind=DecisionDisplayCardKind.UNAVAILABLE,
            title="Unavailable Display Placeholder",
            description="Display content remains unavailable and planning-only in Prompt 43.",
            notes=["Not a recommendation card and not an active UI component."],
        ),
        DecisionDisplayCardPlaceholder(
            card_id="decision-display-card-evidence-v1",
            card_kind=DecisionDisplayCardKind.EVIDENCE_PLACEHOLDER,
            title="Evidence Placeholder",
            description="Planned evidence summary placeholder with no validated evidence bundle.",
            notes=["Evidence placeholder does not imply a complete bundle."],
        ),
        DecisionDisplayCardPlaceholder(
            card_id="decision-display-card-risk-v1",
            card_kind=DecisionDisplayCardKind.RISK_PLACEHOLDER,
            title="Risk Placeholder",
            description="Planned risk summary placeholder with no computed decision output.",
            notes=["Risk placeholder does not imply readiness-to-trade."],
        ),
        DecisionDisplayCardPlaceholder(
            card_id="decision-display-card-safety-v1",
            card_kind=DecisionDisplayCardKind.SAFETY_PLACEHOLDER,
            title="Safety Placeholder",
            description="Planned safety status placeholder with no safety pass.",
            notes=["Safety placeholder does not grant approval or override."],
        ),
        DecisionDisplayCardPlaceholder(
            card_id="decision-display-card-human-review-v1",
            card_kind=DecisionDisplayCardKind.HUMAN_REVIEW_PLACEHOLDER,
            title="Human Review Placeholder",
            description="Planned human-review placeholder with no approval granted.",
            notes=["Human review placeholder is not approval."],
        ),
    ]

