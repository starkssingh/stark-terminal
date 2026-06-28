import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_decision_console.demo_state import DEMO_CREATED_AT, retail_decision_console_demo_state
from stark_terminal_core.retail_decision_console.layout import (
    VISUAL_LAYOUT_STAGE,
    RetailDecisionConsoleLayoutDescriptor,
    RetailDecisionConsoleLayoutSection,
    RetailDecisionConsoleLayoutZone,
    retail_decision_console_default_layout,
)
from stark_terminal_core.retail_decision_console.state_view_model import (
    map_demo_state_to_shell_descriptor,
    retail_decision_console_state_view_model,
)
from stark_terminal_core.retail_decision_console.static_state import RetailDecisionConsoleStaticState


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

FORBIDDEN_ACTIVE_LABELS = {
    "Buy",
    "Sell",
    "Execute",
    "Place Order",
    "Broker",
    "Connect Broker",
    "Trade Now",
    "Auto Trade",
    "Approve Trade",
    "Override",
    "Live Signal",
    "Strong Buy",
    "Strong Sell",
    "Ready to Trade",
    "Confidence 70%",
    "Confidence",
    "Probability",
    "Recommended",
}


def test_retail_decision_console_layout_descriptor_validates() -> None:
    layout = retail_decision_console_default_layout(DEMO_CREATED_AT)

    assert layout.stage == VISUAL_LAYOUT_STAGE
    assert layout.demo_only is True
    assert layout.unavailable is True
    assert layout.read_only is True
    assert set(layout.zones) == set(RetailDecisionConsoleLayoutZone)
    assert layout.sections
    assert {section.section_id for section in layout.sections} >= {
        "header-status-banner",
        "instrument-selector",
        "timeframe-selector",
        "market-session",
        "refresh-placeholder",
        "decision-summary",
        "regime-state",
        "evidence-panel",
        "risk-invalidation",
        "options-context",
        "research-context",
        "journal",
        "settings",
    }
    for flag in DANGEROUS_FLAGS:
        assert getattr(layout, flag) is False
    for section in layout.sections:
        assert section.demo_only is True
        assert section.unavailable is True
        assert section.safety_label
        for flag in DANGEROUS_FLAGS:
            assert getattr(section, flag) is False


def test_retail_decision_console_layout_rejects_unsafe_values() -> None:
    layout = retail_decision_console_default_layout(DEMO_CREATED_AT)
    section = layout.sections[0]

    with pytest.raises(ValidationError):
        RetailDecisionConsoleLayoutSection(
            section_id="bad-section",
            title="Bad",
            subtitle="Bad",
            zone=RetailDecisionConsoleLayoutZone.PRIMARY,
            placeholder_text="Bad",
            demo_only=False,
        )
    with pytest.raises(ValidationError):
        RetailDecisionConsoleLayoutDescriptor(
            sections=[section],
            zones=[RetailDecisionConsoleLayoutZone.HEADER],
            live_data_enabled=True,
        )


def test_shell_view_model_exposes_layout_zones_and_preserves_safety_flags() -> None:
    view_model = retail_decision_console_state_view_model()

    assert view_model.layout.stage == VISUAL_LAYOUT_STAGE
    assert view_model.layout.safety_banner.startswith("Demo/static preview only")
    assert view_model.demo_only is True
    assert view_model.unavailable is True
    assert view_model.sections
    assert {section.layout_zone for section in view_model.sections} == set(RetailDecisionConsoleLayoutZone)
    assert [section.layout_priority for section in view_model.sections] == sorted(
        section.layout_priority for section in view_model.sections
    )
    for flag in DANGEROUS_FLAGS:
        assert getattr(view_model, flag) is False
        assert view_model.safety_flags[flag] is False
    for section in view_model.sections:
        assert section.demo_only is True
        assert section.unavailable is True
        assert "demo" in section.layout_safety_label.lower()
        assert "unavailable" in section.layout_safety_label.lower()
        for flag in DANGEROUS_FLAGS:
            assert getattr(section, flag) is False


def test_static_state_maps_to_visual_layout_without_active_decision_labels() -> None:
    view_model = map_demo_state_to_shell_descriptor()
    dump_text = str(view_model.model_dump(mode="json"))

    assert view_model.layout.demo_only is True
    assert view_model.layout.unavailable is True
    assert view_model.layout.sections
    assert not FORBIDDEN_ACTIVE_LABELS.intersection(view_model.active_control_labels)
    for section in view_model.sections:
        assert section.title not in FORBIDDEN_ACTIVE_LABELS
        assert not FORBIDDEN_ACTIVE_LABELS.intersection(section.active_control_labels)
        for card in section.cards:
            assert card.title not in FORBIDDEN_ACTIVE_LABELS
            assert not FORBIDDEN_ACTIVE_LABELS.intersection(card.active_control_labels)
    assert "live_data_enabled': True" not in dump_text
    assert "recommendations_enabled': True" not in dump_text
    assert "confidence_scoring_enabled': True" not in dump_text
    assert "execution_enabled': True" not in dump_text


def test_visual_layout_rejects_unsafe_static_state_mapping() -> None:
    state = retail_decision_console_demo_state()

    with pytest.raises(ValidationError):
        RetailDecisionConsoleStaticState(
            state_id="bad-state",
            provenance=state.provenance,
            sections=state.sections,
            live_data_enabled=True,
        )
