from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.serialization.json import to_jsonable
from stark_terminal_data_platform.quality.enums import (
    ValidationScope,
    ValidationSeverity,
    ValidationStatus,
)
from stark_terminal_data_platform.quality.issues import ValidationIssue, text_has_sensitive_content


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def ensure_quality_jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        for key in value:
            if text_has_sensitive_content(str(key)):
                raise ValueError("validation metadata cannot contain secret-like keys")
    jsonable = to_jsonable(value)
    try:
        json.dumps(jsonable, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise ValueError("validation metadata must be JSON-serializable") from exc
    return jsonable


class ValidationResult(BaseModel):
    status: ValidationStatus
    scope: ValidationScope
    subject_id: str
    rule_id: str | None = None
    issues: list[ValidationIssue] = Field(default_factory=list)
    checked_at: datetime = Field(default_factory=utc_now)
    metadata: dict[str, object] = Field(default_factory=dict)

    @field_validator("subject_id", "rule_id")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        if not normalized:
            raise ValueError("validation result text fields cannot be empty")
        if text_has_sensitive_content(normalized):
            raise ValueError("validation result text fields cannot contain secrets or raw URLs")
        return normalized

    @field_validator("checked_at")
    @classmethod
    def checked_at_must_be_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @field_validator("metadata")
    @classmethod
    def metadata_must_be_jsonable(cls, value: dict[str, Any]) -> dict[str, object]:
        return ensure_quality_jsonable(value)

    @model_validator(mode="after")
    def status_and_issues_must_be_consistent(self) -> ValidationResult:
        if self.status == ValidationStatus.PASS and self.issues:
            raise ValueError("PASS validation results cannot contain issues")
        if self.status in {ValidationStatus.FAIL, ValidationStatus.BLOCKED}:
            severities = {issue.severity for issue in self.issues}
            if not severities.intersection({ValidationSeverity.ERROR, ValidationSeverity.CRITICAL}):
                raise ValueError("FAIL/BLOCKED validation results require ERROR or CRITICAL issues")
        return self


def pass_result(
    scope: ValidationScope,
    subject_id: str,
    rule_id: str | None = None,
    metadata: dict[str, object] | None = None,
) -> ValidationResult:
    return ValidationResult(
        status=ValidationStatus.PASS,
        scope=scope,
        subject_id=subject_id,
        rule_id=rule_id,
        metadata=metadata or {},
    )


def warn_result(
    scope: ValidationScope,
    subject_id: str,
    issue: ValidationIssue,
    rule_id: str | None = None,
    metadata: dict[str, object] | None = None,
) -> ValidationResult:
    return ValidationResult(
        status=ValidationStatus.WARN,
        scope=scope,
        subject_id=subject_id,
        rule_id=rule_id,
        issues=[issue],
        metadata=metadata or {},
    )


def fail_result(
    scope: ValidationScope,
    subject_id: str,
    issue: ValidationIssue,
    rule_id: str | None = None,
    metadata: dict[str, object] | None = None,
) -> ValidationResult:
    return ValidationResult(
        status=ValidationStatus.FAIL,
        scope=scope,
        subject_id=subject_id,
        rule_id=rule_id,
        issues=[issue],
        metadata=metadata or {},
    )


def blocked_result(
    scope: ValidationScope,
    subject_id: str,
    issue: ValidationIssue,
    rule_id: str | None = None,
    metadata: dict[str, object] | None = None,
) -> ValidationResult:
    return ValidationResult(
        status=ValidationStatus.BLOCKED,
        scope=scope,
        subject_id=subject_id,
        rule_id=rule_id,
        issues=[issue],
        metadata=metadata or {},
    )
