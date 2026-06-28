import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_decision_console.ui_descriptors import (
    FORBIDDEN_ACTIVE_CONTROL_LABELS,
    SAFETY_BANNER,
    SHELL_TITLE,
    RetailDecisionConsolePlaceholderState,
    RetailDecisionConsoleSectionDescriptor,
    RetailDecisionConsoleShellDescriptor,
    retail_decision_console_section_descriptors,
    retail_decision_console_ui_forbidden_labels,
    retail_decision_console_ui_shell_descriptor,
)
from stark_terminal_core.retail_decision_console.ui_shell import (
    assert_no_retail_console_broker_controls,
    assert_no_retail_console_confidence_scoring,
    assert_no_retail_console_decision_object_generation,
    assert_no_retail_console_execution,
    assert_no_retail_console_live_decisions,
    assert_no_retail_console_order_buttons,
    assert_no_retail_console_recommendations,
    assert_retail_decision_console_ui_shell_is_safe,
)


DANGEROUS_FLAGS = [
    "live_data_enabled",
    "recommendations_enabled",
    "action_generation_enabled",
    "confidence_scoring_enabled",
    "decision_object_generation_enabled",
    "broker_controls_enabled",
    "order_buttons_enabled",
    "execution_enabled",
]


def test_retail_decision_console_shell_descriptor_validates() -> None:
    shell = retail_decision_console_ui_shell_descriptor()

    assert shell.shell_id == "retail-decision-console-ui-shell-skeleton-v1"
    assert shell.title == SHELL_TITLE
    assert shell.stage == "ui_shell_skeleton"
    assert shell.safety_banner == SAFETY_BANNER
    assert shell.skeleton_only is True
    assert shell.unavailable_by_default is True
    assert shell.sections
    for flag in DANGEROUS_FLAGS:
        assert getattr(shell, flag) is False
    assert shell.active_control_labels == []
    assert_retail_decision_console_ui_shell_is_safe(shell)


def test_retail_decision_console_section_descriptors_validate() -> None:
    sections = retail_decision_console_section_descriptors()
    section_titles = {section.title for section in sections}

    assert "Header/status banner" in section_titles
    assert "Instrument selector placeholder" in section_titles
    assert "Timeframe selector placeholder" in section_titles
    assert "Market/session placeholder" in section_titles
    assert "Disabled refresh placeholder" in section_titles
    assert "Decision summary placeholder" in section_titles
    assert "Regime/state placeholder" in section_titles
    assert "Evidence panel placeholder" in section_titles
    assert "Risk/invalidation placeholder" in section_titles
    assert "Options context placeholder" in section_titles
    assert "Research context placeholder" in section_titles
    assert "Journal placeholder" in section_titles
    assert "Settings placeholder" in section_titles
    for section in sections:
        assert section.skeleton_only is True
        assert section.active_control_labels == []
        assert section.placeholder_state.unavailable is True
        assert section.placeholder_state.skeleton_only is True
        assert section.placeholder_state.demo_only is True
        for flag in DANGEROUS_FLAGS:
            assert getattr(section, flag) is False
            assert getattr(section.placeholder_state, flag) is False


def test_retail_decision_console_forbidden_active_labels_are_not_controls() -> None:
    shell = retail_decision_console_ui_shell_descriptor()
    forbidden = set(retail_decision_console_ui_forbidden_labels())

    assert forbidden == set(FORBIDDEN_ACTIVE_CONTROL_LABELS)
    assert not forbidden.intersection(shell.active_control_labels)
    assert not forbidden.intersection(shell.safe_control_labels)
    for section in shell.sections:
        assert not forbidden.intersection(section.active_control_labels)


def test_retail_decision_console_descriptor_rejects_unsafe_values() -> None:
    shell = retail_decision_console_ui_shell_descriptor()
    placeholder = RetailDecisionConsolePlaceholderState(state_id="test-unavailable-state")

    with pytest.raises(ValidationError):
        RetailDecisionConsoleShellDescriptor(shell_id="bad", title="", sections=shell.sections)
    with pytest.raises(ValidationError):
        RetailDecisionConsoleShellDescriptor(shell_id="bad", sections=[])
    with pytest.raises(ValidationError):
        RetailDecisionConsoleShellDescriptor(shell_id="bad", live_data_enabled=True, sections=shell.sections)
    with pytest.raises(ValidationError):
        RetailDecisionConsoleSectionDescriptor(
            section_id="unsafe-section",
            title="Unsafe",
            description="Unsafe active control",
            placeholder_state=placeholder,
            active_control_labels=["Buy"],
        )
    with pytest.raises(ValidationError):
        RetailDecisionConsolePlaceholderState(state_id="unsafe-state", execution_enabled=True)


def test_retail_decision_console_boundary_helpers_reject_mutated_dangerous_flags() -> None:
    shell = retail_decision_console_ui_shell_descriptor()

    with pytest.raises(ValueError):
        assert_no_retail_console_live_decisions(shell.model_copy(update={"live_data_enabled": True}))
    with pytest.raises(ValueError):
        assert_no_retail_console_recommendations(shell.model_copy(update={"recommendations_enabled": True}))
    with pytest.raises(ValueError):
        assert_no_retail_console_confidence_scoring(shell.model_copy(update={"confidence_scoring_enabled": True}))
    with pytest.raises(ValueError):
        assert_no_retail_console_decision_object_generation(
            shell.model_copy(update={"decision_object_generation_enabled": True})
        )
    with pytest.raises(ValueError):
        assert_no_retail_console_broker_controls(shell.model_copy(update={"broker_controls_enabled": True}))
    with pytest.raises(ValueError):
        assert_no_retail_console_order_buttons(shell.model_copy(update={"order_buttons_enabled": True}))
    with pytest.raises(ValueError):
        assert_no_retail_console_execution(shell.model_copy(update={"execution_enabled": True}))
