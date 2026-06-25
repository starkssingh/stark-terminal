from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.retail_trader_experience_display.badges import (
    default_retail_trader_experience_display_badges,
)
from stark_terminal_core.retail_trader_experience_display.contracts import (
    default_retail_trader_experience_display_contract_metadata,
)
from stark_terminal_core.retail_trader_experience_display.health import (
    check_retail_trader_experience_display_health,
)
from stark_terminal_core.retail_trader_experience_display.journeys import (
    default_retail_trader_experience_display_journey_placeholders,
)
from stark_terminal_core.retail_trader_experience_display.personas import (
    default_retail_trader_experience_display_persona_placeholders,
)
from stark_terminal_core.retail_trader_experience_display.sections import (
    default_retail_trader_experience_display_section_placeholders,
)
from stark_terminal_core.retail_trader_experience_display.unavailable import (
    default_retail_trader_experience_display_unavailable_response,
)
from stark_terminal_core.retail_trader_experience_display.widgets import (
    default_retail_trader_experience_display_widget_placeholders,
)

router = APIRouter()


@router.get("/retail-trader-experience-display/health")
def retail_trader_experience_display_health() -> dict[str, Any]:
    status = check_retail_trader_experience_display_health(get_settings())
    return {
        "service": "stark-terminal-retail-trader-experience-display",
        **status.model_dump(),
    }


@router.get("/retail-trader-experience-display/contracts")
def retail_trader_experience_display_contracts() -> dict[str, Any]:
    settings = get_settings()
    metadata = default_retail_trader_experience_display_contract_metadata()
    return {
        "service": "stark-terminal-retail-trader-experience-display",
        "schema_version": settings.retail_trader_experience_display_schema_version,
        "computation_scope": "display-contract-skeleton-only",
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
        "returns_unavailable_by_default": True,
        "persona_kinds": [kind.value for kind in metadata.persona_kinds],
        "journey_kinds": [kind.value for kind in metadata.journey_kinds],
        "section_kinds": [kind.value for kind in metadata.section_kinds],
        "widget_kinds": [kind.value for kind in metadata.widget_kinds],
        "badge_kinds": [kind.value for kind in metadata.badge_kinds],
        "forbidden_outputs": list(metadata.forbidden_outputs),
    }


@router.get("/retail-trader-experience-display/unavailable-template")
def retail_trader_experience_display_unavailable_template() -> dict[str, Any]:
    unavailable = default_retail_trader_experience_display_unavailable_response()
    return {
        "service": "stark-terminal-retail-trader-experience-display",
        "display_contract_skeleton_only": True,
        "unavailable_response": unavailable.model_dump(mode="json"),
        "no_active_ui": True,
        "no_frontend_components": True,
        "no_desktop_components": True,
        "no_recommendations": True,
        "no_action_generation": True,
        "no_confidence_scoring": True,
        "no_decision_object": True,
        "no_readiness_to_trade": True,
        "no_broker_controls": True,
        "no_suitability_profiling": True,
        "no_execution": True,
        "no_approval": True,
        "no_override": True,
    }


@router.get("/retail-trader-experience-display/placeholder-experience")
def retail_trader_experience_display_placeholder_experience() -> dict[str, Any]:
    return {
        "service": "stark-terminal-retail-trader-experience-display",
        "display_contract_skeleton_only": True,
        "persona_placeholders": [
            persona.model_dump(mode="json")
            for persona in default_retail_trader_experience_display_persona_placeholders()
        ],
        "journey_placeholders": [
            journey.model_dump(mode="json")
            for journey in default_retail_trader_experience_display_journey_placeholders()
        ],
        "visual_sections": [
            section.model_dump(mode="json")
            for section in default_retail_trader_experience_display_section_placeholders()
        ],
        "widgets": [
            widget.model_dump(mode="json")
            for widget in default_retail_trader_experience_display_widget_placeholders()
        ],
        "badges": [
            badge.model_dump(mode="json")
            for badge in default_retail_trader_experience_display_badges()
        ],
        "unavailable_response": default_retail_trader_experience_display_unavailable_response().model_dump(
            mode="json"
        ),
        "no_active_ui": True,
        "no_generated_outputs": True,
        "no_broker_controls": True,
        "no_suitability_profiling": True,
        "no_execution": True,
        "active_ui_generated": False,
        "frontend_component_generated": False,
        "desktop_component_generated": False,
        "recommendation_generated": False,
        "action_generated": False,
        "confidence_generated": False,
        "decision_object_generated": False,
        "readiness_to_trade_generated": False,
        "broker_control_generated": False,
        "suitability_profile_generated": False,
        "execution_ready": False,
        "approval_granted": False,
        "override_granted": False,
    }
