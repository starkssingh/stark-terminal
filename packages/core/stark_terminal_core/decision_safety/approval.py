from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_safety.guardrails import (
    DecisionApprovalPlaceholderStatus,
    DecisionSafetyLabel,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_decision_safety_notes,
)


class DecisionApprovalPlaceholder(BaseModel):
    approval_id: str
    title: str
    description: str
    status: DecisionApprovalPlaceholderStatus = DecisionApprovalPlaceholderStatus.PLACEHOLDER_ONLY
    approval_granted: bool = False
    active_workflow: bool = False
    grants_recommendations: bool = False
    grants_action_generation: bool = False
    grants_confidence_scoring: bool = False
    grants_decision_object_generation: bool = False
    grants_execution: bool = False
    safety_label: DecisionSafetyLabel = DecisionSafetyLabel.NOT_APPROVAL
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("approval_id", "title", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision approval placeholder text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_safety_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def placeholder_must_not_grant_anything(self) -> DecisionApprovalPlaceholder:
        if self.status == DecisionApprovalPlaceholderStatus.UNKNOWN:
            raise ValueError("approval placeholder status cannot be UNKNOWN")
        if self.approval_granted:
            raise ValueError("approval cannot be granted in Prompt 39")
        if self.active_workflow:
            raise ValueError("active approval workflows are forbidden in Prompt 39")
        if self.grants_recommendations:
            raise ValueError("approval placeholders cannot grant recommendations in Prompt 39")
        if self.grants_action_generation:
            raise ValueError("approval placeholders cannot grant action generation in Prompt 39")
        if self.grants_confidence_scoring:
            raise ValueError("approval placeholders cannot grant confidence scoring in Prompt 39")
        if self.grants_decision_object_generation:
            raise ValueError("approval placeholders cannot grant DecisionObject generation in Prompt 39")
        if self.grants_execution:
            raise ValueError("approval placeholders cannot grant execution in Prompt 39")
        if self.safety_label == DecisionSafetyLabel.UNKNOWN:
            raise ValueError("approval placeholder safety label cannot be UNKNOWN")
        return self


def default_decision_approval_placeholders() -> list[DecisionApprovalPlaceholder]:
    definitions = [
        (
            "decision-approval-placeholder-human-operator",
            "Human Operator Approval Placeholder",
            "Placeholder for a future approval workflow; it is inactive and grants nothing.",
        ),
        (
            "decision-approval-placeholder-compliance",
            "Compliance Approval Placeholder",
            "Placeholder for future compliance review; it is inactive and grants nothing.",
        ),
    ]
    return [
        DecisionApprovalPlaceholder(
            approval_id=approval_id,
            title=title,
            description=description,
            notes=["Approval placeholder only; no approval is granted."],
        )
        for approval_id, title, description in definitions
    ]


def evaluate_decision_approval_placeholders(
    placeholders: list[DecisionApprovalPlaceholder],
) -> list[str]:
    blockers: list[str] = []
    if not placeholders:
        blockers.append("decision approval placeholders are missing")
    for placeholder in placeholders:
        if placeholder.approval_granted:
            blockers.append(f"{placeholder.approval_id}: approval cannot be granted")
        if placeholder.active_workflow:
            blockers.append(f"{placeholder.approval_id}: active approval workflow is forbidden")
        if (
            placeholder.grants_recommendations
            or placeholder.grants_action_generation
            or placeholder.grants_confidence_scoring
            or placeholder.grants_decision_object_generation
            or placeholder.grants_execution
        ):
            blockers.append(f"{placeholder.approval_id}: placeholder cannot grant dangerous outputs")
    return blockers
