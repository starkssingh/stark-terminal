from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.retail_decision_console.cards import (
    default_retail_decision_console_card_placeholders,
)
from stark_terminal_core.retail_decision_console.demo_state import (
    retail_decision_console_demo_state,
)
from stark_terminal_core.retail_decision_console.health import (
    retail_decision_console_health,
)
from stark_terminal_core.retail_decision_console.navigation import (
    default_retail_decision_console_navigation_placeholder,
)
from stark_terminal_core.retail_decision_console.productization import (
    default_retail_decision_console_productization_plan,
)
from stark_terminal_core.retail_decision_console.readiness import (
    retail_decision_console_readiness,
)
from stark_terminal_core.retail_decision_console.sections import (
    default_retail_decision_console_section_placeholders,
)
from stark_terminal_core.retail_decision_console.state_view_model import (
    retail_decision_console_state_view_model,
)
from stark_terminal_core.retail_decision_console.ui_boundary import (
    default_retail_decision_console_ui_boundary,
)
from stark_terminal_core.retail_decision_console.unavailable import (
    unavailable_retail_decision_console_state,
)

router = APIRouter()


def _safe_flags() -> dict[str, bool]:
    return {
        "planning_only": True,
        "productization_plan_only": True,
        "read_only": True,
        "unavailable_by_default": True,
        "live_decisions_enabled": False,
        "recommendations_enabled": False,
        "action_generation_enabled": False,
        "confidence_scoring_enabled": False,
        "decision_object_generation_enabled": False,
        "live_market_data_enabled": False,
        "broker_controls_enabled": False,
        "order_buttons_enabled": False,
        "execution_enabled": False,
    }


def _base_response() -> dict[str, Any]:
    return {
        "service": "stark-terminal-retail-decision-console",
        "no_live_data": True,
        "no_live_decisions": True,
        "no_recommendations": True,
        "no_action_generation": True,
        "no_confidence_scoring": True,
        "no_active_decision_object_generation": True,
        "no_live_market_data_claim": True,
        "no_broker_controls": True,
        "no_order_buttons": True,
        "no_execution": True,
        **_safe_flags(),
    }


def _demo_static_state_flags() -> dict[str, bool]:
    return {
        "demo_static_state_only": True,
        "demo_only": True,
        "unavailable": True,
    }


def _static_state_wiring_flags() -> dict[str, bool]:
    return {
        "static_state_wiring_only": True,
        "demo_only": True,
        "unavailable": True,
        "read_only": True,
    }


@router.get("/retail-decision-console/health")
def retail_decision_console_health_endpoint() -> dict[str, Any]:
    status = retail_decision_console_health(get_settings())
    return {
        **_base_response(),
        **status.model_dump(mode="json"),
    }


@router.get("/retail-decision-console/productization-plan")
def retail_decision_console_productization_plan_endpoint() -> dict[str, Any]:
    plan = default_retail_decision_console_productization_plan(get_settings())
    return {
        **_base_response(),
        "productization_plan": plan.model_dump(mode="json"),
    }


@router.get("/retail-decision-console/ui-boundary")
def retail_decision_console_ui_boundary_endpoint() -> dict[str, Any]:
    boundary = default_retail_decision_console_ui_boundary(get_settings())
    return {
        **_base_response(),
        "ui_boundary": boundary.model_dump(mode="json"),
        "allowed_shell_concepts": list(boundary.allowed_shell_concepts),
        "forbidden_shell_capabilities": list(boundary.forbidden_shell_capabilities),
    }


@router.get("/retail-decision-console/readiness")
def retail_decision_console_readiness_endpoint() -> dict[str, Any]:
    readiness = retail_decision_console_readiness(get_settings())
    return {
        **_base_response(),
        "readiness": readiness.model_dump(mode="json"),
        "next_allowed_phase": readiness.next_allowed_phase,
    }


@router.get("/retail-decision-console/unavailable-state")
def retail_decision_console_unavailable_state_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "unavailable_state": unavailable_retail_decision_console_state().model_dump(mode="json"),
    }


@router.get("/retail-decision-console/navigation-placeholder")
def retail_decision_console_navigation_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "navigation_placeholder": default_retail_decision_console_navigation_placeholder().model_dump(mode="json"),
    }


@router.get("/retail-decision-console/section-placeholder")
def retail_decision_console_section_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "section_placeholders": [
            placeholder.model_dump(mode="json")
            for placeholder in default_retail_decision_console_section_placeholders()
        ],
    }


@router.get("/retail-decision-console/card-placeholder")
def retail_decision_console_card_placeholder_endpoint() -> dict[str, Any]:
    return {
        **_base_response(),
        "card_placeholders": [
            placeholder.model_dump(mode="json")
            for placeholder in default_retail_decision_console_card_placeholders()
        ],
    }


@router.get("/retail-decision-console/demo-state")
def retail_decision_console_demo_state_endpoint() -> dict[str, Any]:
    state = retail_decision_console_demo_state()
    return {
        **_base_response(),
        **_demo_static_state_flags(),
        "demo_state": state.model_dump(mode="json"),
    }


@router.get("/retail-decision-console/static-state-view-model")
def retail_decision_console_static_state_view_model_endpoint() -> dict[str, Any]:
    view_model = retail_decision_console_state_view_model()
    return {
        **_base_response(),
        **_static_state_wiring_flags(),
        "view_model": view_model.model_dump(mode="json"),
    }
