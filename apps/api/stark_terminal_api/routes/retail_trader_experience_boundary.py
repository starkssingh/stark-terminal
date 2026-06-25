from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.retail_trader_experience_boundary.endpoints import (
    default_retail_trader_experience_endpoint_boundary_policies,
)
from stark_terminal_core.retail_trader_experience_boundary.forbidden import (
    default_retail_trader_experience_forbidden_behavior_registry,
)
from stark_terminal_core.retail_trader_experience_boundary.health import (
    check_retail_trader_experience_boundary_health,
)
from stark_terminal_core.retail_trader_experience_boundary.invariants import (
    evaluate_retail_trader_experience_boundary_invariants,
)
from stark_terminal_core.retail_trader_experience_boundary.modules import (
    default_retail_trader_experience_module_boundary_policies,
)

router = APIRouter()


@router.get("/retail-trader-experience-boundary/health")
def retail_trader_experience_boundary_health() -> dict[str, Any]:
    status = check_retail_trader_experience_boundary_health(get_settings())
    return {
        "service": "stark-terminal-retail-trader-experience-boundary",
        **status.model_dump(),
    }


@router.get("/retail-trader-experience-boundary/contracts")
def retail_trader_experience_boundary_contracts() -> dict[str, Any]:
    settings = get_settings()
    registry = default_retail_trader_experience_forbidden_behavior_registry()
    endpoint_policies = default_retail_trader_experience_endpoint_boundary_policies()
    module_policies = default_retail_trader_experience_module_boundary_policies()
    return {
        "service": "stark-terminal-retail-trader-experience-boundary",
        "schema_version": settings.retail_trader_experience_boundary_schema_version,
        "computation_scope": "boundary-hardening-only",
        "forbidden_behaviors": [behavior.kind.value for behavior in registry.behaviors],
        "endpoint_families": [policy.endpoint_family for policy in endpoint_policies],
        "module_families": [policy.module_family for policy in module_policies],
        "active_ui_allowed_now": False,
        "frontend_components_allowed_now": False,
        "desktop_components_allowed_now": False,
        "recommendations_allowed_now": False,
        "action_generation_allowed_now": False,
        "confidence_scoring_allowed_now": False,
        "decision_object_generation_allowed_now": False,
        "readiness_to_trade_allowed_now": False,
        "suitability_profiling_allowed_now": False,
        "broker_controls_allowed_now": False,
        "execution_allowed_now": False,
        "approval_allowed_now": False,
        "override_allowed_now": False,
    }


@router.get("/retail-trader-experience-boundary/invariants")
def retail_trader_experience_boundary_invariants() -> dict[str, Any]:
    result = evaluate_retail_trader_experience_boundary_invariants()
    return {
        "service": "stark-terminal-retail-trader-experience-boundary",
        "boundary_hardening_only": True,
        "invariant_result": result.model_dump(mode="json"),
        "blockers": list(result.blockers),
        "warnings": list(result.warnings),
        "no_active_ui": True,
        "no_frontend_components": True,
        "no_desktop_components": True,
        "no_recommendations": True,
        "no_action_generation": True,
        "no_confidence_scoring": True,
        "no_decision_object": True,
        "no_readiness_to_trade": True,
        "no_suitability_profiling": True,
        "no_broker_controls": True,
        "no_approval": True,
        "no_override": True,
        "no_execution": True,
        "active_ui_generated": False,
        "frontend_component_generated": False,
        "desktop_component_generated": False,
        "recommendation_generated": False,
        "action_generated": False,
        "confidence_generated": False,
        "decision_object_generated": False,
        "readiness_to_trade_generated": False,
        "suitability_profile_generated": False,
        "broker_control_enabled": False,
        "approval_granted": False,
        "override_granted": False,
        "execution_ready": False,
    }
