from pydantic import ValidationError

from stark_terminal_core.retail_decision_console.cards import (
    DecisionBiasCardPlaceholder,
    default_retail_decision_console_card_placeholders,
)
from stark_terminal_core.retail_decision_console.health import (
    retail_decision_console_health,
)
from stark_terminal_core.retail_decision_console.navigation import (
    ConsoleNavigationItemPlaceholder,
    default_retail_decision_console_navigation_placeholder,
)
from stark_terminal_core.retail_decision_console.productization import (
    RetailDecisionConsoleProductizationPlan,
    default_retail_decision_console_productization_plan,
)
from stark_terminal_core.retail_decision_console.readiness import (
    retail_decision_console_readiness,
)
from stark_terminal_core.retail_decision_console.sections import (
    DecisionSummarySectionPlaceholder,
    default_retail_decision_console_section_placeholders,
)
from stark_terminal_core.retail_decision_console.ui_boundary import (
    RetailDecisionConsoleUiShellBoundary,
    default_retail_decision_console_ui_boundary,
)
from stark_terminal_core.retail_decision_console.unavailable import (
    RetailDecisionConsoleUnavailableState,
    unavailable_retail_decision_console_state,
)


DANGEROUS_FALSE_FIELDS = [
    "live_decisions_enabled",
    "recommendations_enabled",
    "action_generation_enabled",
    "confidence_scoring_enabled",
    "decision_object_generation_enabled",
    "live_market_data_enabled",
    "broker_controls_enabled",
    "execution_enabled",
]


def test_retail_decision_console_productization_plan_validates() -> None:
    plan = default_retail_decision_console_productization_plan()

    assert plan.service == "stark-terminal-retail-decision-console"
    assert plan.stage == "productization_plan"
    assert plan.planning_only is True
    assert plan.productization_plan_only is True
    assert plan.read_only is True
    assert plan.unavailable_by_default is True
    for field in [*DANGEROUS_FALSE_FIELDS, "order_buttons_enabled"]:
        assert getattr(plan, field) is False

    with pytest_raises_validation():
        RetailDecisionConsoleProductizationPlan(
            plan_id="unsafe",
            live_decisions_enabled=True,
        )


def test_retail_decision_console_ui_boundary_validates() -> None:
    boundary = default_retail_decision_console_ui_boundary()

    assert boundary.placeholder_only is True
    assert boundary.read_only is True
    assert "app frame placeholder" in boundary.allowed_shell_concepts
    assert "instrument selector placeholder" in boundary.allowed_shell_concepts
    assert "order buttons" in boundary.forbidden_shell_capabilities
    assert boundary.order_buttons_enabled is False
    assert boundary.execution_controls_enabled is False

    with pytest_raises_validation():
        RetailDecisionConsoleUiShellBoundary(
            boundary_id="unsafe",
            order_buttons_enabled=True,
        )


def test_navigation_section_and_card_placeholders_validate() -> None:
    navigation = default_retail_decision_console_navigation_placeholder()
    sections = default_retail_decision_console_section_placeholders()
    cards = default_retail_decision_console_card_placeholders()

    assert navigation.placeholder_only is True
    assert navigation.read_only is True
    assert navigation.items
    for item in navigation.items:
        assert item.launch_execution_enabled is False
        assert item.broker_controls_enabled is False
        assert item.recommendation_trigger_enabled is False

    assert sections
    for section in sections:
        assert section.display_planning_only is True
        assert section.read_only is True
        for field in DANGEROUS_FALSE_FIELDS:
            assert getattr(section, field) is False

    assert cards
    for card in cards:
        assert card.display_planning_only is True
        assert card.generated_recommendations_enabled is False
        assert card.generated_confidence_scores_enabled is False
        assert card.active_decision_objects_enabled is False
        assert card.live_market_data_enabled is False
        assert card.broker_controls_enabled is False
        assert card.execution_controls_enabled is False

    with pytest_raises_validation():
        ConsoleNavigationItemPlaceholder(
            item_id="unsafe",
            label="Unsafe",
            target_placeholder="unsafe",
            broker_controls_enabled=True,
        )
    with pytest_raises_validation():
        DecisionSummarySectionPlaceholder(
            section_id="unsafe",
            label="Unsafe",
            description="Unsafe",
            recommendations_enabled=True,
        )
    with pytest_raises_validation():
        DecisionBiasCardPlaceholder(
            card_id="unsafe",
            label="Unsafe",
            description="Unsafe",
            generated_confidence_scores_enabled=True,
        )


def test_unavailable_readiness_and_health_remain_safe() -> None:
    unavailable = unavailable_retail_decision_console_state()
    readiness = retail_decision_console_readiness()
    health = retail_decision_console_health()

    assert unavailable.unavailable is True
    assert unavailable.allowed_stage == "productization_plan"
    assert unavailable.order_buttons_enabled is False
    assert unavailable.execution_enabled is False
    assert readiness.ready_for_productization_plan is True
    assert readiness.ready_for_ui_shell_skeleton is True
    assert readiness.ready_for_live_decisions is False
    assert readiness.ready_for_recommendations is False
    assert readiness.ready_for_confidence_scoring is False
    assert readiness.ready_for_decision_object_generation is False
    assert readiness.ready_for_broker_controls is False
    assert readiness.ready_for_execution is False
    assert health.productization_plan_only is True
    assert health.read_only is True
    assert health.unavailable_by_default is True
    assert health.status == "healthy"
    for field in [*DANGEROUS_FALSE_FIELDS, "order_buttons_enabled"]:
        assert getattr(health, field) is False

    with pytest_raises_validation():
        RetailDecisionConsoleUnavailableState(
            reason="unsafe",
            execution_enabled=True,
        )


class pytest_raises_validation:
    def __enter__(self) -> None:
        return None

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        assert exc_type is ValidationError
        return True
