from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.decision_boundary.endpoints import default_decision_endpoint_boundary_policies
from stark_terminal_core.decision_boundary.forbidden import default_decision_forbidden_behavior_registry
from stark_terminal_core.decision_boundary.health import check_decision_boundary_health
from stark_terminal_core.decision_boundary.invariants import evaluate_decision_boundary_invariants
from stark_terminal_core.decision_boundary.modules import default_decision_module_boundary_policies

router = APIRouter()


@router.get("/decision-boundary/health")
def decision_boundary_health() -> dict[str, Any]:
    status = check_decision_boundary_health(get_settings())
    return {
        "service": "stark-terminal-decision-boundary",
        **status.model_dump(),
    }


@router.get("/decision-boundary/contracts")
def decision_boundary_contracts() -> dict[str, Any]:
    settings = get_settings()
    registry = default_decision_forbidden_behavior_registry()
    endpoint_policies = default_decision_endpoint_boundary_policies()
    module_policies = default_decision_module_boundary_policies()
    return {
        "service": "stark-terminal-decision-boundary",
        "schema_version": settings.decision_boundary_schema_version,
        "computation_scope": "boundary-hardening-only",
        "forbidden_behaviors": [behavior.kind.value for behavior in registry.behaviors],
        "endpoint_families": [policy.endpoint_family for policy in endpoint_policies],
        "module_families": [policy.module_family for policy in module_policies],
        "recommendations_allowed_now": False,
        "action_generation_allowed_now": False,
        "confidence_scoring_allowed_now": False,
        "decision_object_generation_allowed_now": False,
        "execution_allowed_now": False,
        "approval_allowed_now": False,
        "override_allowed_now": False,
        "active_ui_allowed_now": False,
        "active_workflow_allowed_now": False,
        "readiness_to_trade_allowed_now": False,
    }


@router.get("/decision-boundary/invariants")
def decision_boundary_invariants() -> dict[str, Any]:
    result = evaluate_decision_boundary_invariants()
    return {
        "service": "stark-terminal-decision-boundary",
        "boundary_hardening_only": True,
        "invariant_result": result.model_dump(mode="json"),
        "blockers": list(result.blockers),
        "warnings": list(result.warnings),
        "no_recommendations": True,
        "no_action_generation": True,
        "no_confidence_scoring": True,
        "no_decision_object": True,
        "no_approval": True,
        "no_override": True,
        "no_active_ui": True,
        "no_active_workflow": True,
        "no_readiness_to_trade": True,
        "no_execution": True,
        "recommendation_generated": False,
        "action_generated": False,
        "confidence_generated": False,
        "decision_object_generated": False,
        "approval_granted": False,
        "override_granted": False,
        "active_ui": False,
        "workflow_active": False,
        "readiness_to_trade": False,
        "execution_ready": False,
    }
