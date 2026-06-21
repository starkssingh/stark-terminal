from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel, Field, field_validator

from stark_terminal_core.serialization.json import to_jsonable
from stark_terminal_data_platform.quality.enums import (
    ValidationRuleType,
    ValidationScope,
    ValidationSeverity,
)
from stark_terminal_data_platform.quality.issues import text_has_sensitive_content


class ValidationRule(BaseModel):
    rule_id: str
    name: str
    rule_type: ValidationRuleType
    scope: ValidationScope
    severity: ValidationSeverity = ValidationSeverity.ERROR
    description: str
    enabled: bool = True
    parameters: dict[str, object] = Field(default_factory=dict)
    schema_version: str = "v1"

    @field_validator("rule_id", "name", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("validation rule text fields cannot be empty")
        if text_has_sensitive_content(normalized):
            raise ValueError("validation rule text cannot contain secrets or raw URLs")
        return normalized

    @field_validator("parameters")
    @classmethod
    def parameters_must_be_jsonable_and_safe(cls, value: dict[str, Any]) -> dict[str, object]:
        for key in value:
            if text_has_sensitive_content(str(key)):
                raise ValueError("validation rule parameters cannot contain secret-like keys")
        jsonable = to_jsonable(value)
        for key in jsonable:
            if text_has_sensitive_content(str(key)):
                raise ValueError("validation rule parameters cannot contain secret-like keys")
        try:
            json.dumps(jsonable, sort_keys=True)
        except (TypeError, ValueError) as exc:
            raise ValueError("validation rule parameters must be JSON-serializable") from exc
        return jsonable


def create_required_field_rule(
    rule_id: str,
    name: str,
    scope: ValidationScope,
    field: str,
    severity: ValidationSeverity = ValidationSeverity.ERROR,
) -> ValidationRule:
    return ValidationRule(
        rule_id=rule_id,
        name=name,
        rule_type=ValidationRuleType.REQUIRED_FIELD,
        scope=scope,
        severity=severity,
        description=f"Require field {field}.",
        parameters={"field": field},
    )


def create_range_rule(
    rule_id: str,
    name: str,
    scope: ValidationScope,
    field: str,
    min_value: float | None = None,
    max_value: float | None = None,
    severity: ValidationSeverity = ValidationSeverity.ERROR,
) -> ValidationRule:
    return ValidationRule(
        rule_id=rule_id,
        name=name,
        rule_type=ValidationRuleType.RANGE_CHECK,
        scope=scope,
        severity=severity,
        description=f"Check numeric range for {field}.",
        parameters={"field": field, "min_value": min_value, "max_value": max_value},
    )


def create_source_reference_rule(
    rule_id: str,
    name: str,
    scope: ValidationScope,
    severity: ValidationSeverity = ValidationSeverity.ERROR,
) -> ValidationRule:
    return ValidationRule(
        rule_id=rule_id,
        name=name,
        rule_type=ValidationRuleType.SOURCE_REFERENCE_CHECK,
        scope=scope,
        severity=severity,
        description="Require source data reference.",
        parameters={"field": "source_data_reference"},
    )
