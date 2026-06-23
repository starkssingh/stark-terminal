from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_human_review.workflow import (
    DecisionHumanReviewSafetyLabel,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_decision_human_review_notes,
)


class DecisionHumanReviewUnavailableResponse(BaseModel):
    response_id: str
    unavailable: bool = True
    message: str
    workflow_skeleton_only: bool = True
    active_workflow_allowed: bool = False
    task_assignment_allowed: bool = False
    reviewer_auth_allowed: bool = False
    notifications_allowed: bool = False
    approval_allowed: bool = False
    override_allowed: bool = False
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    readiness_to_trade_allowed: bool = False
    execution_allowed: bool = False
    safety_label: DecisionHumanReviewSafetyLabel = DecisionHumanReviewSafetyLabel.NOT_APPROVAL
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("response_id", "message", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision human review unavailable response text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_human_review_notes(value)

    @model_validator(mode="after")
    def unavailable_response_must_fail_closed(self) -> DecisionHumanReviewUnavailableResponse:
        if not self.unavailable:
            raise ValueError("decision human review unavailable response must be unavailable")
        if not self.workflow_skeleton_only:
            raise ValueError("decision human review response must remain workflow skeleton only")
        if self.active_workflow_allowed:
            raise ValueError("active workflow is forbidden in Prompt 45")
        if self.task_assignment_allowed:
            raise ValueError("task assignment is forbidden in Prompt 45")
        if self.reviewer_auth_allowed:
            raise ValueError("reviewer auth is forbidden in Prompt 45")
        if self.notifications_allowed:
            raise ValueError("notifications are forbidden in Prompt 45")
        if self.approval_allowed:
            raise ValueError("approval is forbidden in Prompt 45")
        if self.override_allowed:
            raise ValueError("override is forbidden in Prompt 45")
        if self.recommendations_allowed:
            raise ValueError("recommendations are forbidden in Prompt 45")
        if self.action_generation_allowed:
            raise ValueError("action generation is forbidden in Prompt 45")
        if self.confidence_scoring_allowed:
            raise ValueError("confidence scoring is forbidden in Prompt 45")
        if self.decision_object_generation_allowed:
            raise ValueError("DecisionObject generation is forbidden in Prompt 45")
        if self.readiness_to_trade_allowed:
            raise ValueError("readiness-to-trade is forbidden in Prompt 45")
        if self.execution_allowed:
            raise ValueError("execution is forbidden in Prompt 45")
        if self.safety_label == DecisionHumanReviewSafetyLabel.UNKNOWN:
            raise ValueError("UNKNOWN safety label is not allowed")
        return self


def default_decision_human_review_unavailable_response() -> DecisionHumanReviewUnavailableResponse:
    return DecisionHumanReviewUnavailableResponse(
        response_id="decision-human-review-unavailable-response-v1",
        message="Decision human review workflow is unavailable; Prompt 45 exposes skeleton contracts only.",
        notes=[
            "No active workflow, task assignment, reviewer auth, notifications, approval, override, or execution.",
            "Human review placeholders are not recommendations or readiness-to-trade.",
        ],
    )
