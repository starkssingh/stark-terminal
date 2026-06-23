from __future__ import annotations

from datetime import datetime
from typing import Any, Iterable

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_human_review.roles import DecisionReviewerRolePlaceholder
from stark_terminal_core.decision_human_review.tasks import DecisionReviewTaskPlaceholder
from stark_terminal_core.decision_human_review.workflow import (
    DecisionHumanReviewWorkflowContract,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_decision_human_review_notes,
)


class DecisionHumanReviewSafetyPolicy(BaseModel):
    policy_id: str
    name: str
    allow_active_workflow: bool = False
    allow_task_assignment: bool = False
    allow_reviewer_auth: bool = False
    allow_notifications: bool = False
    allow_approval: bool = False
    allow_override: bool = False
    allow_recommendations: bool = False
    allow_action_generation: bool = False
    allow_confidence_scoring: bool = False
    allow_decision_object_generation: bool = False
    allow_readiness_to_trade: bool = False
    allow_execution: bool = False
    require_workflow_skeleton_only: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)

    @field_validator("policy_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision human review safety policy text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_human_review_notes(value)

    @model_validator(mode="after")
    def policy_must_fail_closed(self) -> DecisionHumanReviewSafetyPolicy:
        if self.allow_active_workflow:
            raise ValueError("active workflow is forbidden in Prompt 45")
        if self.allow_task_assignment:
            raise ValueError("task assignment is forbidden in Prompt 45")
        if self.allow_reviewer_auth:
            raise ValueError("reviewer auth is forbidden in Prompt 45")
        if self.allow_notifications:
            raise ValueError("notifications are forbidden in Prompt 45")
        if self.allow_approval:
            raise ValueError("approval is forbidden in Prompt 45")
        if self.allow_override:
            raise ValueError("override is forbidden in Prompt 45")
        if self.allow_recommendations:
            raise ValueError("recommendations are forbidden in Prompt 45")
        if self.allow_action_generation:
            raise ValueError("action generation is forbidden in Prompt 45")
        if self.allow_confidence_scoring:
            raise ValueError("confidence scoring is forbidden in Prompt 45")
        if self.allow_decision_object_generation:
            raise ValueError("DecisionObject generation is forbidden in Prompt 45")
        if self.allow_readiness_to_trade:
            raise ValueError("readiness-to-trade is forbidden in Prompt 45")
        if self.allow_execution:
            raise ValueError("execution is forbidden in Prompt 45")
        if not self.require_workflow_skeleton_only:
            raise ValueError("decision human review must remain workflow-skeleton-only in Prompt 45")
        return self


class DecisionHumanReviewSafetyResult(BaseModel):
    result_id: str
    policy_id: str
    safe: bool
    reasons: list[str]
    workflow_skeleton_only: bool = True
    approval_granted: bool = False
    override_granted: bool = False
    execution_allowed: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("result_id", "policy_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision human review safety result text fields")

    @field_validator("reasons")
    @classmethod
    def reasons_must_be_present(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_decision_human_review_notes(value)
        if not sanitized:
            raise ValueError("decision human review safety reasons cannot be empty")
        return sanitized

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def result_must_remain_non_approval(self) -> DecisionHumanReviewSafetyResult:
        if not self.workflow_skeleton_only:
            raise ValueError("decision human review safety result must remain workflow-skeleton-only")
        if self.approval_granted:
            raise ValueError("decision human review safety result cannot grant approval")
        if self.override_granted:
            raise ValueError("decision human review safety result cannot grant override")
        if self.execution_allowed:
            raise ValueError("decision human review safety result cannot allow execution")
        return self


def default_decision_human_review_safety_policy(settings: Any | None = None) -> DecisionHumanReviewSafetyPolicy:
    notes = ["Prompt 45 permits workflow skeleton contracts only."]
    if settings is not None:
        notes.append(f"stage={settings.decision_human_review_stage}")
    return DecisionHumanReviewSafetyPolicy(
        policy_id="decision-human-review-safety-policy-v1",
        name="Decision Human Review Safety Policy",
        notes=notes,
    )


def _safety_result(result_id: str, policy_id: str, reasons: list[str], safe: bool) -> DecisionHumanReviewSafetyResult:
    return DecisionHumanReviewSafetyResult(
        result_id=result_id,
        policy_id=policy_id,
        safe=safe,
        reasons=reasons,
    )


def evaluate_decision_human_review_workflow_safety(
    workflow: DecisionHumanReviewWorkflowContract,
    policy: DecisionHumanReviewSafetyPolicy,
) -> DecisionHumanReviewSafetyResult:
    reasons: list[str] = []
    if workflow.active_workflow or policy.allow_active_workflow:
        reasons.append("human review workflow cannot be active")
    if workflow.task_assignment_allowed or policy.allow_task_assignment:
        reasons.append("human review workflow cannot assign tasks")
    if workflow.reviewer_auth_allowed or policy.allow_reviewer_auth:
        reasons.append("human review workflow cannot authenticate reviewers")
    if workflow.notifications_allowed or policy.allow_notifications:
        reasons.append("human review workflow cannot send notifications")
    if workflow.approval_allowed or policy.allow_approval:
        reasons.append("human review workflow cannot grant approval")
    if workflow.override_allowed or policy.allow_override:
        reasons.append("human review workflow cannot grant override")
    if workflow.recommendations_allowed or policy.allow_recommendations:
        reasons.append("human review workflow cannot generate recommendations")
    if workflow.action_generation_allowed or policy.allow_action_generation:
        reasons.append("human review workflow cannot generate actions")
    if workflow.confidence_scoring_allowed or policy.allow_confidence_scoring:
        reasons.append("human review workflow cannot score confidence")
    if workflow.decision_object_generation_allowed or policy.allow_decision_object_generation:
        reasons.append("human review workflow cannot generate DecisionObjects")
    if workflow.readiness_to_trade_allowed or policy.allow_readiness_to_trade:
        reasons.append("human review workflow cannot generate readiness-to-trade")
    if workflow.execution_allowed or policy.allow_execution:
        reasons.append("human review workflow cannot allow execution")
    if not workflow.returns_unavailable_by_default:
        reasons.append("human review workflow must return unavailable by default")
    if reasons:
        return _safety_result("decision-human-review-workflow-safety-blocked", policy.policy_id, reasons, False)
    return _safety_result(
        "decision-human-review-workflow-safety-safe",
        policy.policy_id,
        ["workflow remains skeleton-only and no approval, override, recommendation, readiness-to-trade, or execution is allowed"],
        True,
    )


def evaluate_decision_review_tasks_safety(
    tasks: Iterable[DecisionReviewTaskPlaceholder],
    policy: DecisionHumanReviewSafetyPolicy,
) -> DecisionHumanReviewSafetyResult:
    reasons: list[str] = []
    task_list = list(tasks)
    if not task_list:
        reasons.append("human review task placeholders are required")
    for task in task_list:
        if task.assigned or policy.allow_task_assignment:
            reasons.append(f"{task.task_id} cannot be assigned")
        if task.active or task.completed:
            reasons.append(f"{task.task_id} cannot be active or completed")
        if task.approval_granted or policy.allow_approval:
            reasons.append(f"{task.task_id} cannot grant approval")
        if task.override_granted or policy.allow_override:
            reasons.append(f"{task.task_id} cannot grant override")
        if task.recommendation_generated or policy.allow_recommendations:
            reasons.append(f"{task.task_id} cannot generate recommendations")
        if task.action_generated or policy.allow_action_generation:
            reasons.append(f"{task.task_id} cannot generate actions")
        if task.confidence_generated or policy.allow_confidence_scoring:
            reasons.append(f"{task.task_id} cannot generate confidence scores")
        if task.decision_object_generated or policy.allow_decision_object_generation:
            reasons.append(f"{task.task_id} cannot generate DecisionObjects")
        if task.readiness_to_trade_generated or policy.allow_readiness_to_trade:
            reasons.append(f"{task.task_id} cannot generate readiness-to-trade")
        if task.execution_ready or policy.allow_execution:
            reasons.append(f"{task.task_id} cannot mark execution ready")
    if reasons:
        return _safety_result("decision-human-review-task-safety-blocked", policy.policy_id, reasons, False)
    return _safety_result(
        "decision-human-review-task-safety-safe",
        policy.policy_id,
        ["task placeholders remain inactive and non-approval"],
        True,
    )


def evaluate_decision_reviewer_roles_safety(
    roles: Iterable[DecisionReviewerRolePlaceholder],
    policy: DecisionHumanReviewSafetyPolicy,
) -> DecisionHumanReviewSafetyResult:
    reasons: list[str] = []
    role_list = list(roles)
    if not role_list:
        reasons.append("reviewer role placeholders are required")
    for role in role_list:
        if role.authenticated or policy.allow_reviewer_auth:
            reasons.append(f"{role.role_id} cannot authenticate reviewers")
        if role.active_user_bound:
            reasons.append(f"{role.role_id} cannot bind active users")
        if role.can_approve or policy.allow_approval:
            reasons.append(f"{role.role_id} cannot approve")
        if role.can_override or policy.allow_override:
            reasons.append(f"{role.role_id} cannot override")
        if role.can_generate_recommendations or policy.allow_recommendations:
            reasons.append(f"{role.role_id} cannot generate recommendations")
        if role.can_generate_decision_objects or policy.allow_decision_object_generation:
            reasons.append(f"{role.role_id} cannot generate DecisionObjects")
        if role.can_execute or policy.allow_execution:
            reasons.append(f"{role.role_id} cannot execute")
    if reasons:
        return _safety_result("decision-human-review-role-safety-blocked", policy.policy_id, reasons, False)
    return _safety_result(
        "decision-human-review-role-safety-safe",
        policy.policy_id,
        ["reviewer role placeholders remain unauthenticated and non-approval"],
        True,
    )


def reject_review_as_approval(
    reason: str = "human review workflow placeholders cannot be treated as approval in Prompt 45",
) -> DecisionHumanReviewSafetyResult:
    return _safety_result("decision-human-review-reject-approval", "decision-human-review-safety-policy-v1", [reason], False)


def reject_review_as_override(
    reason: str = "human review workflow placeholders cannot be treated as override in Prompt 45",
) -> DecisionHumanReviewSafetyResult:
    return _safety_result("decision-human-review-reject-override", "decision-human-review-safety-policy-v1", [reason], False)


def reject_review_as_recommendation(
    reason: str = "human review workflow placeholders cannot be treated as recommendations in Prompt 45",
) -> DecisionHumanReviewSafetyResult:
    return _safety_result(
        "decision-human-review-reject-recommendation",
        "decision-human-review-safety-policy-v1",
        [reason],
        False,
    )
