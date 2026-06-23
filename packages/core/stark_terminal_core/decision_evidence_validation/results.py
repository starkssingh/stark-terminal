from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_evidence_validation.contracts import (
    DecisionEvidenceValidationIssueSeverity,
    DecisionEvidenceValidationSafetyLabel,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_decision_evidence_validation_notes,
)
from stark_terminal_core.decision_evidence_validation.issues import DecisionEvidenceValidationIssue


class DecisionEvidenceValidationResult(BaseModel):
    result_id: str
    request_id: str
    bundle_id: str | None = None
    valid: bool
    validation_only: bool = True
    issues: list[DecisionEvidenceValidationIssue] = Field(default_factory=list)
    issue_count: int
    blocker_count: int
    warning_count: int
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    execution_allowed: bool = False
    approval_granted: bool = False
    override_granted: bool = False
    readiness_to_trade: bool = False
    safety_label: DecisionEvidenceValidationSafetyLabel = DecisionEvidenceValidationSafetyLabel.VALIDATION_ONLY
    status: str
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("result_id", "request_id", "status", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision evidence validation result text fields")

    @field_validator("bundle_id")
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
    def result_must_remain_validation_only(self) -> DecisionEvidenceValidationResult:
        if not self.validation_only:
            raise ValueError("decision evidence validation results must remain validation-only in Prompt 44")
        if self.issue_count != len(self.issues):
            raise ValueError("issue_count must equal len(issues)")
        expected_blockers = sum(
            1 for issue in self.issues if issue.severity == DecisionEvidenceValidationIssueSeverity.BLOCKER
        )
        if self.blocker_count != expected_blockers:
            raise ValueError("blocker_count must equal count of BLOCKER issues")
        expected_warnings = sum(
            1 for issue in self.issues if issue.severity == DecisionEvidenceValidationIssueSeverity.WARNING
        )
        if self.warning_count != expected_warnings:
            raise ValueError("warning_count must equal count of WARNING issues")
        if self.recommendations_allowed:
            raise ValueError("recommendations are forbidden in Prompt 44")
        if self.action_generation_allowed:
            raise ValueError("action generation is forbidden in Prompt 44")
        if self.confidence_scoring_allowed:
            raise ValueError("confidence scoring is forbidden in Prompt 44")
        if self.decision_object_generation_allowed:
            raise ValueError("DecisionObject generation is forbidden in Prompt 44")
        if self.execution_allowed:
            raise ValueError("execution is forbidden in Prompt 44")
        if self.approval_granted:
            raise ValueError("approval is forbidden in Prompt 44")
        if self.override_granted:
            raise ValueError("override is forbidden in Prompt 44")
        if self.readiness_to_trade:
            raise ValueError("readiness-to-trade is forbidden in Prompt 44")
        if self.safety_label == DecisionEvidenceValidationSafetyLabel.UNKNOWN:
            raise ValueError("decision evidence validation safety label cannot be UNKNOWN")
        return self


def create_decision_evidence_validation_result(
    result_id: str,
    request_id: str,
    valid: bool,
    issues: list[DecisionEvidenceValidationIssue] | None = None,
    bundle_id: str | None = None,
    status: str | None = None,
    notes: list[str] | None = None,
) -> DecisionEvidenceValidationResult:
    resolved_issues = list(issues or [])
    blocker_count = sum(
        1 for issue in resolved_issues if issue.severity == DecisionEvidenceValidationIssueSeverity.BLOCKER
    )
    warning_count = sum(
        1 for issue in resolved_issues if issue.severity == DecisionEvidenceValidationIssueSeverity.WARNING
    )
    return DecisionEvidenceValidationResult(
        result_id=result_id,
        request_id=request_id,
        bundle_id=bundle_id,
        valid=valid,
        issues=resolved_issues,
        issue_count=len(resolved_issues),
        blocker_count=blocker_count,
        warning_count=warning_count,
        status=status or ("valid_validation_only" if valid else "blocked_validation_only"),
        notes=notes or [],
    )


def create_valid_decision_evidence_validation_result(
    request_id: str,
    bundle_id: str | None = None,
) -> DecisionEvidenceValidationResult:
    return create_decision_evidence_validation_result(
        result_id=f"decision-evidence-validation-result-{request_id}",
        request_id=request_id,
        bundle_id=bundle_id,
        valid=True,
        issues=[],
        status="valid_validation_only_not_decision_ready",
        notes=["A valid validation result is not approval, readiness-to-trade, or DecisionObject readiness."],
    )


def create_invalid_decision_evidence_validation_result(
    request_id: str,
    issues: list[DecisionEvidenceValidationIssue],
    bundle_id: str | None = None,
) -> DecisionEvidenceValidationResult:
    return create_decision_evidence_validation_result(
        result_id=f"decision-evidence-validation-result-{request_id}",
        request_id=request_id,
        bundle_id=bundle_id,
        valid=False,
        issues=issues,
        status="blocked_validation_only",
        notes=["Validation blockers do not create recommendations, approvals, readiness-to-trade, or execution."],
    )

