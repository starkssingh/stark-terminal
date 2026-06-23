from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_evidence.items import (
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_decision_evidence_notes,
)


class DecisionEvidenceHumanReviewAttachment(BaseModel):
    attachment_id: str
    title: str
    description: str
    reviewer_role: str = "human_operator"
    required: bool = True
    completed: bool = False
    approval_granted: bool = False
    blocks_recommendations: bool = True
    blocks_action_generation: bool = True
    blocks_confidence_scoring: bool = True
    blocks_decision_object_generation: bool = True
    blocks_execution: bool = True
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("attachment_id", "title", "description", "reviewer_role", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision evidence human review attachment text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_evidence_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def attachment_must_remain_blocking(self) -> DecisionEvidenceHumanReviewAttachment:
        if self.approval_granted:
            raise ValueError("human-review attachment approval is forbidden in Prompt 38")
        if not self.blocks_recommendations:
            raise ValueError("human-review attachments must block recommendations in Prompt 38")
        if not self.blocks_action_generation:
            raise ValueError("human-review attachments must block action generation in Prompt 38")
        if not self.blocks_confidence_scoring:
            raise ValueError("human-review attachments must block confidence scoring in Prompt 38")
        if not self.blocks_decision_object_generation:
            raise ValueError("human-review attachments must block DecisionObject generation in Prompt 38")
        if not self.blocks_execution:
            raise ValueError("human-review attachments must block execution in Prompt 38")
        return self


class DecisionEvidenceHumanReviewAttachmentSet(BaseModel):
    attachment_set_id: str
    attachments: list[DecisionEvidenceHumanReviewAttachment]
    complete: bool = False
    approval_granted: bool = False
    decision_object_generation_allowed: bool = False
    execution_allowed: bool = False
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("attachment_set_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision evidence human review attachment set text fields")

    @field_validator("attachments")
    @classmethod
    def attachments_must_be_present(
        cls,
        value: list[DecisionEvidenceHumanReviewAttachment],
    ) -> list[DecisionEvidenceHumanReviewAttachment]:
        if not value:
            raise ValueError("decision evidence human review attachments cannot be empty")
        return value

    @field_validator("blockers", "warnings")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_evidence_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def attachment_set_must_not_enable_outputs(self) -> DecisionEvidenceHumanReviewAttachmentSet:
        if self.approval_granted:
            raise ValueError("human-review attachment approval is forbidden in Prompt 38")
        if self.decision_object_generation_allowed:
            raise ValueError("human-review attachments cannot allow DecisionObject generation in Prompt 38")
        if self.execution_allowed:
            raise ValueError("human-review attachments cannot allow execution in Prompt 38")
        if self.complete and self.blockers:
            raise ValueError("complete decision evidence human-review attachment set cannot have blockers")
        return self


def default_decision_evidence_human_review_attachments() -> list[DecisionEvidenceHumanReviewAttachment]:
    return [
        DecisionEvidenceHumanReviewAttachment(
            attachment_id="decision-evidence-human-review-source-chain",
            title="Source Chain Review Attachment",
            description="Planned attachment proving source references were reviewed; it is not approval.",
        ),
        DecisionEvidenceHumanReviewAttachment(
            attachment_id="decision-evidence-human-review-validation",
            title="Validation Checklist Review Attachment",
            description="Planned attachment proving validation checklist review; it does not unlock generation.",
        ),
        DecisionEvidenceHumanReviewAttachment(
            attachment_id="decision-evidence-human-review-safety-boundary",
            title="Safety Boundary Review Attachment",
            description="Planned attachment confirming recommendation, DecisionObject, and execution boundaries.",
        ),
    ]


def build_decision_evidence_human_review_attachment_set(
    attachments: list[DecisionEvidenceHumanReviewAttachment] | None = None,
    completed_attachment_ids: set[str] | None = None,
    warnings: list[str] | None = None,
) -> DecisionEvidenceHumanReviewAttachmentSet:
    resolved_attachments = attachments or default_decision_evidence_human_review_attachments()
    completed = completed_attachment_ids or set()
    blockers = [
        f"missing required decision evidence human-review attachment: {attachment.attachment_id}"
        for attachment in resolved_attachments
        if attachment.required and attachment.attachment_id not in completed
    ]
    return DecisionEvidenceHumanReviewAttachmentSet(
        attachment_set_id="decision-evidence-human-review-attachments-v1",
        attachments=resolved_attachments,
        complete=not blockers,
        blockers=blockers,
        warnings=warnings or [],
    )


def evaluate_decision_evidence_human_review_attachment_set(
    attachment_set: DecisionEvidenceHumanReviewAttachmentSet,
) -> DecisionEvidenceHumanReviewAttachmentSet:
    if attachment_set.complete:
        return attachment_set
    blockers = attachment_set.blockers or ["required decision evidence human-review attachments remain incomplete"]
    return attachment_set.model_copy(update={"blockers": sanitize_decision_evidence_notes(blockers), "complete": False})

