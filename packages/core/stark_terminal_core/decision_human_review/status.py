from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_human_review.workflow import (
    DecisionReviewStatusKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_decision_human_review_notes,
)


class DecisionHumanReviewStatusPlaceholder(BaseModel):
    status_id: str
    status_kind: DecisionReviewStatusKind
    message: str
    workflow_active: bool = False
    tasks_active: bool = False
    approval_granted: bool = False
    override_granted: bool = False
    recommendation_generated: bool = False
    decision_object_generated: bool = False
    readiness_to_trade_generated: bool = False
    execution_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("status_id", "message", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision human review status text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_human_review_notes(value)

    @model_validator(mode="after")
    def status_placeholder_must_remain_inactive(self) -> DecisionHumanReviewStatusPlaceholder:
        if self.status_kind == DecisionReviewStatusKind.UNKNOWN:
            raise ValueError("UNKNOWN human review status kind is not allowed")
        if self.workflow_active:
            raise ValueError("active workflow status is forbidden in Prompt 45")
        if self.tasks_active:
            raise ValueError("active task status is forbidden in Prompt 45")
        if self.approval_granted:
            raise ValueError("human review status cannot grant approval in Prompt 45")
        if self.override_granted:
            raise ValueError("human review status cannot grant override in Prompt 45")
        if self.recommendation_generated:
            raise ValueError("human review status cannot generate recommendations in Prompt 45")
        if self.decision_object_generated:
            raise ValueError("human review status cannot generate DecisionObjects in Prompt 45")
        if self.readiness_to_trade_generated:
            raise ValueError("human review status cannot generate readiness-to-trade in Prompt 45")
        if self.execution_ready:
            raise ValueError("human review status cannot mark execution ready in Prompt 45")
        return self


def default_decision_human_review_status_placeholder() -> DecisionHumanReviewStatusPlaceholder:
    return DecisionHumanReviewStatusPlaceholder(
        status_id="decision-human-review-status-placeholder",
        status_kind=DecisionReviewStatusKind.UNAVAILABLE,
        message="Decision human review workflow is unavailable and skeleton-only in Prompt 45.",
        notes=[
            "No active workflow, task assignment, reviewer auth, notification, approval, override, or execution.",
        ],
    )
