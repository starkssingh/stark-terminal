import pytest

from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.quality.builtins import InstrumentValidator
from stark_terminal_data_platform.quality.enums import ValidationScope, ValidationStatus
from stark_terminal_data_platform.quality.registry import (
    ValidationRegistry,
    create_default_validation_registry,
)


def test_validation_registry_register_get_list_validate() -> None:
    registry = ValidationRegistry()
    validator = InstrumentValidator()

    registry.register(validator)

    assert registry.get(ValidationScope.INSTRUMENT) is validator
    assert registry.list_scopes() == ["INSTRUMENT"]
    assert registry.validate(create_sample_instruments()[0]).status == ValidationStatus.PASS


def test_duplicate_scope_rejected_unless_replace() -> None:
    registry = ValidationRegistry()
    registry.register(InstrumentValidator())

    with pytest.raises(ValueError):
        registry.register(InstrumentValidator())

    registry.register(InstrumentValidator(), replace=True)

    assert len(registry.list_validators()) == 1


def test_unregister_clear_and_unknown_subject_behaviors() -> None:
    registry = ValidationRegistry()
    registry.register(InstrumentValidator())
    registry.unregister(ValidationScope.INSTRUMENT)

    assert registry.get(ValidationScope.INSTRUMENT) is None
    assert registry.validate({"unknown": True}).status == ValidationStatus.BLOCKED

    registry.register(InstrumentValidator())
    registry.clear()

    assert registry.list_scopes() == []


def test_default_registry_has_builtin_validators_and_no_shared_state() -> None:
    first = create_default_validation_registry()
    second = create_default_validation_registry()
    first.clear()

    assert first.list_scopes() == []
    assert len(second.list_scopes()) == 10
