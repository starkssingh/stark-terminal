from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_human_review.workflow import (
    DecisionReviewQueueKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_decision_human_review_notes,
)


class DecisionReviewQueuePlaceholder(BaseModel):
    queue_id: str
    queue_kind: DecisionReviewQueueKind
    name: str
    description: str
    active_queue: bool = False
    persisted: bool = False
    task_assignment_allowed: bool = False
    notifications_allowed: bool = False
    approval_allowed: bool = False
    override_allowed: bool = False
    execution_allowed: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("queue_id", "name", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision review queue text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_human_review_notes(value)

    @model_validator(mode="after")
    def queue_placeholder_must_remain_inactive(self) -> DecisionReviewQueuePlaceholder:
        if self.queue_kind == DecisionReviewQueueKind.UNKNOWN:
            raise ValueError("UNKNOWN review queue kind is not allowed")
        if self.active_queue:
            raise ValueError("active review queues are forbidden in Prompt 45")
        if self.persisted:
            raise ValueError("review queue persistence is forbidden in Prompt 45")
        if self.task_assignment_allowed:
            raise ValueError("review queue task assignment is forbidden in Prompt 45")
        if self.notifications_allowed:
            raise ValueError("review queue notifications are forbidden in Prompt 45")
        if self.approval_allowed:
            raise ValueError("review queues cannot approve in Prompt 45")
        if self.override_allowed:
            raise ValueError("review queues cannot override in Prompt 45")
        if self.execution_allowed:
            raise ValueError("review queues cannot execute in Prompt 45")
        return self


def default_decision_review_queue_placeholders() -> list[DecisionReviewQueuePlaceholder]:
    return [
        DecisionReviewQueuePlaceholder(
            queue_id="decision-review-queue-placeholder",
            queue_kind=DecisionReviewQueueKind.PLACEHOLDER_QUEUE,
            name="Placeholder review queue",
            description="Planning-only queue placeholder; no persistence or task assignment.",
            notes=["Queue is not active and has no approval path."],
        ),
        DecisionReviewQueuePlaceholder(
            queue_id="decision-review-queue-evidence-placeholder",
            queue_kind=DecisionReviewQueueKind.EVIDENCE_QUEUE,
            name="Evidence review queue placeholder",
            description="Planning-only evidence queue placeholder.",
            notes=["Queue cannot assign tasks or send notifications."],
        ),
        DecisionReviewQueuePlaceholder(
            queue_id="decision-review-queue-safety-placeholder",
            queue_kind=DecisionReviewQueueKind.SAFETY_QUEUE,
            name="Safety review queue placeholder",
            description="Planning-only safety queue placeholder.",
            notes=["Queue cannot override safety guardrails."],
        ),
    ]
