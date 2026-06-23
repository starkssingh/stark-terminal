from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.decision_display.badges import default_decision_display_badges
from stark_terminal_core.decision_display.cards import default_decision_display_card_placeholders
from stark_terminal_core.decision_display.contracts import default_decision_display_contract_metadata
from stark_terminal_core.decision_display.health import check_decision_display_health
from stark_terminal_core.decision_display.references import (
    default_decision_display_evidence_reference,
    default_decision_display_safety_reference,
)
from stark_terminal_core.decision_display.sections import default_decision_display_section_placeholders
from stark_terminal_core.decision_display.unavailable import default_decision_display_unavailable_response

router = APIRouter()


@router.get("/decision-display/health")
def decision_display_health() -> dict[str, Any]:
    status = check_decision_display_health(get_settings())
    return {
        "service": "stark-terminal-decision-display",
        **status.model_dump(),
    }


@router.get("/decision-display/contracts")
def decision_display_contracts() -> dict[str, Any]:
    settings = get_settings()
    metadata = default_decision_display_contract_metadata()
    return {
        "service": "stark-terminal-decision-display",
        "schema_version": settings.decision_display_schema_version,
        "computation_scope": "display-contract-skeleton-only",
        "recommendations_allowed_now": False,
        "action_generation_allowed_now": False,
        "confidence_scoring_allowed_now": False,
        "decision_object_generation_allowed_now": False,
        "readiness_to_trade_allowed_now": False,
        "execution_allowed_now": False,
        "approval_allowed_now": False,
        "override_allowed_now": False,
        "returns_unavailable_by_default": True,
        "supported_section_kinds": [section.value for section in metadata.supported_section_kinds],
        "supported_card_kinds": [card.value for card in metadata.supported_card_kinds],
        "supported_badge_kinds": [badge.value for badge in metadata.supported_badge_kinds],
        "forbidden_outputs": list(metadata.forbidden_outputs),
    }


@router.get("/decision-display/unavailable-template")
def decision_display_unavailable_template() -> dict[str, Any]:
    unavailable = default_decision_display_unavailable_response()
    return {
        "service": "stark-terminal-decision-display",
        "display_contract_skeleton_only": True,
        "unavailable_response": unavailable.model_dump(mode="json"),
        "no_recommendations": True,
        "no_action_generation": True,
        "no_confidence_scoring": True,
        "no_decision_object": True,
        "no_readiness_to_trade": True,
        "no_approval": True,
        "no_override": True,
        "no_execution": True,
        "no_active_ui": True,
    }


@router.get("/decision-display/placeholder-layout")
def decision_display_placeholder_layout() -> dict[str, Any]:
    sections = default_decision_display_section_placeholders()
    cards = default_decision_display_card_placeholders()
    badges = default_decision_display_badges()
    evidence_reference = default_decision_display_evidence_reference()
    safety_reference = default_decision_display_safety_reference()
    unavailable = default_decision_display_unavailable_response()
    return {
        "service": "stark-terminal-decision-display",
        "planning_only": True,
        "display_contract_skeleton_only": True,
        "sections": [section.model_dump(mode="json") for section in sections],
        "cards": [card.model_dump(mode="json") for card in cards],
        "badges": [badge.model_dump(mode="json") for badge in badges],
        "evidence_reference_placeholder": evidence_reference.model_dump(mode="json"),
        "safety_reference_placeholder": safety_reference.model_dump(mode="json"),
        "unavailable_response": unavailable.model_dump(mode="json"),
        "no_generated_outputs": True,
        "recommendation_generated": False,
        "action_generated": False,
        "confidence_generated": False,
        "decision_object_generated": False,
        "readiness_to_trade_generated": False,
        "execution_ready": False,
        "approval_granted": False,
        "override_granted": False,
        "active_ui": False,
    }
