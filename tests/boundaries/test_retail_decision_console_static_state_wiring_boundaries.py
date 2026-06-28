import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_decision_console.demo_state import (
    retail_decision_console_demo_state,
)
from stark_terminal_core.retail_decision_console.state_view_model import (
    STATIC_STATE_SAFETY_BANNER,
    RetailDecisionConsoleCardViewModel,
    RetailDecisionConsoleShellViewModel,
    RetailDecisionConsoleSectionViewModel,
    map_demo_cards_to_ui_cards,
    map_demo_sections_to_ui_sections,
    map_demo_state_to_shell_descriptor,
    retail_decision_console_state_view_model,
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


def test_demo_static_state_maps_to_shell_view_model() -> None:
    state = retail_decision_console_demo_state()
    view_model = retail_decision_console_state_view_model()
    mapped = map_demo_state_to_shell_descriptor(state)

    assert mapped == view_model
    assert view_model.view_model_id == "retail-decision-console-static-state-view-model-v1"
    assert view_model.stage == "static_state_wired_shell"
    assert view_model.static_state_wiring_only is True
    assert view_model.demo_only is True
    assert view_model.unavailable is True
    assert view_model.read_only is True
    assert view_model.safety_banner == STATIC_STATE_SAFETY_BANNER
    assert "demo" in view_model.provenance_demo_label.lower()
    assert "static" in view_model.provenance_demo_label.lower()
    assert "unavailable" in view_model.provenance_demo_label.lower()
    assert len(view_model.sections) == len(state.sections)
    for flag in DANGEROUS_FLAGS:
        assert getattr(view_model, flag) is False
        assert view_model.safety_flags[flag] is False


def test_demo_sections_and_cards_map_to_ui_sections_and_cards() -> None:
    state = retail_decision_console_demo_state()
    sections = map_demo_sections_to_ui_sections(state.sections, state.provenance)
    cards = map_demo_cards_to_ui_cards(state.sections[0].cards, state.provenance)

    assert sections
    assert cards
    assert {section.section_id for section in sections} == {section.section_id for section in state.sections}
    for section in sections:
        assert section.demo_only is True
        assert section.unavailable is True
        assert "demo" in section.unavailable_demo_label.lower()
        assert "unavailable" in section.unavailable_demo_label.lower()
        assert "demo" in section.provenance_demo_label.lower()
        assert section.cards
        for flag in DANGEROUS_FLAGS:
            assert getattr(section, flag) is False
            assert section.safety_flags[flag] is False
        for card in section.cards:
            assert card.demo_only is True
            assert card.unavailable is True
            assert "demo" in card.unavailable_demo_label.lower()
            assert "unavailable" in card.unavailable_demo_label.lower()
            for flag in DANGEROUS_FLAGS:
                assert getattr(card, flag) is False
                assert card.safety_flags[flag] is False


def test_view_model_rejects_unsafe_values() -> None:
    state = retail_decision_console_demo_state()
    section = map_demo_sections_to_ui_sections(state.sections, state.provenance)[0]
    card = section.cards[0]

    with pytest.raises(ValidationError):
        RetailDecisionConsoleCardViewModel(
            card_id="bad-card",
            title="Bad",
            placeholder_text="Bad",
            provenance_demo_label="demo static unavailable",
            recommendations_enabled=True,
            created_at=card.created_at,
        )
    with pytest.raises(ValidationError):
        RetailDecisionConsoleSectionViewModel(
            section_id="bad-section",
            title="Bad",
            placeholder_text="Bad",
            provenance_demo_label="demo static unavailable",
            cards=[card],
            active_control_labels=["Buy"],
            created_at=section.created_at,
        )
    with pytest.raises(ValidationError):
        RetailDecisionConsoleShellViewModel(
            view_model_id="bad-shell",
            shell_id="bad-shell",
            provenance_demo_label="demo static unavailable",
            sections=[section],
            execution_enabled=True,
            created_at=state.created_at,
        )
    with pytest.raises(ValueError):
        map_demo_state_to_shell_descriptor(state.model_copy(update={"live_data_enabled": True}))


def test_view_model_has_no_forbidden_active_decision_labels_or_controls() -> None:
    view_model = retail_decision_console_state_view_model()

    assert not FORBIDDEN_ACTIVE_LABELS.intersection(view_model.active_control_labels)
    assert not FORBIDDEN_ACTIVE_LABELS.intersection({view_model.safety_banner})
    for section in view_model.sections:
        assert not FORBIDDEN_ACTIVE_LABELS.intersection(section.active_control_labels)
        assert section.title not in FORBIDDEN_ACTIVE_LABELS
        for card in section.cards:
            assert not FORBIDDEN_ACTIVE_LABELS.intersection(card.active_control_labels)
            assert card.title not in FORBIDDEN_ACTIVE_LABELS
