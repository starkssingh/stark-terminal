from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.decision_safety.guardrails import default_decision_safety_guardrails


class DecisionSafetyHealthStatus(BaseModel):
    enabled: bool
    schema_version: str
    stage: str
    recommendations_allowed: bool
    action_generation_allowed: bool
    confidence_scoring_allowed: bool
    decision_object_generation_allowed: bool
    execution_allowed: bool = False
    human_approval_allowed: bool
    overrides_allowed: bool
    human_review_required: bool
    blocked_output_policy_required: bool
    default_guardrail_count: int
    status: str
    error: str | None = None


def check_decision_safety_health(settings: Settings | None = None) -> DecisionSafetyHealthStatus:
    resolved = settings or get_settings()
    guardrails = default_decision_safety_guardrails()
    unsafe_flags = (
        resolved.decision_safety_allow_recommendations
        or resolved.decision_safety_allow_action_generation
        or resolved.decision_safety_allow_confidence_scoring
        or resolved.decision_safety_allow_decision_object_generation
        or resolved.decision_safety_allow_execution
        or resolved.decision_safety_allow_human_approval
        or resolved.decision_safety_allow_overrides
        or resolved.execution_apis_enabled
    )
    has_required_configuration = (
        bool(resolved.decision_safety_schema_version.strip())
        and resolved.decision_safety_stage == "guardrails_only"
        and resolved.decision_safety_require_human_review
        and resolved.decision_safety_require_blocked_output_policy
        and bool(guardrails)
    )
    status = "healthy" if resolved.decision_safety_enabled and not unsafe_flags and has_required_configuration else "blocked"
    error = None if status == "healthy" else "Decision safety flags are not fail-closed"
    return DecisionSafetyHealthStatus(
        enabled=resolved.decision_safety_enabled,
        schema_version=resolved.decision_safety_schema_version,
        stage=resolved.decision_safety_stage,
        recommendations_allowed=resolved.decision_safety_allow_recommendations,
        action_generation_allowed=resolved.decision_safety_allow_action_generation,
        confidence_scoring_allowed=resolved.decision_safety_allow_confidence_scoring,
        decision_object_generation_allowed=resolved.decision_safety_allow_decision_object_generation,
        execution_allowed=False,
        human_approval_allowed=resolved.decision_safety_allow_human_approval,
        overrides_allowed=resolved.decision_safety_allow_overrides,
        human_review_required=resolved.decision_safety_require_human_review,
        blocked_output_policy_required=resolved.decision_safety_require_blocked_output_policy,
        default_guardrail_count=len(guardrails),
        status=status,
        error=error,
    )
