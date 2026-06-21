import pytest
from pydantic import ValidationError

from stark_terminal_data_platform.quality.enums import (
    ValidationScope,
    ValidationSeverity,
    ValidationStatus,
)
from stark_terminal_data_platform.quality.issues import ValidationIssue
from stark_terminal_data_platform.quality.reports import build_validation_report, summarize_report
from stark_terminal_data_platform.quality.results import (
    ValidationResult,
    blocked_result,
    fail_result,
    pass_result,
)


def _error_issue() -> ValidationIssue:
    return ValidationIssue(
        code="ERR",
        severity=ValidationSeverity.ERROR,
        message="failure",
        scope=ValidationScope.INSTRUMENT,
    )


def test_pass_result_has_no_issues() -> None:
    result = pass_result(ValidationScope.INSTRUMENT, "NSE:TEST:NSE_EQUITY")

    assert result.status == ValidationStatus.PASS
    assert result.issues == []


def test_fail_and_blocked_results_include_blocking_issues() -> None:
    fail = fail_result(ValidationScope.INSTRUMENT, "subject", _error_issue())
    blocked = blocked_result(
        ValidationScope.INSTRUMENT,
        "subject",
        ValidationIssue(
            code="BLOCK",
            severity=ValidationSeverity.CRITICAL,
            message="blocked",
            scope=ValidationScope.INSTRUMENT,
        ),
    )

    assert fail.status == ValidationStatus.FAIL
    assert blocked.status == ValidationStatus.BLOCKED


def test_pass_with_issues_rejected() -> None:
    with pytest.raises(ValidationError):
        ValidationResult(
            status=ValidationStatus.PASS,
            scope=ValidationScope.INSTRUMENT,
            subject_id="subject",
            issues=[_error_issue()],
        )


def test_validation_report_counts_and_summary() -> None:
    report = build_validation_report(
        ValidationScope.INSTRUMENT,
        "subject",
        [fail_result(ValidationScope.INSTRUMENT, "subject", _error_issue())],
        source_data_reference="fixture://quality",
    )
    summary = summarize_report(report)

    assert report.status == ValidationStatus.FAIL
    assert report.issue_count == 1
    assert report.error_count == 1
    assert summary["status"] == "FAIL"
    assert report.model_dump()["source_data_reference"] == "fixture://quality"
