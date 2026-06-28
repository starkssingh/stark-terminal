from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.strategy_research_workspace_boundary.endpoints import (
    default_strategy_research_endpoint_boundary_policies,
)
from stark_terminal_core.strategy_research_workspace_boundary.forbidden import (
    default_strategy_research_forbidden_behavior_registry,
)
from stark_terminal_core.strategy_research_workspace_boundary.health import (
    check_strategy_research_boundary_health,
)
from stark_terminal_core.strategy_research_workspace_boundary.invariants import (
    evaluate_strategy_research_boundary_invariants,
)
from stark_terminal_core.strategy_research_workspace_boundary.modules import (
    default_strategy_research_module_boundary_policies,
)

router = APIRouter()


def _public_forbidden_behavior_label(kind_value: str) -> str:
    if kind_value == "SECRET_OR_CREDENTIAL":
        return "SENSITIVE_MATERIAL"
    return kind_value


@router.get("/strategy-research-workspace-boundary/health")
def strategy_research_workspace_boundary_health() -> dict[str, Any]:
    status = check_strategy_research_boundary_health(get_settings())
    return {
        "service": "stark-terminal-strategy-research-workspace-boundary",
        **status.model_dump(),
    }


@router.get("/strategy-research-workspace-boundary/contracts")
def strategy_research_workspace_boundary_contracts() -> dict[str, Any]:
    settings = get_settings()
    registry = default_strategy_research_forbidden_behavior_registry()
    endpoint_policies = default_strategy_research_endpoint_boundary_policies()
    module_policies = default_strategy_research_module_boundary_policies()
    return {
        "service": "stark-terminal-strategy-research-workspace-boundary",
        "schema_version": settings.strategy_research_workspace_boundary_schema_version,
        "computation_scope": "boundary-hardening-only",
        "boundary_hardening_only": True,
        "forbidden_behaviors": [
            _public_forbidden_behavior_label(behavior.kind.value)
            for behavior in registry.behaviors
        ],
        "endpoint_families": [policy.endpoint_family for policy in endpoint_policies],
        "module_families": [policy.module_family for policy in module_policies],
        "active_ui_allowed_now": False,
        "frontend_components_allowed_now": False,
        "desktop_components_allowed_now": False,
        "paper_ingestion_allowed_now": False,
        "paper_parsing_allowed_now": False,
        "strategy_generation_allowed_now": False,
        "strategy_code_generation_allowed_now": False,
        "backtesting_allowed_now": False,
        "optimization_allowed_now": False,
        "recommendations_allowed_now": False,
        "action_generation_allowed_now": False,
        "confidence_scoring_allowed_now": False,
        "decision_object_generation_allowed_now": False,
        "readiness_to_trade_allowed_now": False,
        "broker_controls_allowed_now": False,
        "execution_allowed_now": False,
        "approval_allowed_now": False,
        "override_allowed_now": False,
    }


@router.get("/strategy-research-workspace-boundary/invariants")
def strategy_research_workspace_boundary_invariants() -> dict[str, Any]:
    result = evaluate_strategy_research_boundary_invariants()
    return {
        "service": "stark-terminal-strategy-research-workspace-boundary",
        "computation_scope": "boundary-hardening-only",
        "boundary_hardening_only": True,
        "invariant_result": result.model_dump(mode="json"),
        "blockers": list(result.blockers),
        "warnings": list(result.warnings),
        "no_active_ui": True,
        "no_frontend_components": True,
        "no_desktop_components": True,
        "no_paper_ingestion": True,
        "no_paper_parsing": True,
        "no_strategy_generation": True,
        "no_strategy_code_generation": True,
        "no_backtesting": True,
        "no_optimization": True,
        "no_recommendations": True,
        "no_action_generation": True,
        "no_confidence_scoring": True,
        "no_decision_object": True,
        "no_readiness_to_trade": True,
        "no_broker_controls": True,
        "no_approval": True,
        "no_override": True,
        "no_execution": True,
        "active_ui_generated": False,
        "frontend_component_generated": False,
        "desktop_component_generated": False,
        "paper_ingested": False,
        "paper_parsed": False,
        "strategy_generated": False,
        "strategy_code_generated": False,
        "backtest_generated": False,
        "optimization_generated": False,
        "recommendation_generated": False,
        "action_generated": False,
        "confidence_generated": False,
        "decision_object_generated": False,
        "readiness_to_trade_generated": False,
        "broker_control_enabled": False,
        "approval_granted": False,
        "override_granted": False,
        "execution_ready": False,
    }
