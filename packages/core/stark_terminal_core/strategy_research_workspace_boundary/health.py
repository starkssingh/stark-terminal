from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.strategy_research_workspace_boundary.endpoints import (
    default_strategy_research_endpoint_boundary_policies,
)
from stark_terminal_core.strategy_research_workspace_boundary.forbidden import (
    default_strategy_research_forbidden_behavior_registry,
)
from stark_terminal_core.strategy_research_workspace_boundary.invariants import (
    evaluate_strategy_research_boundary_invariants,
)
from stark_terminal_core.strategy_research_workspace_boundary.modules import (
    default_strategy_research_module_boundary_policies,
)


class StrategyResearchBoundaryHealthStatus(BaseModel):
    enabled: bool
    schema_version: str
    stage: str
    forbidden_behavior_count: int
    endpoint_policy_count: int
    module_policy_count: int
    invariant_passed: bool
    active_ui_allowed: bool
    frontend_components_allowed: bool
    desktop_components_allowed: bool
    paper_ingestion_allowed: bool
    paper_parsing_allowed: bool
    strategy_generation_allowed: bool
    strategy_code_generation_allowed: bool
    backtesting_allowed: bool
    optimization_allowed: bool
    recommendations_allowed: bool
    action_generation_allowed: bool
    confidence_scoring_allowed: bool
    decision_object_generation_allowed: bool
    readiness_to_trade_allowed: bool
    broker_controls_allowed: bool
    execution_allowed: bool = False
    approval_allowed: bool
    override_allowed: bool
    status: str
    error: str | None = None


def check_strategy_research_boundary_health(
    settings: Settings | None = None,
) -> StrategyResearchBoundaryHealthStatus:
    resolved = settings or get_settings()
    registry = default_strategy_research_forbidden_behavior_registry()
    endpoint_policies = default_strategy_research_endpoint_boundary_policies()
    module_policies = default_strategy_research_module_boundary_policies()
    invariant = evaluate_strategy_research_boundary_invariants(
        endpoint_policies,
        module_policies,
        registry,
    )
    unsafe_flags: dict[str, Any] = {
        "active_ui_allowed": resolved.strategy_research_workspace_boundary_allow_active_ui,
        "frontend_components_allowed": (
            resolved.strategy_research_workspace_boundary_allow_frontend_components
        ),
        "desktop_components_allowed": resolved.strategy_research_workspace_boundary_allow_desktop_components,
        "paper_ingestion_allowed": resolved.strategy_research_workspace_boundary_allow_paper_ingestion,
        "paper_parsing_allowed": resolved.strategy_research_workspace_boundary_allow_paper_parsing,
        "strategy_generation_allowed": (
            resolved.strategy_research_workspace_boundary_allow_strategy_generation
        ),
        "strategy_code_generation_allowed": (
            resolved.strategy_research_workspace_boundary_allow_strategy_code_generation
        ),
        "backtesting_allowed": resolved.strategy_research_workspace_boundary_allow_backtesting,
        "optimization_allowed": resolved.strategy_research_workspace_boundary_allow_optimization,
        "recommendations_allowed": resolved.strategy_research_workspace_boundary_allow_recommendations,
        "action_generation_allowed": resolved.strategy_research_workspace_boundary_allow_action_generation,
        "confidence_scoring_allowed": (
            resolved.strategy_research_workspace_boundary_allow_confidence_scoring
        ),
        "decision_object_generation_allowed": (
            resolved.strategy_research_workspace_boundary_allow_decision_object_generation
        ),
        "readiness_to_trade_allowed": (
            resolved.strategy_research_workspace_boundary_allow_readiness_to_trade
        ),
        "broker_controls_allowed": resolved.strategy_research_workspace_boundary_allow_broker_controls,
        "execution_allowed": (
            resolved.strategy_research_workspace_boundary_allow_execution
            or resolved.execution_apis_enabled
        ),
        "approval_allowed": resolved.strategy_research_workspace_boundary_allow_approval,
        "override_allowed": resolved.strategy_research_workspace_boundary_allow_override,
    }
    error: str | None = None
    if any(bool(value) for value in unsafe_flags.values()):
        error = "strategy research workspace boundary unsafe flags must remain false"
    elif not resolved.strategy_research_workspace_boundary_schema_version.strip():
        error = "strategy research workspace boundary schema version cannot be empty"
    elif resolved.strategy_research_workspace_boundary_stage != "boundary_hardening":
        error = "strategy research workspace boundary stage must remain boundary_hardening"
    elif not invariant.passed:
        error = "strategy research workspace boundary invariants must pass"
    elif not registry.behaviors or not endpoint_policies or not module_policies:
        error = "strategy research workspace boundary registries and policies are required"
    return StrategyResearchBoundaryHealthStatus(
        enabled=resolved.strategy_research_workspace_boundary_enabled,
        schema_version=resolved.strategy_research_workspace_boundary_schema_version,
        stage=resolved.strategy_research_workspace_boundary_stage,
        forbidden_behavior_count=len(registry.behaviors),
        endpoint_policy_count=len(endpoint_policies),
        module_policy_count=len(module_policies),
        invariant_passed=invariant.passed,
        active_ui_allowed=resolved.strategy_research_workspace_boundary_allow_active_ui,
        frontend_components_allowed=(
            resolved.strategy_research_workspace_boundary_allow_frontend_components
        ),
        desktop_components_allowed=resolved.strategy_research_workspace_boundary_allow_desktop_components,
        paper_ingestion_allowed=resolved.strategy_research_workspace_boundary_allow_paper_ingestion,
        paper_parsing_allowed=resolved.strategy_research_workspace_boundary_allow_paper_parsing,
        strategy_generation_allowed=(
            resolved.strategy_research_workspace_boundary_allow_strategy_generation
        ),
        strategy_code_generation_allowed=(
            resolved.strategy_research_workspace_boundary_allow_strategy_code_generation
        ),
        backtesting_allowed=resolved.strategy_research_workspace_boundary_allow_backtesting,
        optimization_allowed=resolved.strategy_research_workspace_boundary_allow_optimization,
        recommendations_allowed=resolved.strategy_research_workspace_boundary_allow_recommendations,
        action_generation_allowed=resolved.strategy_research_workspace_boundary_allow_action_generation,
        confidence_scoring_allowed=(
            resolved.strategy_research_workspace_boundary_allow_confidence_scoring
        ),
        decision_object_generation_allowed=(
            resolved.strategy_research_workspace_boundary_allow_decision_object_generation
        ),
        readiness_to_trade_allowed=resolved.strategy_research_workspace_boundary_allow_readiness_to_trade,
        broker_controls_allowed=resolved.strategy_research_workspace_boundary_allow_broker_controls,
        execution_allowed=False,
        approval_allowed=resolved.strategy_research_workspace_boundary_allow_approval,
        override_allowed=resolved.strategy_research_workspace_boundary_allow_override,
        status="healthy" if error is None else "blocked",
        error=error,
    )
