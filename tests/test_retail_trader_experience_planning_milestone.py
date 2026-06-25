from __future__ import annotations

from stark_terminal_core.retail_trader_experience.cards import (
    default_retail_trader_experience_card_placeholders,
)
from stark_terminal_core.retail_trader_experience.interactions import (
    default_retail_trader_experience_forbidden_interactions,
)
from stark_terminal_core.retail_trader_experience.journeys import (
    default_retail_trader_journey_placeholders,
)
from stark_terminal_core.retail_trader_experience.personas import (
    default_retail_trader_persona_placeholders,
)
from stark_terminal_core.retail_trader_experience.planning import (
    RetailTraderExperienceForbiddenInteractionKind,
    default_retail_trader_experience_planning_contract,
)
from stark_terminal_core.retail_trader_experience.readiness import (
    build_retail_trader_experience_readiness_report,
    retail_trader_experience_ready_for_active_ui,
    retail_trader_experience_ready_for_execution,
    retail_trader_experience_ready_for_recommendations,
    retail_trader_experience_ready_for_suitability_profiling,
)
from stark_terminal_core.retail_trader_experience.references import (
    default_retail_trader_experience_dashboard_reference,
    default_retail_trader_experience_decision_reference,
    default_retail_trader_experience_safety_reference,
)
from stark_terminal_core.retail_trader_experience.safety import (
    default_retail_trader_experience_safety_policy,
    evaluate_retail_trader_experience_plan_safety,
)
from stark_terminal_core.retail_trader_experience.sections import (
    default_retail_trader_experience_section_placeholders,
)


def test_retail_trader_experience_planning_remains_guardrails_only() -> None:
    plan = default_retail_trader_experience_planning_contract()
    assert plan.returns_unavailable_by_default is True

    for flag in [
        "active_ui_allowed",
        "frontend_components_allowed",
        "desktop_components_allowed",
        "recommendations_allowed",
        "action_generation_allowed",
        "confidence_scoring_allowed",
        "decision_object_generation_allowed",
        "readiness_to_trade_allowed",
        "broker_controls_allowed",
        "execution_allowed",
        "approval_allowed",
        "override_allowed",
        "suitability_profiling_allowed",
    ]:
        assert getattr(plan, flag) is False


def test_retail_trader_experience_placeholders_remain_placeholders() -> None:
    for persona in default_retail_trader_persona_placeholders():
        assert persona.planning_only is True
        assert persona.active_profile is False
        assert persona.suitability_profile is False
        assert persona.trading_permission_profile is False

    for journey in default_retail_trader_journey_placeholders():
        assert journey.planning_only is True
        assert journey.active_ui is False
        assert journey.unavailable is True

    for section in default_retail_trader_experience_section_placeholders():
        assert section.planning_only is True
        assert section.active_ui is False
        assert section.unavailable is True

    for card in default_retail_trader_experience_card_placeholders():
        assert card.planning_only is True
        assert card.active_ui is False
        assert card.unavailable is True
        assert card.recommendation_card is False
        assert card.decision_object_display is False
        assert card.suitability_profile_display is False


def test_forbidden_interaction_registry_remains_complete() -> None:
    plan = default_retail_trader_experience_planning_contract()
    default_interactions = default_retail_trader_experience_forbidden_interactions()
    kinds = set(plan.forbidden_interactions)
    interaction_kinds = {interaction.kind for interaction in default_interactions}

    for required in [
        RetailTraderExperienceForbiddenInteractionKind.RECOMMENDATION_CARD,
        RetailTraderExperienceForbiddenInteractionKind.ACTION_BUTTON,
        RetailTraderExperienceForbiddenInteractionKind.CONFIDENCE_SCORE,
        RetailTraderExperienceForbiddenInteractionKind.DECISION_OBJECT_DISPLAY,
        RetailTraderExperienceForbiddenInteractionKind.READINESS_TO_TRADE_BADGE,
        RetailTraderExperienceForbiddenInteractionKind.BROKER_CONTROL,
        RetailTraderExperienceForbiddenInteractionKind.ORDER_BUTTON,
        RetailTraderExperienceForbiddenInteractionKind.APPROVAL_CONTROL,
        RetailTraderExperienceForbiddenInteractionKind.OVERRIDE_CONTROL,
        RetailTraderExperienceForbiddenInteractionKind.SUITABILITY_PROFILING,
    ]:
        assert required in kinds
        assert required in interaction_kinds


def test_planning_safety_and_readiness_do_not_unlock_active_outputs() -> None:
    plan = default_retail_trader_experience_planning_contract()
    personas = default_retail_trader_persona_placeholders()
    journeys = default_retail_trader_journey_placeholders()
    sections = default_retail_trader_experience_section_placeholders()
    cards = default_retail_trader_experience_card_placeholders()
    interactions = default_retail_trader_experience_forbidden_interactions()
    policy = default_retail_trader_experience_safety_policy()
    result = evaluate_retail_trader_experience_plan_safety(plan, policy)
    report = build_retail_trader_experience_readiness_report(
        plan, personas, journeys, sections, cards, interactions, result
    )

    assert retail_trader_experience_ready_for_active_ui(report) is False
    assert retail_trader_experience_ready_for_recommendations(report) is False
    assert retail_trader_experience_ready_for_suitability_profiling(report) is False
    assert retail_trader_experience_ready_for_execution(report) is False
    assert report.ready_for_readiness_to_trade is False
    assert report.ready_for_broker_controls is False


def test_reference_placeholders_are_not_active_outputs() -> None:
    dashboard = default_retail_trader_experience_dashboard_reference()
    decision = default_retail_trader_experience_decision_reference()
    safety = default_retail_trader_experience_safety_reference()

    assert dashboard.active_dashboard is False
    assert dashboard.display_ready is False
    assert decision.active_decision_object is False
    assert decision.confidence_available is False
    assert decision.execution_available is False
    assert safety.safety_passed is False
    assert safety.approval_granted is False
    assert safety.override_granted is False
    assert safety.readiness_to_trade_allowed is False
    assert safety.broker_controls_allowed is False
    assert safety.execution_allowed is False
