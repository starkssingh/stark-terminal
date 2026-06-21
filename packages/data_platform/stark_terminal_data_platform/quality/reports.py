from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_data_platform.quality.enums import (
    ValidationScope,
    ValidationSeverity,
    ValidationStatus,
)
from stark_terminal_data_platform.quality.issues import SECRET_TEXT_PARTS, text_has_sensitive_content
from stark_terminal_data_platform.quality.results import ValidationResult


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _status_from_results(results: list[ValidationResult]) -> ValidationStatus:
    if any(result.status == ValidationStatus.BLOCKED for result in results):
        return ValidationStatus.BLOCKED
    severities = {
        issue.severity
        for result in results
        for issue in result.issues
    }
    if ValidationSeverity.CRITICAL in severities:
        return ValidationStatus.BLOCKED
    if ValidationSeverity.ERROR in severities:
        return ValidationStatus.FAIL
    if ValidationSeverity.WARNING in severities or any(result.status == ValidationStatus.WARN for result in results):
        return ValidationStatus.WARN
    if all(result.status == ValidationStatus.PASS for result in results):
        return ValidationStatus.PASS
    return ValidationStatus.UNKNOWN


def _issue_counts(results: list[ValidationResult]) -> tuple[int, int, int, int]:
    issues = [issue for result in results for issue in result.issues]
    warnings = sum(1 for issue in issues if issue.severity == ValidationSeverity.WARNING)
    errors = sum(1 for issue in issues if issue.severity == ValidationSeverity.ERROR)
    critical = sum(1 for issue in issues if issue.severity == ValidationSeverity.CRITICAL)
    return len(issues), warnings, errors, critical


class ValidationReport(BaseModel):
    report_id: str
    scope: ValidationScope
    subject_id: str
    status: ValidationStatus
    results: list[ValidationResult]
    issue_count: int
    warning_count: int
    error_count: int
    critical_count: int
    generated_at: datetime = Field(default_factory=_utc_now)
    schema_version: str = "v1"
    source_data_reference: str | None = None
    notes: list[str] = Field(default_factory=list)

    @field_validator("report_id", "subject_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        if not normalized:
            raise ValueError("validation report text fields cannot be empty")
        if text_has_sensitive_content(normalized):
            raise ValueError("validation report text fields cannot contain secrets or raw URLs")
        return normalized

    @field_validator("source_data_reference")
    @classmethod
    def source_reference_must_not_contain_secret_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        if not normalized:
            raise ValueError("source_data_reference cannot be empty")
        lowered = normalized.lower()
        if any(part in lowered for part in SECRET_TEXT_PARTS):
            raise ValueError("source_data_reference cannot contain secret-like text")
        return normalized

    @field_validator("results")
    @classmethod
    def results_cannot_be_empty(cls, value: list[ValidationResult]) -> list[ValidationResult]:
        if not value:
            raise ValueError("validation reports require at least one result")
        return value

    @field_validator("issue_count", "warning_count", "error_count", "critical_count")
    @classmethod
    def counts_must_be_non_negative(cls, value: int) -> int:
        if value < 0:
            raise ValueError("validation report counts cannot be negative")
        return value

    @field_validator("generated_at")
    @classmethod
    def generated_at_must_be_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @model_validator(mode="after")
    def counts_must_match_results(self) -> ValidationReport:
        issue_count, warning_count, error_count, critical_count = _issue_counts(self.results)
        if (
            self.issue_count,
            self.warning_count,
            self.error_count,
            self.critical_count,
        ) != (issue_count, warning_count, error_count, critical_count):
            raise ValueError("validation report counts must match result issues")
        return self


def build_validation_report(
    scope: ValidationScope,
    subject_id: str,
    results: list[ValidationResult],
    settings=None,
    source_data_reference: str | None = None,
    notes: list[str] | None = None,
) -> ValidationReport:
    schema_version = getattr(settings, "data_quality_schema_version", "v1")
    issue_count, warning_count, error_count, critical_count = _issue_counts(results)
    return ValidationReport(
        report_id=f"validation_{uuid4().hex}",
        scope=scope,
        subject_id=subject_id,
        status=_status_from_results(results),
        results=results,
        issue_count=issue_count,
        warning_count=warning_count,
        error_count=error_count,
        critical_count=critical_count,
        schema_version=schema_version,
        source_data_reference=source_data_reference,
        notes=notes or [],
    )


def summarize_report(report: ValidationReport) -> dict[str, int | str | None]:
    return {
        "report_id": report.report_id,
        "scope": report.scope.value,
        "subject_id": report.subject_id,
        "status": report.status.value,
        "issue_count": report.issue_count,
        "warning_count": report.warning_count,
        "error_count": report.error_count,
        "critical_count": report.critical_count,
        "schema_version": report.schema_version,
        "source_data_reference": report.source_data_reference,
    }
