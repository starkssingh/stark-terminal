from __future__ import annotations

from typing import Any

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_data_platform.quality.enums import (
    ValidationScope,
    ValidationSeverity,
    ValidationStatus,
)
from stark_terminal_data_platform.quality.issues import ValidationIssue
from stark_terminal_data_platform.quality.reports import ValidationReport, build_validation_report
from stark_terminal_data_platform.quality.results import (
    ValidationResult,
    blocked_result,
    fail_result,
    pass_result,
    warn_result,
)


class BaseValidator:
    """Deterministic local validator base; no external calls or state mutation."""

    scope: ValidationScope = ValidationScope.UNKNOWN
    name: str = "base_validator"
    expected_type: type[Any] | tuple[type[Any], ...] | None = None

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    def subject_id(self, subject: object) -> str:
        return str(
            getattr(
                subject,
                "dataset_id",
                getattr(subject, "snapshot_id", getattr(subject, "request_id", subject.__class__.__name__)),
            )
        )

    def validate_subject_type(self, subject: object) -> ValidationResult | None:
        if self.expected_type is None or isinstance(subject, self.expected_type):
            return None
        return blocked_result(
            self.scope,
            subject.__class__.__name__,
            ValidationIssue(
                code="INVALID_SUBJECT_TYPE",
                severity=ValidationSeverity.CRITICAL,
                message=f"{self.name} cannot validate subject type {subject.__class__.__name__}",
                scope=self.scope,
            ),
        )

    def validate(self, subject: object) -> ValidationReport:
        type_result = self.validate_subject_type(subject)
        if type_result is not None:
            return build_validation_report(self.scope, type_result.subject_id, [type_result], self.settings)
        try:
            return self._validate(subject)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # expected validator failures become reports.
            result = fail_result(
                self.scope,
                self.subject_id(subject),
                ValidationIssue(
                    code="VALIDATOR_EXCEPTION",
                    severity=ValidationSeverity.ERROR,
                    message=str(exc) or "validator failed",
                    scope=self.scope,
                ),
            )
            return build_validation_report(self.scope, self.subject_id(subject), [result], self.settings)

    def _validate(self, subject: object) -> ValidationReport:
        raise NotImplementedError

    def _pass(self, subject: object, metadata: dict[str, object] | None = None) -> ValidationResult:
        return pass_result(self.scope, self.subject_id(subject), metadata=metadata or {})

    def _warn(
        self,
        subject: object,
        code: str,
        message: str,
        field: str | None = None,
    ) -> ValidationResult:
        return warn_result(
            self.scope,
            self.subject_id(subject),
            ValidationIssue(
                code=code,
                severity=ValidationSeverity.WARNING,
                message=message,
                field=field,
                scope=self.scope,
            ),
        )

    def _fail(
        self,
        subject: object,
        code: str,
        message: str,
        field: str | None = None,
        severity: ValidationSeverity = ValidationSeverity.ERROR,
    ) -> ValidationResult:
        status = ValidationStatus.BLOCKED if severity == ValidationSeverity.CRITICAL else ValidationStatus.FAIL
        issue = ValidationIssue(
            code=code,
            severity=severity,
            message=message,
            field=field,
            scope=self.scope,
        )
        if status == ValidationStatus.BLOCKED:
            return blocked_result(self.scope, self.subject_id(subject), issue)
        return fail_result(self.scope, self.subject_id(subject), issue)

    def _report(
        self,
        subject: object,
        results: list[ValidationResult],
        source_data_reference: str | None = None,
    ) -> ValidationReport:
        if not results:
            results = [self._pass(subject)]
        return build_validation_report(
            self.scope,
            self.subject_id(subject),
            results,
            self.settings,
            source_data_reference=source_data_reference,
        )
