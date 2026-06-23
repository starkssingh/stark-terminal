from __future__ import annotations

from stark_terminal_core.retail_dashboard.cards import default_retail_dashboard_card_placeholders
from stark_terminal_core.retail_dashboard.interactions import (
    RetailDashboardForbiddenInteractionKind,
    default_retail_dashboard_forbidden_interactions,
)
from stark_terminal_core.retail_dashboard.planning import (
    REQUIRED_FORBIDDEN_INTERACTIONS,
    default_retail_dashboard_planning_contract,
)
from stark_terminal_core.retail_dashboard.readiness import (
    build_retail_dashboard_readiness_report,
    retail_dashboard_ready_for_active_ui,
    retail_dashboard_ready_for_execution,
    retail_dashboard_ready_for_recommendations,
)
from stark_terminal_core.retail_dashboard.safety import (
    default_retail_dashboard_safety_policy,
    evaluate_retail_dashboard_plan_safety,
)
from stark_terminal_core.retail_dashboard.sections import default_retail_dashboard_section_placeholders


def test_retail_dashboard_planning_contract_remains_guardrails_only() -> None:
    plan = default_retail_dashboard_planning_contract()

    assert plan.stage.value.lower() == "planning_and_guardrails"
    assert plan.returns_unavailable_by_default is True
    assert plan.active_ui_allowed is False
    assert plan.recommendations_allowed is False
    assert plan.action_generation_allowed is False
    assert plan.confidence_scoring_allowed is False
    assert plan.decision_object_generation_allowed is False
    assert plan.readiness_to_trade_allowed is False
    assert plan.broker_controls_allowed is False
    assert plan.execution_allowed is False


def test_retail_dashboard_placeholders_remain_placeholders() -> None:
    for section in default_retail_dashboard_section_placeholders():
        assert section.active_ui is False
        assert section.unavailable is True
        assert section.planning_only is True
        assert section.recommendations_allowed is False
        assert section.execution_allowed is False

    for card in default_retail_dashboard_card_placeholders():
        assert card.active_ui is False
        assert card.unavailable is True
        assert card.planning_only is True
        assert card.recommendation_card is False
        assert card.action_card is False
        assert card.confidence_display is False
        assert card.decision_object_display is False
        assert card.broker_control is False
        assert card.execution_control is False


def test_forbidden_interaction_registry_remains_complete() -> None:
    interactions = default_retail_dashboard_forbidden_interactions()
    kinds = {interaction.kind for interaction in interactions}

    assert REQUIRED_FORBIDDEN_INTERACTIONS <= kinds
    assert RetailDashboardForbiddenInteractionKind.LIVE_DATA_CONTROL in kinds
    for interaction in interactions:
        assert interaction.forbidden_now is True
        assert interaction.requires_future_prompt is True
        assert interaction.requires_audit_before_unlock is True


def test_safety_and_readiness_helpers_do_not_permit_active_outputs() -> None:
    plan = default_retail_dashboard_planning_contract()
    sections = default_retail_dashboard_section_placeholders()
    cards = default_retail_dashboard_card_placeholders()
    interactions = default_retail_dashboard_forbidden_interactions()
    policy = default_retail_dashboard_safety_policy()
    safety_result = evaluate_retail_dashboard_plan_safety(plan, policy)
    report = build_retail_dashboard_readiness_report(plan, sections, cards, interactions, safety_result)

    assert safety_result.safe is True
    assert safety_result.active_ui_allowed is False
    assert safety_result.recommendations_allowed is False
    assert safety_result.execution_allowed is False
    assert retail_dashboard_ready_for_active_ui(report) is False
    assert retail_dashboard_ready_for_recommendations(report) is False
    assert retail_dashboard_ready_for_execution(report) is False
    assert report.ready_for_active_ui is False
    assert report.ready_for_recommendations is False
    assert report.ready_for_execution is False
