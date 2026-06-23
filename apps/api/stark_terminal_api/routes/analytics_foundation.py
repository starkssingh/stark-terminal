from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_analytics.foundation.contracts import default_analytics_module_plans
from stark_terminal_analytics.foundation.dependencies import (
    default_analytics_dependency_plan,
    list_blocked_heavy_dependencies_for_prompt_26,
)
from stark_terminal_analytics.foundation.health import check_analytics_foundation_health
from stark_terminal_analytics.foundation.roadmap import default_analytics_roadmap

router = APIRouter()


@router.get("/analytics-foundation/health")
def analytics_foundation_health() -> dict[str, Any]:
    status = check_analytics_foundation_health(get_settings())
    return {
        "service": "stark-terminal-analytics-foundation",
        **status.model_dump(),
    }


@router.get("/analytics-foundation/contracts")
def analytics_foundation_contracts() -> dict[str, Any]:
    settings = get_settings()
    planned_modules = default_analytics_module_plans()
    roadmap = default_analytics_roadmap()
    return {
        "service": "stark-terminal-analytics-foundation",
        "schema_version": settings.analytics_schema_version,
        "computation_implemented_now": False,
        "signals_allowed_now": False,
        "recommendations_allowed_now": False,
        "execution_allowed_now": False,
        "dependency_stage": settings.analytics_dependency_stage,
        "planned_modules": [module.module_id for module in planned_modules],
        "planned_next_prompts": [item.prompt for item in roadmap[:7]],
        "note": "Prompt 26 defines analytics planning contracts only; no analytics calculations are implemented.",
    }


@router.get("/analytics-foundation/dependencies")
def analytics_foundation_dependencies() -> dict[str, Any]:
    plan = default_analytics_dependency_plan()
    return {
        "service": "stark-terminal-analytics-foundation",
        "current_stage": plan.current_stage.value,
        "installed_now": "No new heavy analytics dependency is required by Prompt 26.",
        "planned_dependencies": [dependency.name for dependency in plan.dependencies],
        "blocked_heavy_dependencies_now": list_blocked_heavy_dependencies_for_prompt_26(),
        "heavy_dependencies_installed_now": False,
        "computation_implemented_now": False,
        "no_signals": True,
        "no_recommendations": True,
        "no_execution_apis": True,
    }
