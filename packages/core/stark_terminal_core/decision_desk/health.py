from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.decision_desk.action_placeholders import default_retail_action_placeholder_contracts
from stark_terminal_core.decision_desk.planning import default_retail_decision_desk_plan


class RetailDecisionDeskHealthStatus(BaseModel):
    enabled: bool
    schema_version: str
    planning_stage: str
    real_data_allowed: bool
    recommendations_allowed: bool
    action_generation_allowed: bool
    confidence_scoring_allowed: bool
    decision_objects_allowed: bool
    execution_allowed: bool = False
    evidence_required: bool
    human_review_required: bool
    planned_action_placeholder_count: int
    status: str
    error: str | None = None


def check_retail_decision_desk_health(settings: Settings | None = None) -> RetailDecisionDeskHealthStatus:
    resolved = settings or get_settings()
    plan = default_retail_decision_desk_plan()
    placeholders = default_retail_action_placeholder_contracts()
    unsafe_flags = (
        resolved.retail_decision_desk_allow_real_data
        or resolved.retail_decision_desk_allow_recommendations
        or resolved.retail_decision_desk_allow_action_generation
        or resolved.retail_decision_desk_allow_confidence_scoring
        or resolved.retail_decision_desk_allow_decision_objects
        or resolved.retail_decision_desk_allow_execution
        or resolved.execution_apis_enabled
    )
    has_required_configuration = (
        bool(resolved.retail_decision_desk_schema_version.strip())
        and resolved.retail_decision_desk_planning_stage == "planning_only"
        and resolved.retail_decision_desk_require_evidence
        and resolved.retail_decision_desk_require_human_review
        and bool(plan.planned_action_placeholders)
        and bool(placeholders)
    )
    status = "healthy" if resolved.retail_decision_desk_enabled and not unsafe_flags and has_required_configuration else "blocked"
    error = None if status == "healthy" else "Retail Decision Desk planning safety flags are not fail-closed"
    return RetailDecisionDeskHealthStatus(
        enabled=resolved.retail_decision_desk_enabled,
        schema_version=resolved.retail_decision_desk_schema_version,
        planning_stage=resolved.retail_decision_desk_planning_stage,
        real_data_allowed=resolved.retail_decision_desk_allow_real_data,
        recommendations_allowed=resolved.retail_decision_desk_allow_recommendations,
        action_generation_allowed=resolved.retail_decision_desk_allow_action_generation,
        confidence_scoring_allowed=resolved.retail_decision_desk_allow_confidence_scoring,
        decision_objects_allowed=resolved.retail_decision_desk_allow_decision_objects,
        execution_allowed=False,
        evidence_required=resolved.retail_decision_desk_require_evidence,
        human_review_required=resolved.retail_decision_desk_require_human_review,
        planned_action_placeholder_count=len(placeholders),
        status=status,
        error=error,
    )
