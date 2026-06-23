from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_human_review.workflow import (
    DecisionHumanReviewSafetyLabel,
    DecisionReviewTaskKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_decision_human_review_notes,
)


class DecisionReviewTaskPlaceholder(BaseModel):
    task_id: str
    task_kind: DecisionReviewTaskKind
    title: str
    description: str
    assigned: bool = False
    active: bool = False
    completed: bool = False
    approval_granted: bool = False
    override_granted: bool = False
    recommendation_generated: bool = False
    action_generated: bool = False
    confidence_generated: bool = False
    decision_object_generated: bool = False
    readiness_to_trade_generated: bool = False
    execution_ready: bool = False
    safety_label: DecisionHumanReviewSafetyLabel = DecisionHumanReviewSafetyLabel.WORKFLOW_SKELETON_ONLY
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("task_id", "title", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision review task text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_human_review_notes(value)

    @model_validator(mode="after")
    def task_placeholder_must_remain_inactive(self) -> DecisionReviewTaskPlaceholder:
        if self.task_kind == DecisionReviewTaskKind.UNKNOWN:
            raise ValueError("UNKNOWN review task kind is not allowed")
        if self.assigned:
            raise ValueError("review task assignment is forbidden in Prompt 45")
        if self.active:
            raise ValueError("active review tasks are forbidden in Prompt 45")
        if self.completed:
            raise ValueError("completed review tasks are forbidden in Prompt 45")
        if self.approval_granted:
            raise ValueError("review tasks cannot grant approval in Prompt 45")
        if self.override_granted:
            raise ValueError("review tasks cannot grant override in Prompt 45")
        if self.recommendation_generated:
            raise ValueError("review tasks cannot generate recommendations in Prompt 45")
        if self.action_generated:
            raise ValueError("review tasks cannot generate actions in Prompt 45")
        if self.confidence_generated:
            raise ValueError("review tasks cannot generate confidence scores in Prompt 45")
        if self.decision_object_generated:
            raise ValueError("review tasks cannot generate DecisionObjects in Prompt 45")
        if self.readiness_to_trade_generated:
            raise ValueError("review tasks cannot generate readiness-to-trade in Prompt 45")
        if self.execution_ready:
            raise ValueError("review tasks cannot mark execution ready in Prompt 45")
        if self.safety_label == DecisionHumanReviewSafetyLabel.UNKNOWN:
            raise ValueError("UNKNOWN safety label is not allowed")
        return self


def default_decision_review_task_placeholders() -> list[DecisionReviewTaskPlaceholder]:
    return [
        DecisionReviewTaskPlaceholder(
            task_id="decision-review-task-evidence-placeholder",
            task_kind=DecisionReviewTaskKind.EVIDENCE_REVIEW,
            title="Evidence review placeholder",
            description="Planning-only placeholder for future evidence review workflow.",
            notes=["Not assigned, not active, not approval."],
        ),
        DecisionReviewTaskPlaceholder(
            task_id="decision-review-task-safety-placeholder",
            task_kind=DecisionReviewTaskKind.SAFETY_REVIEW,
            title="Safety review placeholder",
            description="Planning-only placeholder for future safety review workflow.",
            notes=["No override, no approval, no execution."],
        ),
        DecisionReviewTaskPlaceholder(
            task_id="decision-review-task-validation-placeholder",
            task_kind=DecisionReviewTaskKind.VALIDATION_REVIEW,
            title="Validation review placeholder",
            description="Planning-only placeholder for future validation review workflow.",
            notes=["Validation review is not DecisionObject readiness."],
        ),
        DecisionReviewTaskPlaceholder(
            task_id="decision-review-task-display-placeholder",
            task_kind=DecisionReviewTaskKind.DISPLAY_REVIEW,
            title="Display review placeholder",
            description="Planning-only placeholder for future display review workflow.",
            notes=["Display review does not create active UI or recommendation cards."],
        ),
    ]
