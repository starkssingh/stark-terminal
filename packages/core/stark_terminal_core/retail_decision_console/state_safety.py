from __future__ import annotations

from stark_terminal_core.retail_decision_console.demo_state import (
    retail_decision_console_demo_state,
)
from stark_terminal_core.retail_decision_console.static_state import (
    FORBIDDEN_ACTIVE_DECISION_OUTPUTS,
    RetailDecisionConsoleStaticState,
)
from stark_terminal_core.retail_decision_console.ui_descriptors import (
    FORBIDDEN_ACTIVE_CONTROL_LABELS,
)


def _state_or_default(state: RetailDecisionConsoleStaticState | None) -> RetailDecisionConsoleStaticState:
    return state or retail_decision_console_demo_state()


def _sections_and_cards(state: RetailDecisionConsoleStaticState):
    for section in state.sections:
        yield section
        yield from section.cards


def retail_decision_console_demo_state_forbidden_terms() -> tuple[str, ...]:
    return (*FORBIDDEN_ACTIVE_CONTROL_LABELS, *FORBIDDEN_ACTIVE_DECISION_OUTPUTS)


def assert_demo_state_has_no_live_data(state: RetailDecisionConsoleStaticState | None = None) -> None:
    current = _state_or_default(state)
    if current.live_data_enabled or any(item.live_data_enabled for item in _sections_and_cards(current)):
        raise ValueError("Retail Decision Console demo state cannot enable live data")


def assert_demo_state_has_no_recommendations(state: RetailDecisionConsoleStaticState | None = None) -> None:
    current = _state_or_default(state)
    if current.recommendations_enabled or any(item.recommendations_enabled for item in _sections_and_cards(current)):
        raise ValueError("Retail Decision Console demo state cannot enable recommendations")


def assert_demo_state_has_no_action_generation(state: RetailDecisionConsoleStaticState | None = None) -> None:
    current = _state_or_default(state)
    if current.action_generation_enabled or any(item.action_generation_enabled for item in _sections_and_cards(current)):
        raise ValueError("Retail Decision Console demo state cannot enable action generation")


def assert_demo_state_has_no_confidence_scoring(state: RetailDecisionConsoleStaticState | None = None) -> None:
    current = _state_or_default(state)
    if current.confidence_scoring_enabled or any(
        item.confidence_scoring_enabled for item in _sections_and_cards(current)
    ):
        raise ValueError("Retail Decision Console demo state cannot enable confidence scoring")
    if any(getattr(item, "numeric_confidence_score", None) is not None for item in _sections_and_cards(current)):
        raise ValueError("Retail Decision Console demo state cannot expose confidence-like numeric scores")


def assert_demo_state_has_no_decision_object_generation(
    state: RetailDecisionConsoleStaticState | None = None,
) -> None:
    current = _state_or_default(state)
    if current.decision_object_generation_enabled or any(
        item.decision_object_generation_enabled for item in _sections_and_cards(current)
    ):
        raise ValueError("Retail Decision Console demo state cannot enable active DecisionObject generation")


def assert_demo_state_has_no_broker_controls(state: RetailDecisionConsoleStaticState | None = None) -> None:
    current = _state_or_default(state)
    if current.broker_controls_enabled or any(item.broker_controls_enabled for item in _sections_and_cards(current)):
        raise ValueError("Retail Decision Console demo state cannot enable broker controls")


def assert_demo_state_has_no_order_buttons(state: RetailDecisionConsoleStaticState | None = None) -> None:
    current = _state_or_default(state)
    if current.order_buttons_enabled or any(item.order_buttons_enabled for item in _sections_and_cards(current)):
        raise ValueError("Retail Decision Console demo state cannot enable order buttons")


def assert_demo_state_has_no_execution(state: RetailDecisionConsoleStaticState | None = None) -> None:
    current = _state_or_default(state)
    if current.execution_enabled or any(item.execution_enabled for item in _sections_and_cards(current)):
        raise ValueError("Retail Decision Console demo state cannot enable execution")


def assert_retail_decision_console_demo_state_is_safe(
    state: RetailDecisionConsoleStaticState | None = None,
) -> None:
    current = _state_or_default(state)
    assert_demo_state_has_no_live_data(current)
    assert_demo_state_has_no_recommendations(current)
    assert_demo_state_has_no_action_generation(current)
    assert_demo_state_has_no_confidence_scoring(current)
    assert_demo_state_has_no_decision_object_generation(current)
    assert_demo_state_has_no_broker_controls(current)
    assert_demo_state_has_no_order_buttons(current)
    assert_demo_state_has_no_execution(current)
