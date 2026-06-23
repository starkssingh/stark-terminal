from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.retail_dashboard.cards import default_retail_dashboard_card_placeholders
from stark_terminal_core.retail_dashboard.health import check_retail_dashboard_health
from stark_terminal_core.retail_dashboard.interactions import default_retail_dashboard_forbidden_interactions
from stark_terminal_core.retail_dashboard.planning import default_retail_dashboard_planning_contract
from stark_terminal_core.retail_dashboard.readiness import build_retail_dashboard_readiness_report
from stark_terminal_core.retail_dashboard.references import (
    default_retail_dashboard_data_source_references,
    default_retail_dashboard_decision_reference,
)
from stark_terminal_core.retail_dashboard.safety import (
    default_retail_dashboard_safety_policy,
    evaluate_retail_dashboard_plan_safety,
)
from stark_terminal_core.retail_dashboard.sections import default_retail_dashboard_section_placeholders

router = APIRouter()


@router.get("/retail-dashboard/health")
def retail_dashboard_health() -> dict[str, Any]:
    status = check_retail_dashboard_health(get_settings())
    return {
        "service": "stark-terminal-retail-dashboard",
        **status.model_dump(),
    }


@router.get("/retail-dashboard/contracts")
def retail_dashboard_contracts() -> dict[str, Any]:
    settings = get_settings()
    contract = default_retail_dashboard_planning_contract()
    return {
        "service": "stark-terminal-retail-dashboard",
        "schema_version": settings.retail_dashboard_schema_version,
        "computation_scope": "planning-and-guardrails-only",
        "active_ui_allowed_now": False,
        "recommendations_allowed_now": False,
        "action_generation_allowed_now": False,
        "confidence_scoring_allowed_now": False,
        "decision_object_generation_allowed_now": False,
        "readiness_to_trade_allowed_now": False,
        "broker_controls_allowed_now": False,
        "execution_allowed_now": False,
        "approval_allowed_now": False,
        "override_allowed_now": False,
        "planned_sections": [section.value for section in contract.planned_sections],
        "planned_cards": [card.value for card in contract.planned_cards],
        "forbidden_interactions": [interaction.value for interaction in contract.forbidden_interactions],
    }


@router.get("/retail-dashboard/placeholder-layout")
def retail_dashboard_placeholder_layout() -> dict[str, Any]:
    sections = default_retail_dashboard_section_placeholders()
    cards = default_retail_dashboard_card_placeholders()
    data_source_references = default_retail_dashboard_data_source_references()
    decision_reference = default_retail_dashboard_decision_reference()
    forbidden_interactions = default_retail_dashboard_forbidden_interactions()
    return {
        "service": "stark-terminal-retail-dashboard",
        "planning_only": True,
        "active_ui_allowed_now": False,
        "unavailable_by_default": True,
        "sections": [section.model_dump(mode="json") for section in sections],
        "cards": [card.model_dump(mode="json") for card in cards],
        "data_source_references": [reference.model_dump(mode="json") for reference in data_source_references],
        "decision_reference": decision_reference.model_dump(mode="json"),
        "forbidden_interactions": [interaction.model_dump(mode="json") for interaction in forbidden_interactions],
        "no_active_ui": True,
        "no_recommendations": True,
        "no_action_generation": True,
        "no_confidence_scoring": True,
        "no_decision_object": True,
        "no_readiness_to_trade": True,
        "no_broker_controls": True,
        "no_execution": True,
        "recommendation_generated": False,
        "action_generated": False,
        "confidence_generated": False,
        "decision_object_generated": False,
        "readiness_to_trade": False,
        "broker_control_enabled": False,
        "execution_ready": False,
    }


@router.get("/retail-dashboard/readiness-template")
def retail_dashboard_readiness_template() -> dict[str, Any]:
    plan = default_retail_dashboard_planning_contract()
    sections = default_retail_dashboard_section_placeholders()
    cards = default_retail_dashboard_card_placeholders()
    forbidden_interactions = default_retail_dashboard_forbidden_interactions()
    policy = default_retail_dashboard_safety_policy(get_settings())
    safety_result = evaluate_retail_dashboard_plan_safety(plan, policy)
    report = build_retail_dashboard_readiness_report(plan, sections, cards, forbidden_interactions, safety_result)
    return {
        "service": "stark-terminal-retail-dashboard",
        "planning_only": True,
        "readiness_report": report.model_dump(mode="json"),
        "ready_for_active_ui": False,
        "ready_for_recommendations": False,
        "ready_for_broker_controls": False,
        "ready_for_execution": False,
        "no_readiness_to_trade": True,
        "readiness_to_trade": False,
        "recommendation_generated": False,
        "action_generated": False,
        "confidence_generated": False,
        "decision_object_generated": False,
        "broker_control_enabled": False,
        "execution_ready": False,
    }
