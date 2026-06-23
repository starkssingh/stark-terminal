from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.decision_human_review.queues import default_decision_review_queue_placeholders
from stark_terminal_core.decision_human_review.roles import default_decision_reviewer_role_placeholders
from stark_terminal_core.decision_human_review.tasks import default_decision_review_task_placeholders


class DecisionHumanReviewHealthStatus(BaseModel):
    enabled: bool
    schema_version: str
    stage: str
    active_workflow_allowed: bool
    task_assignment_allowed: bool
    reviewer_auth_allowed: bool
    notifications_allowed: bool
    approval_allowed: bool
    override_allowed: bool
    recommendations_allowed: bool
    action_generation_allowed: bool
    confidence_scoring_allowed: bool
    decision_object_generation_allowed: bool
    readiness_to_trade_allowed: bool
    execution_allowed: bool = False
    returns_unavailable_by_default: bool
    default_task_count: int
    default_role_count: int
    default_queue_count: int
    status: str
    error: str | None = None


def check_decision_human_review_health(settings: Settings | None = None) -> DecisionHumanReviewHealthStatus:
    resolved_settings = settings or get_settings()
    default_task_count = len(default_decision_review_task_placeholders())
    default_role_count = len(default_decision_reviewer_role_placeholders())
    default_queue_count = len(default_decision_review_queue_placeholders())
    unsafe_flags: dict[str, Any] = {
        "active_workflow_allowed": resolved_settings.decision_human_review_allow_active_workflow,
        "task_assignment_allowed": resolved_settings.decision_human_review_allow_task_assignment,
        "reviewer_auth_allowed": resolved_settings.decision_human_review_allow_reviewer_auth,
        "notifications_allowed": resolved_settings.decision_human_review_allow_notifications,
        "approval_allowed": resolved_settings.decision_human_review_allow_approval,
        "override_allowed": resolved_settings.decision_human_review_allow_override,
        "recommendations_allowed": resolved_settings.decision_human_review_allow_recommendations,
        "action_generation_allowed": resolved_settings.decision_human_review_allow_action_generation,
        "confidence_scoring_allowed": resolved_settings.decision_human_review_allow_confidence_scoring,
        "decision_object_generation_allowed": resolved_settings.decision_human_review_allow_decision_object_generation,
        "readiness_to_trade_allowed": resolved_settings.decision_human_review_allow_readiness_to_trade,
        "execution_allowed": resolved_settings.decision_human_review_allow_execution,
    }
    error: str | None = None
    if any(bool(value) for value in unsafe_flags.values()):
        error = "decision human review unsafe flags must remain false"
    elif not resolved_settings.decision_human_review_return_unavailable_by_default:
        error = "decision human review must return unavailable by default"
    elif not resolved_settings.decision_human_review_schema_version:
        error = "decision human review schema version cannot be empty"
    elif default_task_count == 0 or default_role_count == 0 or default_queue_count == 0:
        error = "decision human review default placeholders are required"
    return DecisionHumanReviewHealthStatus(
        enabled=resolved_settings.decision_human_review_enabled,
        schema_version=resolved_settings.decision_human_review_schema_version,
        stage=resolved_settings.decision_human_review_stage,
        active_workflow_allowed=resolved_settings.decision_human_review_allow_active_workflow,
        task_assignment_allowed=resolved_settings.decision_human_review_allow_task_assignment,
        reviewer_auth_allowed=resolved_settings.decision_human_review_allow_reviewer_auth,
        notifications_allowed=resolved_settings.decision_human_review_allow_notifications,
        approval_allowed=resolved_settings.decision_human_review_allow_approval,
        override_allowed=resolved_settings.decision_human_review_allow_override,
        recommendations_allowed=resolved_settings.decision_human_review_allow_recommendations,
        action_generation_allowed=resolved_settings.decision_human_review_allow_action_generation,
        confidence_scoring_allowed=resolved_settings.decision_human_review_allow_confidence_scoring,
        decision_object_generation_allowed=resolved_settings.decision_human_review_allow_decision_object_generation,
        readiness_to_trade_allowed=resolved_settings.decision_human_review_allow_readiness_to_trade,
        execution_allowed=False,
        returns_unavailable_by_default=resolved_settings.decision_human_review_return_unavailable_by_default,
        default_task_count=default_task_count,
        default_role_count=default_role_count,
        default_queue_count=default_queue_count,
        status="healthy" if error is None else "blocked",
        error=error,
    )
