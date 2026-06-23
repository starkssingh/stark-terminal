from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings


class DecisionEvidenceValidationHealthStatus(BaseModel):
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
    readiness_to_trade_allowed: bool
    validation_only: bool = True
    status: str
    error: str | None = None


def check_decision_evidence_validation_health(
    settings: Settings | None = None,
) -> DecisionEvidenceValidationHealthStatus:
    resolved = settings or get_settings()
    unsafe_flags = (
        resolved.decision_evidence_validation_allow_recommendations
        or resolved.decision_evidence_validation_allow_action_generation
        or resolved.decision_evidence_validation_allow_confidence_scoring
        or resolved.decision_evidence_validation_allow_decision_object_generation
        or resolved.decision_evidence_validation_allow_execution
        or resolved.decision_evidence_validation_allow_approval
        or resolved.decision_evidence_validation_allow_override
        or resolved.decision_evidence_validation_allow_readiness_to_trade
        or resolved.execution_apis_enabled
    )
    has_required_configuration = (
        bool(resolved.decision_evidence_validation_schema_version.strip())
        and resolved.decision_evidence_validation_stage == "validation_v0"
    )
    status = (
        "healthy"
        if resolved.decision_evidence_validation_enabled and not unsafe_flags and has_required_configuration
        else "blocked"
    )
    error = None if status == "healthy" else "Decision evidence validation flags are not fail-closed"
    return DecisionEvidenceValidationHealthStatus(
        enabled=resolved.decision_evidence_validation_enabled,
        schema_version=resolved.decision_evidence_validation_schema_version,
        stage=resolved.decision_evidence_validation_stage,
        recommendations_allowed=resolved.decision_evidence_validation_allow_recommendations,
        action_generation_allowed=resolved.decision_evidence_validation_allow_action_generation,
        confidence_scoring_allowed=resolved.decision_evidence_validation_allow_confidence_scoring,
        decision_object_generation_allowed=resolved.decision_evidence_validation_allow_decision_object_generation,
        execution_allowed=False,
        approval_allowed=resolved.decision_evidence_validation_allow_approval,
        override_allowed=resolved.decision_evidence_validation_allow_override,
        readiness_to_trade_allowed=resolved.decision_evidence_validation_allow_readiness_to_trade,
        validation_only=True,
        status=status,
        error=error,
    )

