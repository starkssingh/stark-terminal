from copy import deepcopy

from stark_terminal_data_platform.quality.enums import ValidationScope, ValidationStatus
from stark_terminal_data_platform.quality.reports import build_validation_report
from stark_terminal_data_platform.quality.results import pass_result
from stark_terminal_data_platform.quality.validators import BaseValidator


class DictValidator(BaseValidator):
    scope = ValidationScope.UNKNOWN
    name = "dict_validator"
    expected_type = dict

    def _validate(self, subject: object):
        return build_validation_report(
            self.scope,
            "dict",
            [pass_result(self.scope, "dict")],
            self.settings,
        )


def test_base_validator_subclass_returns_report() -> None:
    report = DictValidator().validate({"ok": True})

    assert report.status == ValidationStatus.PASS


def test_invalid_subject_type_returns_blocked_report() -> None:
    report = DictValidator().validate(["not", "dict"])

    assert report.status == ValidationStatus.BLOCKED
    assert report.critical_count == 1


def test_validator_does_not_mutate_subject() -> None:
    subject = {"ok": True}
    original = deepcopy(subject)

    DictValidator().validate(subject)

    assert subject == original
