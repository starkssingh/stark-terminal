from __future__ import annotations

from stark_terminal_core.retail_decision_console.ui_descriptors import (
    RetailDecisionConsoleShellDescriptor,
    retail_decision_console_ui_shell_descriptor,
)


def _descriptor_or_default(
    descriptor: RetailDecisionConsoleShellDescriptor | None,
) -> RetailDecisionConsoleShellDescriptor:
    return descriptor or retail_decision_console_ui_shell_descriptor()


def assert_no_retail_console_live_decisions(
    descriptor: RetailDecisionConsoleShellDescriptor | None = None,
) -> None:
    shell = _descriptor_or_default(descriptor)
    if shell.live_data_enabled:
        raise ValueError("Retail Decision Console UI shell cannot enable live data or live decisions")


def assert_no_retail_console_recommendations(
    descriptor: RetailDecisionConsoleShellDescriptor | None = None,
) -> None:
    shell = _descriptor_or_default(descriptor)
    if shell.recommendations_enabled or any(section.recommendations_enabled for section in shell.sections):
        raise ValueError("Retail Decision Console UI shell cannot enable recommendations")


def assert_no_retail_console_confidence_scoring(
    descriptor: RetailDecisionConsoleShellDescriptor | None = None,
) -> None:
    shell = _descriptor_or_default(descriptor)
    if shell.confidence_scoring_enabled or any(section.confidence_scoring_enabled for section in shell.sections):
        raise ValueError("Retail Decision Console UI shell cannot enable confidence scoring")


def assert_no_retail_console_decision_object_generation(
    descriptor: RetailDecisionConsoleShellDescriptor | None = None,
) -> None:
    shell = _descriptor_or_default(descriptor)
    if shell.decision_object_generation_enabled or any(
        section.decision_object_generation_enabled for section in shell.sections
    ):
        raise ValueError("Retail Decision Console UI shell cannot enable active DecisionObject generation")


def assert_no_retail_console_broker_controls(
    descriptor: RetailDecisionConsoleShellDescriptor | None = None,
) -> None:
    shell = _descriptor_or_default(descriptor)
    if shell.broker_controls_enabled or any(section.broker_controls_enabled for section in shell.sections):
        raise ValueError("Retail Decision Console UI shell cannot enable broker controls")


def assert_no_retail_console_order_buttons(
    descriptor: RetailDecisionConsoleShellDescriptor | None = None,
) -> None:
    shell = _descriptor_or_default(descriptor)
    if shell.order_buttons_enabled or any(section.order_buttons_enabled for section in shell.sections):
        raise ValueError("Retail Decision Console UI shell cannot enable order buttons")


def assert_no_retail_console_execution(
    descriptor: RetailDecisionConsoleShellDescriptor | None = None,
) -> None:
    shell = _descriptor_or_default(descriptor)
    if shell.execution_enabled or any(section.execution_enabled for section in shell.sections):
        raise ValueError("Retail Decision Console UI shell cannot enable execution")


def assert_retail_decision_console_ui_shell_is_safe(
    descriptor: RetailDecisionConsoleShellDescriptor | None = None,
) -> None:
    shell = _descriptor_or_default(descriptor)
    assert_no_retail_console_live_decisions(shell)
    assert_no_retail_console_recommendations(shell)
    assert_no_retail_console_confidence_scoring(shell)
    assert_no_retail_console_decision_object_generation(shell)
    assert_no_retail_console_broker_controls(shell)
    assert_no_retail_console_order_buttons(shell)
    assert_no_retail_console_execution(shell)
