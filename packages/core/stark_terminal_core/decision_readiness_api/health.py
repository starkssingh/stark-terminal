from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings


class DecisionReadinessAPIHealthStatus(BaseModel):
    enabled: bool
    schema_version: str
    stage: str
    recommendations_allowed: bool
    action_generation_allowed: bool
    confidence_scoring_allowed: bool
    decision_object_generation_allowed: bool
    execution_allowed: bool = False
    approval_allowed: bool
    override_allowed: bool
    returns_unavailable_by_default: bool
    readiness_status_generation_allowed: bool
    status: str
    error: str | None = None


def check_decision_readiness_api_health(settings: Settings | None = None) -> DecisionReadinessAPIHealthStatus:
    resolved = settings or get_settings()
    unsafe_flags = (
        resolved.decision_readiness_api_allow_recommendations
        or resolved.decision_readiness_api_allow_action_generation
        or resolved.decision_readiness_api_allow_confidence_scoring
        or resolved.decision_readiness_api_allow_decision_object_generation
        or resolved.decision_readiness_api_allow_execution
        or resolved.decision_readiness_api_allow_approval
        or resolved.decision_readiness_api_allow_override
        or resolved.execution_apis_enabled
    )
    has_required_configuration = (
        bool(resolved.decision_readiness_api_schema_version.strip())
        and resolved.decision_readiness_api_stage == "readiness_contract_skeleton"
        and resolved.decision_readiness_api_return_unavailable_by_default
    )
    status = (
        "healthy"
        if resolved.decision_readiness_api_enabled and not unsafe_flags and has_required_configuration
        else "blocked"
    )
    error = None if status == "healthy" else "Decision Readiness API skeleton flags are not fail-closed"
    return DecisionReadinessAPIHealthStatus(
        enabled=resolved.decision_readiness_api_enabled,
        schema_version=resolved.decision_readiness_api_schema_version,
        stage=resolved.decision_readiness_api_stage,
        recommendations_allowed=resolved.decision_readiness_api_allow_recommendations,
        action_generation_allowed=resolved.decision_readiness_api_allow_action_generation,
        confidence_scoring_allowed=resolved.decision_readiness_api_allow_confidence_scoring,
        decision_object_generation_allowed=resolved.decision_readiness_api_allow_decision_object_generation,
        execution_allowed=False,
        approval_allowed=resolved.decision_readiness_api_allow_approval,
        override_allowed=resolved.decision_readiness_api_allow_override,
        returns_unavailable_by_default=resolved.decision_readiness_api_return_unavailable_by_default,
        readiness_status_generation_allowed=False,
        status=status,
        error=error,
    )
