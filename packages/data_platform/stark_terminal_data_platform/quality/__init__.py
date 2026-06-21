"""Data Quality + Validation Framework foundation."""

from stark_terminal_data_platform.quality.enums import (
    QualityGateDecision,
    ValidationRuleType,
    ValidationScope,
    ValidationSeverity,
    ValidationStatus,
)
from stark_terminal_data_platform.quality.gates import (
    QualityGatePolicy,
    QualityGateResult,
    default_quality_gate_policy,
    evaluate_quality_gate,
)
from stark_terminal_data_platform.quality.health import (
    DataQualityHealthStatus,
    check_data_quality_health,
)
from stark_terminal_data_platform.quality.issues import ValidationIssue
from stark_terminal_data_platform.quality.registry import ValidationRegistry
from stark_terminal_data_platform.quality.reports import ValidationReport
from stark_terminal_data_platform.quality.results import ValidationResult
from stark_terminal_data_platform.quality.rules import ValidationRule

__all__ = [
    "DataQualityHealthStatus",
    "QualityGateDecision",
    "QualityGatePolicy",
    "QualityGateResult",
    "ValidationIssue",
    "ValidationRegistry",
    "ValidationReport",
    "ValidationResult",
    "ValidationRule",
    "ValidationRuleType",
    "ValidationScope",
    "ValidationSeverity",
    "ValidationStatus",
    "check_data_quality_health",
    "default_quality_gate_policy",
    "evaluate_quality_gate",
]
