from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_evidence_validation.contracts import (
    DecisionEvidenceValidationIssueKind,
    DecisionEvidenceValidationIssueSeverity,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_decision_evidence_validation_notes,
)


class DecisionEvidenceValidationIssue(BaseModel):
    issue_id: str
    kind: DecisionEvidenceValidationIssueKind
    severity: DecisionEvidenceValidationIssueSeverity
    message: str
    item_id: str | None = None
    source_id: str | None = None
    blocks_decision_object_generation: bool = True
    blocks_recommendations: bool = True
    blocks_execution: bool = True
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("issue_id", "message", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision evidence validation issue text fields")

    @field_validator("item_id", "source_id")
    @classmethod
    def optional_text_fields_must_be_sanitized(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_evidence_validation_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def issue_must_fail_closed_for_errors(self) -> DecisionEvidenceValidationIssue:
        if self.kind == DecisionEvidenceValidationIssueKind.UNKNOWN:
            raise ValueError("UNKNOWN decision evidence validation issue kind is not allowed")
        if self.severity == DecisionEvidenceValidationIssueSeverity.UNKNOWN:
            raise ValueError("UNKNOWN decision evidence validation issue severity is not allowed")
        if self.severity in {
            DecisionEvidenceValidationIssueSeverity.ERROR,
            DecisionEvidenceValidationIssueSeverity.BLOCKER,
        }:
            if not self.blocks_decision_object_generation:
                raise ValueError("ERROR/BLOCKER issues must block DecisionObject generation")
            if not self.blocks_recommendations:
                raise ValueError("ERROR/BLOCKER issues must block recommendations")
            if not self.blocks_execution:
                raise ValueError("ERROR/BLOCKER issues must block execution")
        return self


def create_validation_issue(
    issue_id: str,
    kind: DecisionEvidenceValidationIssueKind,
    severity: DecisionEvidenceValidationIssueSeverity,
    message: str,
    item_id: str | None = None,
    source_id: str | None = None,
    notes: list[str] | None = None,
) -> DecisionEvidenceValidationIssue:
    return DecisionEvidenceValidationIssue(
        issue_id=issue_id,
        kind=kind,
        severity=severity,
        message=message,
        item_id=item_id,
        source_id=source_id,
        notes=notes or [],
    )


def create_missing_evidence_issue(item_id: str) -> DecisionEvidenceValidationIssue:
    return create_validation_issue(
        issue_id=f"missing-evidence-item-{item_id}",
        kind=DecisionEvidenceValidationIssueKind.MISSING_EVIDENCE_ITEM,
        severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
        message=f"required decision evidence item is missing: {item_id}",
        item_id=item_id,
    )


def create_missing_source_reference_issue(item_id: str) -> DecisionEvidenceValidationIssue:
    return create_validation_issue(
        issue_id=f"missing-source-reference-{item_id}",
        kind=DecisionEvidenceValidationIssueKind.MISSING_SOURCE_REFERENCE,
        severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
        message=f"required source reference is missing for decision evidence item: {item_id}",
        item_id=item_id,
    )


def create_unsafe_flag_issue(item_id: str, flag_name: str) -> DecisionEvidenceValidationIssue:
    return create_validation_issue(
        issue_id=f"unsafe-generated-output-flag-{item_id}-{flag_name}",
        kind=DecisionEvidenceValidationIssueKind.UNSAFE_GENERATED_OUTPUT_FLAG,
        severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
        message=f"unsafe generated output flag is set on {item_id}: {flag_name}",
        item_id=item_id,
    )

