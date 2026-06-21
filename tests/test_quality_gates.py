from stark_terminal_core.config.settings import Settings
from stark_terminal_data_platform.quality.enums import (
    QualityGateDecision,
    ValidationScope,
    ValidationSeverity,
)
from stark_terminal_data_platform.quality.gates import (
    QualityGatePolicy,
    default_quality_gate_policy,
    evaluate_quality_gate,
)
from stark_terminal_data_platform.quality.issues import ValidationIssue
from stark_terminal_data_platform.quality.reports import build_validation_report
from stark_terminal_data_platform.quality.results import fail_result, pass_result, warn_result


def test_default_policy_uses_settings() -> None:
    policy = default_quality_gate_policy(
        ValidationScope.DATASET_MANIFEST,
        Settings(data_quality_default_fail_on_warning=True),
    )

    assert policy.fail_on_warning is True
    assert policy.require_source_reference is True


def test_pass_report_allows_with_source_reference() -> None:
    report = build_validation_report(
        ValidationScope.DATASET_MANIFEST,
        "dataset",
        [pass_result(ValidationScope.DATASET_MANIFEST, "dataset")],
        source_data_reference="fixture://dataset",
    )

    result = evaluate_quality_gate(report, default_quality_gate_policy(ValidationScope.DATASET_MANIFEST))

    assert result.decision == QualityGateDecision.ALLOW


def test_warn_report_warns_or_blocks_based_on_policy() -> None:
    issue = ValidationIssue(
        code="WARN",
        severity=ValidationSeverity.WARNING,
        message="warning",
        scope=ValidationScope.DATASET_MANIFEST,
    )
    report = build_validation_report(
        ValidationScope.DATASET_MANIFEST,
        "dataset",
        [warn_result(ValidationScope.DATASET_MANIFEST, "dataset", issue)],
        source_data_reference="fixture://dataset",
    )

    assert evaluate_quality_gate(report, QualityGatePolicy(policy_id="p1", name="p1", scope=ValidationScope.DATASET_MANIFEST)).decision == QualityGateDecision.WARN
    assert evaluate_quality_gate(report, QualityGatePolicy(policy_id="p2", name="p2", scope=ValidationScope.DATASET_MANIFEST, fail_on_warning=True)).decision == QualityGateDecision.BLOCK


def test_fail_report_blocks_and_missing_source_reference_blocks() -> None:
    error = ValidationIssue(
        code="ERR",
        severity=ValidationSeverity.ERROR,
        message="error",
        scope=ValidationScope.DATASET_MANIFEST,
    )
    fail_report = build_validation_report(
        ValidationScope.DATASET_MANIFEST,
        "dataset",
        [fail_result(ValidationScope.DATASET_MANIFEST, "dataset", error)],
        source_data_reference="fixture://dataset",
    )
    no_source_report = build_validation_report(
        ValidationScope.DATASET_MANIFEST,
        "dataset",
        [pass_result(ValidationScope.DATASET_MANIFEST, "dataset")],
    )

    policy = default_quality_gate_policy(ValidationScope.DATASET_MANIFEST)

    assert evaluate_quality_gate(fail_report, policy).decision == QualityGateDecision.BLOCK
    assert evaluate_quality_gate(no_source_report, policy).decision == QualityGateDecision.BLOCK


def test_warning_threshold_blocks_when_exceeded() -> None:
    issue = ValidationIssue(
        code="WARN",
        severity=ValidationSeverity.WARNING,
        message="warning",
        scope=ValidationScope.DATASET_MANIFEST,
    )
    report = build_validation_report(
        ValidationScope.DATASET_MANIFEST,
        "dataset",
        [warn_result(ValidationScope.DATASET_MANIFEST, "dataset", issue)],
        source_data_reference="fixture://dataset",
    )

    gate = evaluate_quality_gate(
        report,
        QualityGatePolicy(
            policy_id="p",
            name="p",
            scope=ValidationScope.DATASET_MANIFEST,
            max_allowed_warnings=0,
        ),
    )

    assert gate.decision == QualityGateDecision.BLOCK
