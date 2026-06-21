from __future__ import annotations

from typing import Any

from stark_terminal_data_platform.quality.enums import ValidationScope, ValidationSeverity
from stark_terminal_data_platform.quality.issues import ValidationIssue
from stark_terminal_data_platform.quality.reports import ValidationReport, build_validation_report
from stark_terminal_data_platform.quality.results import blocked_result
from stark_terminal_data_platform.quality.validators import BaseValidator


class ValidationRegistry:
    def __init__(self) -> None:
        self._validators: dict[ValidationScope, BaseValidator] = {}

    def register(self, validator: BaseValidator, replace: bool = False) -> None:
        if validator.scope == ValidationScope.UNKNOWN:
            raise ValueError("cannot register validator with UNKNOWN scope")
        if validator.scope in self._validators and not replace:
            raise ValueError(f"validator already registered for scope {validator.scope.value}")
        self._validators[validator.scope] = validator

    def unregister(self, scope: ValidationScope | str) -> None:
        self._validators.pop(ValidationScope(scope), None)

    def get(self, scope: ValidationScope | str) -> BaseValidator | None:
        return self._validators.get(ValidationScope(scope))

    def list_scopes(self) -> list[str]:
        return [scope.value for scope in self._validators]

    def list_validators(self) -> list[BaseValidator]:
        return list(self._validators.values())

    def clear(self) -> None:
        self._validators.clear()

    def _infer_scope(self, subject: object) -> ValidationScope:
        for scope, validator in self._validators.items():
            expected_type = validator.expected_type
            if expected_type is not None and isinstance(subject, expected_type):
                return scope
        return ValidationScope.UNKNOWN

    def validate(self, subject: object, scope: ValidationScope | str | None = None) -> ValidationReport:
        resolved_scope = ValidationScope(scope) if scope is not None else self._infer_scope(subject)
        validator = self._validators.get(resolved_scope)
        if validator is None:
            result = blocked_result(
                resolved_scope,
                subject.__class__.__name__,
                ValidationIssue(
                    code="VALIDATOR_NOT_REGISTERED",
                    severity=ValidationSeverity.CRITICAL,
                    message="no validator registered for subject",
                    scope=resolved_scope,
                ),
            )
            return build_validation_report(resolved_scope, result.subject_id, [result])
        return validator.validate(subject)


def create_default_validation_registry(settings: Any | None = None) -> ValidationRegistry:
    from stark_terminal_data_platform.quality.builtins import create_builtin_validators

    registry = ValidationRegistry()
    for validator in create_builtin_validators(settings=settings):
        registry.register(validator)
    return registry
