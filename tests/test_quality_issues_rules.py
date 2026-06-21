import pytest
from pydantic import ValidationError

from stark_terminal_data_platform.quality.enums import (
    ValidationRuleType,
    ValidationScope,
    ValidationSeverity,
)
from stark_terminal_data_platform.quality.issues import ValidationIssue
from stark_terminal_data_platform.quality.rules import (
    ValidationRule,
    create_range_rule,
    create_required_field_rule,
    create_source_reference_rule,
)


def test_validation_issue_valid_and_sanitizes_preview() -> None:
    issue = ValidationIssue(
        code="TEST_WARNING",
        severity=ValidationSeverity.WARNING,
        message="review value",
        scope=ValidationScope.MARKET_DATA_BAR,
        value_preview="http://secret.example/token",
    )

    assert issue.value_preview == "[redacted]"


def test_validation_issue_rejects_empty_code_and_message() -> None:
    with pytest.raises(ValidationError):
        ValidationIssue(code="", severity=ValidationSeverity.ERROR, message="x")
    with pytest.raises(ValidationError):
        ValidationIssue(code="X", severity=ValidationSeverity.ERROR, message="")


def test_validation_rule_validates_jsonable_safe_parameters() -> None:
    rule = ValidationRule(
        rule_id="rule_1",
        name="Required source",
        rule_type=ValidationRuleType.SOURCE_REFERENCE_CHECK,
        scope=ValidationScope.DATASET_MANIFEST,
        description="Require source reference.",
        parameters={"field": "source_data_reference"},
    )

    assert rule.schema_version == "v1"


def test_validation_rule_rejects_empty_fields_and_secret_parameters() -> None:
    with pytest.raises(ValidationError):
        ValidationRule(
            rule_id=" ",
            name="x",
            rule_type=ValidationRuleType.CUSTOM,
            scope=ValidationScope.UNKNOWN,
            description="x",
        )
    with pytest.raises(ValidationError):
        ValidationRule(
            rule_id="rule_2",
            name="x",
            rule_type=ValidationRuleType.CUSTOM,
            scope=ValidationScope.UNKNOWN,
            description="x",
            parameters={"api_key": "secret"},
        )


def test_rule_helpers_create_expected_rule_types() -> None:
    required = create_required_field_rule("r1", "Require field", ValidationScope.INSTRUMENT, "display_name")
    range_rule = create_range_rule("r2", "Positive price", ValidationScope.MARKET_DATA_BAR, "close", 0)
    source = create_source_reference_rule("r3", "Require source", ValidationScope.DATASET_MANIFEST)

    assert required.rule_type == ValidationRuleType.REQUIRED_FIELD
    assert range_rule.rule_type == ValidationRuleType.RANGE_CHECK
    assert source.rule_type == ValidationRuleType.SOURCE_REFERENCE_CHECK
