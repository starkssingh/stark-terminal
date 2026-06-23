from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_display.cards import (
    DecisionDisplayCardPlaceholder,
    default_decision_display_card_placeholders,
)
from stark_terminal_core.decision_display.contracts import (
    DecisionDisplaySectionKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_decision_display_notes,
)


class DecisionDisplaySectionPlaceholder(BaseModel):
    section_id: str
    section_kind: DecisionDisplaySectionKind
    title: str
    description: str
    cards: list[DecisionDisplayCardPlaceholder]
    visible: bool = True
    unavailable: bool = True
    planning_only: bool = True
    recommendation_generated: bool = False
    action_generated: bool = False
    confidence_generated: bool = False
    decision_object_generated: bool = False
    readiness_to_trade_generated: bool = False
    execution_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("section_id", "title", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision display section text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_display_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def section_placeholder_must_fail_closed(self) -> DecisionDisplaySectionPlaceholder:
        if self.section_kind == DecisionDisplaySectionKind.UNKNOWN:
            raise ValueError("UNKNOWN display section kind is not allowed")
        if not self.cards:
            raise ValueError("display section placeholders require cards")
        if not self.unavailable:
            raise ValueError("Decision display sections must remain unavailable in Prompt 43")
        if not self.planning_only:
            raise ValueError("Decision display sections must remain planning-only")
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
        return self


def default_decision_display_section_placeholders() -> list[DecisionDisplaySectionPlaceholder]:
    cards = default_decision_display_card_placeholders()
    return [
        DecisionDisplaySectionPlaceholder(
            section_id="decision-display-section-header-v1",
            section_kind=DecisionDisplaySectionKind.HEADER,
            title="Display Contract Header Placeholder",
            description="Planned header placeholder with no active UI implementation.",
            cards=[cards[0]],
            notes=["Header placeholder is not an active Decision Desk UI."],
        ),
        DecisionDisplaySectionPlaceholder(
            section_id="decision-display-section-evidence-v1",
            section_kind=DecisionDisplaySectionKind.EVIDENCE_SUMMARY,
            title="Evidence Summary Placeholder",
            description="Planned evidence summary section with no validated evidence display.",
            cards=[cards[1]],
        ),
        DecisionDisplaySectionPlaceholder(
            section_id="decision-display-section-risk-v1",
            section_kind=DecisionDisplaySectionKind.RISK_SUMMARY,
            title="Risk Summary Placeholder",
            description="Planned risk summary section with no readiness-to-trade display.",
            cards=[cards[2]],
        ),
        DecisionDisplaySectionPlaceholder(
            section_id="decision-display-section-human-review-v1",
            section_kind=DecisionDisplaySectionKind.HUMAN_REVIEW,
            title="Human Review Placeholder",
            description="Planned human-review section with no approval display.",
            cards=[cards[4]],
        ),
        DecisionDisplaySectionPlaceholder(
            section_id="decision-display-section-safety-v1",
            section_kind=DecisionDisplaySectionKind.SAFETY_STATUS,
            title="Safety Status Placeholder",
            description="Planned safety section with no safety pass or override display.",
            cards=[cards[3]],
        ),
        DecisionDisplaySectionPlaceholder(
            section_id="decision-display-section-unavailable-v1",
            section_kind=DecisionDisplaySectionKind.UNAVAILABLE_NOTICE,
            title="Unavailable Notice Placeholder",
            description="Unavailable notice section for the display contract skeleton.",
            cards=[cards[0]],
        ),
    ]

