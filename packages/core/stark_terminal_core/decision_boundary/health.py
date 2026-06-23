from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.decision_boundary.endpoints import default_decision_endpoint_boundary_policies
from stark_terminal_core.decision_boundary.forbidden import default_decision_forbidden_behavior_registry
from stark_terminal_core.decision_boundary.invariants import evaluate_decision_boundary_invariants
from stark_terminal_core.decision_boundary.modules import default_decision_module_boundary_policies


class DecisionBoundaryHealthStatus(BaseModel):
    enabled: bool
    schema_version: str
    stage: str
    forbidden_behavior_count: int
    endpoint_policy_count: int
    module_policy_count: int
    invariant_passed: bool
    recommendations_allowed: bool
    action_generation_allowed: bool
    confidence_scoring_allowed: bool
    decision_object_generation_allowed: bool
    execution_allowed: bool = False
    approval_allowed: bool
    override_allowed: bool
    active_ui_allowed: bool
    active_workflow_allowed: bool
    readiness_to_trade_allowed: bool
    status: str
    error: str | None = None


def check_decision_boundary_health(settings: Settings | None = None) -> DecisionBoundaryHealthStatus:
    resolved_settings = settings or get_settings()
    registry = default_decision_forbidden_behavior_registry()
    endpoint_policies = default_decision_endpoint_boundary_policies()
    module_policies = default_decision_module_boundary_policies()
    invariant = evaluate_decision_boundary_invariants(endpoint_policies, module_policies, registry)
    unsafe_flags: dict[str, Any] = {
        "recommendations_allowed": resolved_settings.decision_boundary_allow_recommendations,
        "action_generation_allowed": resolved_settings.decision_boundary_allow_action_generation,
        "confidence_scoring_allowed": resolved_settings.decision_boundary_allow_confidence_scoring,
        "decision_object_generation_allowed": resolved_settings.decision_boundary_allow_decision_object_generation,
        "execution_allowed": resolved_settings.decision_boundary_allow_execution,
        "approval_allowed": resolved_settings.decision_boundary_allow_approval,
        "override_allowed": resolved_settings.decision_boundary_allow_override,
        "active_ui_allowed": resolved_settings.decision_boundary_allow_active_ui,
        "active_workflow_allowed": resolved_settings.decision_boundary_allow_active_workflow,
        "readiness_to_trade_allowed": resolved_settings.decision_boundary_allow_readiness_to_trade,
    }
    error: str | None = None
    if any(bool(value) for value in unsafe_flags.values()):
        error = "decision boundary unsafe flags must remain false"
    elif not resolved_settings.decision_boundary_schema_version:
        error = "decision boundary schema version cannot be empty"
    elif not invariant.passed:
        error = "decision boundary invariants must pass"
    elif not registry.behaviors or not endpoint_policies or not module_policies:
        error = "decision boundary default registries and policies are required"
    return DecisionBoundaryHealthStatus(
        enabled=resolved_settings.decision_boundary_enabled,
        schema_version=resolved_settings.decision_boundary_schema_version,
        stage=resolved_settings.decision_boundary_stage,
        forbidden_behavior_count=len(registry.behaviors),
        endpoint_policy_count=len(endpoint_policies),
        module_policy_count=len(module_policies),
        invariant_passed=invariant.passed,
        recommendations_allowed=resolved_settings.decision_boundary_allow_recommendations,
        action_generation_allowed=resolved_settings.decision_boundary_allow_action_generation,
        confidence_scoring_allowed=resolved_settings.decision_boundary_allow_confidence_scoring,
        decision_object_generation_allowed=resolved_settings.decision_boundary_allow_decision_object_generation,
        execution_allowed=False,
        approval_allowed=resolved_settings.decision_boundary_allow_approval,
        override_allowed=resolved_settings.decision_boundary_allow_override,
        active_ui_allowed=resolved_settings.decision_boundary_allow_active_ui,
        active_workflow_allowed=resolved_settings.decision_boundary_allow_active_workflow,
        readiness_to_trade_allowed=resolved_settings.decision_boundary_allow_readiness_to_trade,
        status="healthy" if error is None else "blocked",
        error=error,
    )
