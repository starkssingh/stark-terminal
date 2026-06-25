from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.retail_trader_experience.cards import (
    default_retail_trader_experience_card_placeholders,
)
from stark_terminal_core.retail_trader_experience.health import check_retail_trader_experience_health
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
    default_retail_trader_experience_planning_contract,
)
from stark_terminal_core.retail_trader_experience.readiness import (
    build_retail_trader_experience_readiness_report,
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

router = APIRouter()


@router.get("/retail-trader-experience/health")
def retail_trader_experience_health() -> dict[str, Any]:
    status = check_retail_trader_experience_health(get_settings())
    return {
        "service": "stark-terminal-retail-trader-experience",
        **status.model_dump(),
    }


@router.get("/retail-trader-experience/contracts")
def retail_trader_experience_contracts() -> dict[str, Any]:
    settings = get_settings()
    contract = default_retail_trader_experience_planning_contract()
    return {
        "service": "stark-terminal-retail-trader-experience",
        "schema_version": settings.retail_trader_experience_schema_version,
        "computation_scope": "planning-and-guardrails-only",
        "active_ui_allowed_now": False,
        "frontend_components_allowed_now": False,
        "desktop_components_allowed_now": False,
        "recommendations_allowed_now": False,
        "action_generation_allowed_now": False,
        "confidence_scoring_allowed_now": False,
        "decision_object_generation_allowed_now": False,
        "readiness_to_trade_allowed_now": False,
        "broker_controls_allowed_now": False,
        "execution_allowed_now": False,
        "approval_allowed_now": False,
        "override_allowed_now": False,
        "suitability_profiling_allowed_now": False,
        "planned_personas": [persona.value for persona in contract.planned_personas],
        "planned_journeys": [journey.value for journey in contract.planned_journeys],
        "planned_sections": [section.value for section in contract.planned_sections],
        "planned_cards": [card.value for card in contract.planned_cards],
        "forbidden_interactions": [interaction.value for interaction in contract.forbidden_interactions],
    }


@router.get("/retail-trader-experience/placeholder-experience")
def retail_trader_experience_placeholder_experience() -> dict[str, Any]:
    personas = default_retail_trader_persona_placeholders()
    journeys = default_retail_trader_journey_placeholders()
    sections = default_retail_trader_experience_section_placeholders()
    cards = default_retail_trader_experience_card_placeholders()
    dashboard_reference = default_retail_trader_experience_dashboard_reference()
    decision_reference = default_retail_trader_experience_decision_reference()
    safety_reference = default_retail_trader_experience_safety_reference()
    forbidden_interactions = default_retail_trader_experience_forbidden_interactions()
    return {
        "service": "stark-terminal-retail-trader-experience",
        "planning_only": True,
        "active_ui_allowed_now": False,
        "unavailable_by_default": True,
        "personas": [persona.model_dump(mode="json") for persona in personas],
        "journeys": [journey.model_dump(mode="json") for journey in journeys],
        "sections": [section.model_dump(mode="json") for section in sections],
        "cards": [card.model_dump(mode="json") for card in cards],
        "dashboard_references": [dashboard_reference.model_dump(mode="json")],
        "decision_references": [decision_reference.model_dump(mode="json")],
        "safety_references": [safety_reference.model_dump(mode="json")],
        "forbidden_interactions": [interaction.model_dump(mode="json") for interaction in forbidden_interactions],
        "no_active_ui": True,
        "no_recommendations": True,
        "no_action_generation": True,
        "no_confidence_scoring": True,
        "no_decision_object": True,
        "no_readiness_to_trade": True,
        "no_broker_controls": True,
        "no_suitability_profiling": True,
        "no_execution": True,
        "recommendation_generated": False,
        "action_generated": False,
        "confidence_generated": False,
        "decision_object_generated": False,
        "readiness_to_trade": False,
        "broker_control_enabled": False,
        "suitability_profile_generated": False,
        "execution_ready": False,
    }


@router.get("/retail-trader-experience/readiness-template")
def retail_trader_experience_readiness_template() -> dict[str, Any]:
    plan = default_retail_trader_experience_planning_contract()
    personas = default_retail_trader_persona_placeholders()
    journeys = default_retail_trader_journey_placeholders()
    sections = default_retail_trader_experience_section_placeholders()
    cards = default_retail_trader_experience_card_placeholders()
    forbidden_interactions = default_retail_trader_experience_forbidden_interactions()
    policy = default_retail_trader_experience_safety_policy(get_settings())
    safety_result = evaluate_retail_trader_experience_plan_safety(plan, policy)
    report = build_retail_trader_experience_readiness_report(
        plan,
        personas,
        journeys,
        sections,
        cards,
        forbidden_interactions,
        safety_result,
    )
    return {
        "service": "stark-terminal-retail-trader-experience",
        "planning_only": True,
        "readiness_report": report.model_dump(mode="json"),
        "ready_for_active_ui": False,
        "ready_for_recommendations": False,
        "ready_for_broker_controls": False,
        "ready_for_execution": False,
        "ready_for_suitability_profiling": False,
        "no_readiness_to_trade": True,
        "readiness_to_trade": False,
        "recommendation_generated": False,
        "action_generated": False,
        "confidence_generated": False,
        "decision_object_generated": False,
        "broker_control_enabled": False,
        "suitability_profile_generated": False,
        "execution_ready": False,
    }
