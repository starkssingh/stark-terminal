import pytest
from pydantic import ValidationError

from stark_terminal_core.retail_decision_console.interactions import (
    FORBIDDEN_RETAIL_DECISION_CONSOLE_INTERACTION_TYPES,
    STATIC_INTERACTION_STAGE,
    RetailDecisionConsoleInteractionDescriptor,
    RetailDecisionConsoleInteractionState,
    RetailDecisionConsoleInteractionType,
    retail_decision_console_static_interactions,
)
from stark_terminal_core.retail_decision_console.state_view_model import (
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
    "Generate Signal",
    "Generate Trade",
    "Recalculate Confidence",
    "Connect Live Data",
}


def test_static_interaction_descriptors_validate() -> None:
    state = retail_decision_console_static_interactions()
    allowed_types = {interaction_type.value for interaction_type in RetailDecisionConsoleInteractionType}

    assert state.stage == STATIC_INTERACTION_STAGE
    assert state.static_interaction_placeholders_only is True
    assert state.demo_only is True
    assert state.unavailable is True
    assert state.local_only is True
    assert state.read_only is True
    assert state.interactions
    assert {interaction.interaction_type.value for interaction in state.interactions} <= allowed_types
    assert {interaction.interaction_type.value for interaction in state.interactions}.isdisjoint(
        FORBIDDEN_RETAIL_DECISION_CONSOLE_INTERACTION_TYPES
    )
    for flag in DANGEROUS_FLAGS:
        assert getattr(state, flag) is False
        assert state.safety_flags[flag] is False

    for interaction in state.interactions:
        assert interaction.interaction_id
        assert interaction.label
        assert interaction.target_section_id
        assert interaction.demo_only is True
        assert interaction.unavailable is True
        assert interaction.local_only is True
        assert interaction.read_only is True
        assert interaction.label not in FORBIDDEN_ACTIVE_LABELS
        for flag in DANGEROUS_FLAGS:
            assert getattr(interaction, flag) is False
            assert interaction.safety_flags[flag] is False


def test_forbidden_interaction_types_are_rejected() -> None:
    for interaction_type in FORBIDDEN_RETAIL_DECISION_CONSOLE_INTERACTION_TYPES:
        with pytest.raises(ValidationError):
            RetailDecisionConsoleInteractionDescriptor(
                interaction_id="bad-interaction",
                label="Bad static placeholder",
                interaction_type=interaction_type,
                target_section_id="decision-summary",
            )


def test_static_interactions_reject_unsafe_flags() -> None:
    safe_state = retail_decision_console_static_interactions()

    with pytest.raises(ValidationError):
        RetailDecisionConsoleInteractionDescriptor(
            interaction_id="unsafe-interaction",
            label="Unsafe placeholder",
            interaction_type=RetailDecisionConsoleInteractionType.SECTION_TOGGLE,
            target_section_id="decision-summary",
            live_data_enabled=True,
        )
    with pytest.raises(ValidationError):
        RetailDecisionConsoleInteractionState(
            interactions=safe_state.interactions,
            execution_enabled=True,
        )


def test_shell_view_model_exposes_static_interactions_without_dangerous_flags() -> None:
    view_model = retail_decision_console_state_view_model()

    assert view_model.static_interaction_placeholders_only is True
    assert view_model.demo_only is True
    assert view_model.unavailable is True
    assert view_model.read_only is True
    assert view_model.interactions
    for flag in DANGEROUS_FLAGS:
        assert getattr(view_model, flag) is False
        assert view_model.safety_flags[flag] is False
    for interaction in view_model.interactions:
        assert interaction.demo_only is True
        assert interaction.unavailable is True
        assert interaction.local_only is True
        assert interaction.read_only is True
        assert interaction.label not in FORBIDDEN_ACTIVE_LABELS
        for flag in DANGEROUS_FLAGS:
            assert getattr(interaction, flag) is False


def test_static_interactions_do_not_expose_forbidden_active_decision_labels() -> None:
    view_model = retail_decision_console_state_view_model()
    labels = {interaction.label for interaction in view_model.interactions}
    section_titles = {section.title for section in view_model.sections}
    card_titles = {card.title for section in view_model.sections for card in section.cards}

    assert labels.isdisjoint(FORBIDDEN_ACTIVE_LABELS)
    assert section_titles.isdisjoint(FORBIDDEN_ACTIVE_LABELS)
    assert card_titles.isdisjoint(FORBIDDEN_ACTIVE_LABELS)
