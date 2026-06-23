from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.retail_dashboard_display.badges import default_retail_dashboard_display_badges
from stark_terminal_core.retail_dashboard_display.contracts import (
    default_retail_dashboard_display_contract_metadata,
)
from stark_terminal_core.retail_dashboard_display.health import check_retail_dashboard_display_health
from stark_terminal_core.retail_dashboard_display.layouts import default_retail_dashboard_layout_placeholders
from stark_terminal_core.retail_dashboard_display.sections import (
    default_retail_dashboard_visual_section_placeholders,
)
from stark_terminal_core.retail_dashboard_display.unavailable import (
    default_retail_dashboard_display_unavailable_response,
)
from stark_terminal_core.retail_dashboard_display.widgets import default_retail_dashboard_widget_placeholders

router = APIRouter()


@router.get("/retail-dashboard-display/health")
def retail_dashboard_display_health() -> dict[str, Any]:
    status = check_retail_dashboard_display_health(get_settings())
    return {
        "service": "stark-terminal-retail-dashboard-display",
        **status.model_dump(),
    }


@router.get("/retail-dashboard-display/contracts")
def retail_dashboard_display_contracts() -> dict[str, Any]:
    settings = get_settings()
    metadata = default_retail_dashboard_display_contract_metadata()
    return {
        "service": "stark-terminal-retail-dashboard-display",
        "schema_version": settings.retail_dashboard_display_schema_version,
        "computation_scope": "display-contract-skeleton-only",
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
        "returns_unavailable_by_default": True,
        "layout_kinds": [layout_kind.value for layout_kind in metadata.layout_kinds],
        "widget_kinds": [widget_kind.value for widget_kind in metadata.widget_kinds],
        "section_kinds": [section_kind.value for section_kind in metadata.section_kinds],
        "badge_kinds": [badge_kind.value for badge_kind in metadata.badge_kinds],
        "forbidden_outputs": list(metadata.forbidden_outputs),
    }


@router.get("/retail-dashboard-display/unavailable-template")
def retail_dashboard_display_unavailable_template() -> dict[str, Any]:
    unavailable = default_retail_dashboard_display_unavailable_response()
    return {
        "service": "stark-terminal-retail-dashboard-display",
        "display_contract_skeleton_only": True,
        "unavailable_response": unavailable.model_dump(mode="json"),
        "no_active_ui": True,
        "no_recommendations": True,
        "no_action_generation": True,
        "no_confidence_scoring": True,
        "no_decision_object": True,
        "no_readiness_to_trade": True,
        "no_broker_controls": True,
        "no_execution": True,
        "no_approval": True,
        "no_override": True,
    }


@router.get("/retail-dashboard-display/placeholder-layout")
def retail_dashboard_display_placeholder_layout() -> dict[str, Any]:
    layouts = default_retail_dashboard_layout_placeholders()
    widgets = default_retail_dashboard_widget_placeholders()
    sections = default_retail_dashboard_visual_section_placeholders()
    badges = default_retail_dashboard_display_badges()
    unavailable = default_retail_dashboard_display_unavailable_response()
    return {
        "service": "stark-terminal-retail-dashboard-display",
        "display_contract_skeleton_only": True,
        "layouts": [layout.model_dump(mode="json") for layout in layouts],
        "widgets": [widget.model_dump(mode="json") for widget in widgets],
        "visual_sections": [section.model_dump(mode="json") for section in sections],
        "badges": [badge.model_dump(mode="json") for badge in badges],
        "unavailable_response": unavailable.model_dump(mode="json"),
        "no_active_ui": True,
        "no_generated_outputs": True,
        "no_broker_controls": True,
        "no_execution": True,
        "active_ui_generated": False,
        "recommendation_generated": False,
        "action_generated": False,
        "confidence_generated": False,
        "decision_object_generated": False,
        "readiness_to_trade_generated": False,
        "broker_control_generated": False,
        "execution_ready": False,
        "approval_granted": False,
        "override_granted": False,
    }
