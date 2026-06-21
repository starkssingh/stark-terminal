from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_data_platform.quality.enums import (
    QualityGateDecision,
    ValidationScope,
    ValidationStatus,
)
from stark_terminal_data_platform.quality.issues import ValidationIssue
from stark_terminal_data_platform.quality.reports import ValidationReport


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class QualityGatePolicy(BaseModel):
    policy_id: str
    name: str
    scope: ValidationScope
    fail_on_error: bool = True
    fail_on_warning: bool = False
    require_source_reference: bool = True
    max_allowed_warnings: int | None = None
    max_allowed_errors: int = 0
    schema_version: str = "v1"

    @field_validator("policy_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("quality gate text fields cannot be empty")
        return normalized

    @field_validator("max_allowed_warnings")
    @classmethod
    def optional_warning_limit_must_be_non_negative(cls, value: int | None) -> int | None:
        if value is not None and value < 0:
            raise ValueError("max_allowed_warnings must be non-negative")
        return value

    @field_validator("max_allowed_errors")
    @classmethod
    def error_limit_must_be_non_negative(cls, value: int) -> int:
        if value < 0:
            raise ValueError("max_allowed_errors must be non-negative")
        return value


class QualityGateResult(BaseModel):
    decision: QualityGateDecision
    policy_id: str
    report_id: str
    reason: str
    evaluated_at: datetime = Field(default_factory=_utc_now)
    blocking_issues: list[ValidationIssue] = Field(default_factory=list)

    @field_validator("policy_id", "report_id", "reason")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("quality gate result text fields cannot be empty")
        return normalized

    @field_validator("evaluated_at")
    @classmethod
    def evaluated_at_must_be_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)


def _blocking_issues(report: ValidationReport) -> list[ValidationIssue]:
    return [
        issue
        for result in report.results
        for issue in result.issues
        if issue.severity in {"ERROR", "CRITICAL"}
    ]


def evaluate_quality_gate(report: ValidationReport, policy: QualityGatePolicy) -> QualityGateResult:
    blocking = _blocking_issues(report)
    if policy.require_source_reference and not report.source_data_reference:
        return QualityGateResult(
            decision=QualityGateDecision.BLOCK,
            policy_id=policy.policy_id,
            report_id=report.report_id,
            reason="source data reference is required",
            blocking_issues=blocking,
        )
    if report.status == ValidationStatus.BLOCKED:
        return QualityGateResult(
            decision=QualityGateDecision.BLOCK,
            policy_id=policy.policy_id,
            report_id=report.report_id,
            reason="validation report is blocked",
            blocking_issues=blocking,
        )
    if report.error_count > policy.max_allowed_errors:
        return QualityGateResult(
            decision=QualityGateDecision.BLOCK,
            policy_id=policy.policy_id,
            report_id=report.report_id,
            reason="error threshold exceeded",
            blocking_issues=blocking,
        )
    if policy.fail_on_error and report.status == ValidationStatus.FAIL:
        return QualityGateResult(
            decision=QualityGateDecision.BLOCK,
            policy_id=policy.policy_id,
            report_id=report.report_id,
            reason="validation errors block the gate",
            blocking_issues=blocking,
        )
    if policy.max_allowed_warnings is not None and report.warning_count > policy.max_allowed_warnings:
        return QualityGateResult(
            decision=QualityGateDecision.BLOCK,
            policy_id=policy.policy_id,
            report_id=report.report_id,
            reason="warning threshold exceeded",
            blocking_issues=blocking,
        )
    if policy.fail_on_warning and report.status == ValidationStatus.WARN:
        return QualityGateResult(
            decision=QualityGateDecision.BLOCK,
            policy_id=policy.policy_id,
            report_id=report.report_id,
            reason="validation warnings block the gate",
            blocking_issues=blocking,
        )
    if report.status == ValidationStatus.WARN:
        return QualityGateResult(
            decision=QualityGateDecision.WARN,
            policy_id=policy.policy_id,
            report_id=report.report_id,
            reason="validation warnings require review",
            blocking_issues=blocking,
        )
    return QualityGateResult(
        decision=QualityGateDecision.ALLOW,
        policy_id=policy.policy_id,
        report_id=report.report_id,
        reason="validation report passes quality gate",
        blocking_issues=blocking,
    )


def default_quality_gate_policy(
    scope: ValidationScope,
    settings: Settings | None = None,
) -> QualityGatePolicy:
    resolved = settings or get_settings()
    return QualityGatePolicy(
        policy_id=f"default_{scope.value.lower()}",
        name=f"Default {scope.value} quality gate",
        scope=scope,
        fail_on_error=resolved.data_quality_default_fail_on_error,
        fail_on_warning=resolved.data_quality_default_fail_on_warning,
        require_source_reference=resolved.data_quality_require_source_reference,
        schema_version=resolved.data_quality_schema_version,
    )
