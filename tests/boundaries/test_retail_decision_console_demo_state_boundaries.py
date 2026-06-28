import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_decision_console.demo_state import (
    DEMO_CREATED_AT,
    retail_decision_console_demo_cards,
    retail_decision_console_demo_sections,
    retail_decision_console_demo_state,
)
from stark_terminal_core.retail_decision_console.state_safety import (
    assert_demo_state_has_no_action_generation,
    assert_demo_state_has_no_broker_controls,
    assert_demo_state_has_no_confidence_scoring,
    assert_demo_state_has_no_decision_object_generation,
    assert_demo_state_has_no_execution,
    assert_demo_state_has_no_live_data,
    assert_demo_state_has_no_order_buttons,
    assert_demo_state_has_no_recommendations,
    assert_retail_decision_console_demo_state_is_safe,
    retail_decision_console_demo_state_forbidden_terms,
)
from stark_terminal_core.retail_decision_console.static_state import (
    RetailDecisionConsoleCardState,
    RetailDecisionConsoleProvenanceState,
    RetailDecisionConsoleSectionState,
    RetailDecisionConsoleStaticState,
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


def test_retail_decision_console_demo_static_state_validates() -> None:
    state = retail_decision_console_demo_state()

    assert state.state_id == "retail-decision-console-demo-static-state-v1"
    assert state.stage == "demo_static_state"
    assert state.demo_static_state_only is True
    assert state.demo_only is True
    assert state.unavailable is True
    assert state.read_only is True
    assert state.created_at == DEMO_CREATED_AT
    assert state.provenance.demo_only is True
    assert state.provenance.static_only is True
    assert state.provenance.unavailable is True
    assert state.provenance.source_validated is False
    assert state.provenance.data_quality_validated is False
    assert state.provenance.live_market_data_source is False
    provenance_text = " ".join([state.provenance.label, state.provenance.source_type, *state.provenance.notes]).lower()
    assert "demo" in provenance_text
    assert "static" in provenance_text
    assert "unavailable" in provenance_text
    assert len(state.sections) == 13
    for flag in DANGEROUS_FLAGS:
        assert getattr(state, flag) is False
    assert_retail_decision_console_demo_state_is_safe(state)


def test_retail_decision_console_demo_sections_and_cards_validate() -> None:
    sections = retail_decision_console_demo_sections()
    cards = retail_decision_console_demo_cards("test-section")
    section_ids = {section.section_id for section in sections}

    assert {
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
    } <= section_ids
    assert cards
    for section in sections:
        assert section.demo_only is True
        assert section.unavailable is True
        assert section.active_decision_labels == []
        for flag in DANGEROUS_FLAGS:
            assert getattr(section, flag) is False
        for card in section.cards:
            assert card.demo_only is True
            assert card.unavailable is True
            assert card.active_decision_labels == []
            assert card.numeric_confidence_score is None
            for flag in DANGEROUS_FLAGS:
                assert getattr(card, flag) is False


def test_retail_decision_console_demo_state_rejects_unsafe_values() -> None:
    state = retail_decision_console_demo_state()
    card = retail_decision_console_demo_cards("unsafe")[0]

    with pytest.raises(ValidationError):
        RetailDecisionConsoleProvenanceState(
            provenance_id="bad-provenance",
            label="demo only",
            source_type="demo",
        )
    with pytest.raises(ValidationError):
        RetailDecisionConsoleCardState(
            card_id="bad-card",
            title="Bad card",
            body="Bad",
            numeric_confidence_score=0.7,
        )
    with pytest.raises(ValidationError):
        RetailDecisionConsoleCardState(
            card_id="bad-card",
            title="Bad card",
            body="Bad",
            active_decision_labels=["Buy"],
        )
    with pytest.raises(ValidationError):
        RetailDecisionConsoleSectionState(
            section_id="bad-section",
            title="Bad section",
            body="Bad",
            cards=[card],
            recommendations_enabled=True,
        )
    with pytest.raises(ValidationError):
        RetailDecisionConsoleStaticState(
            state_id="bad-state",
            provenance=state.provenance,
            sections=[],
        )


def test_retail_decision_console_demo_state_helpers_reject_mutated_flags() -> None:
    state = retail_decision_console_demo_state()

    with pytest.raises(ValueError):
        assert_demo_state_has_no_live_data(state.model_copy(update={"live_data_enabled": True}))
    with pytest.raises(ValueError):
        assert_demo_state_has_no_recommendations(state.model_copy(update={"recommendations_enabled": True}))
    with pytest.raises(ValueError):
        assert_demo_state_has_no_action_generation(state.model_copy(update={"action_generation_enabled": True}))
    with pytest.raises(ValueError):
        assert_demo_state_has_no_confidence_scoring(state.model_copy(update={"confidence_scoring_enabled": True}))
    with pytest.raises(ValueError):
        assert_demo_state_has_no_decision_object_generation(
            state.model_copy(update={"decision_object_generation_enabled": True})
        )
    with pytest.raises(ValueError):
        assert_demo_state_has_no_broker_controls(state.model_copy(update={"broker_controls_enabled": True}))
    with pytest.raises(ValueError):
        assert_demo_state_has_no_order_buttons(state.model_copy(update={"order_buttons_enabled": True}))
    with pytest.raises(ValueError):
        assert_demo_state_has_no_execution(state.model_copy(update={"execution_enabled": True}))


def test_retail_decision_console_demo_state_has_no_active_forbidden_labels() -> None:
    state = retail_decision_console_demo_state()
    forbidden = set(retail_decision_console_demo_state_forbidden_terms())

    assert state.sections
    for section in state.sections:
        assert not forbidden.intersection(section.active_decision_labels)
        for card in section.cards:
            assert not forbidden.intersection(card.active_decision_labels)
