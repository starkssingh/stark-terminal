from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator


class DecisionHumanReviewStage(StrEnum):
    WORKFLOW_SKELETON = "WORKFLOW_SKELETON"
    UNAVAILABLE_ONLY = "UNAVAILABLE_ONLY"
    TASK_PLACEHOLDERS = "TASK_PLACEHOLDERS"
    QUEUE_PLACEHOLDERS = "QUEUE_PLACEHOLDERS"
    ACTIVE_WORKFLOW_PLANNED = "ACTIVE_WORKFLOW_PLANNED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class DecisionReviewTaskKind(StrEnum):
    EVIDENCE_REVIEW = "EVIDENCE_REVIEW"
    SAFETY_REVIEW = "SAFETY_REVIEW"
    VALIDATION_REVIEW = "VALIDATION_REVIEW"
    DISPLAY_REVIEW = "DISPLAY_REVIEW"
    FINAL_REVIEW_PLACEHOLDER = "FINAL_REVIEW_PLACEHOLDER"
    UNKNOWN = "UNKNOWN"


class DecisionReviewerRoleKind(StrEnum):
    HUMAN_OPERATOR = "HUMAN_OPERATOR"
    RISK_REVIEWER = "RISK_REVIEWER"
    COMPLIANCE_REVIEWER = "COMPLIANCE_REVIEWER"
    RESEARCH_REVIEWER = "RESEARCH_REVIEWER"
    ADMIN_PLACEHOLDER = "ADMIN_PLACEHOLDER"
    UNKNOWN = "UNKNOWN"


class DecisionReviewQueueKind(StrEnum):
    PLACEHOLDER_QUEUE = "PLACEHOLDER_QUEUE"
    EVIDENCE_QUEUE = "EVIDENCE_QUEUE"
    SAFETY_QUEUE = "SAFETY_QUEUE"
    VALIDATION_QUEUE = "VALIDATION_QUEUE"
    BLOCKED_QUEUE = "BLOCKED_QUEUE"
    UNKNOWN = "UNKNOWN"


class DecisionReviewStatusKind(StrEnum):
    PLACEHOLDER_ONLY = "PLACEHOLDER_ONLY"
    UNAVAILABLE = "UNAVAILABLE"
    NOT_STARTED = "NOT_STARTED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class DecisionHumanReviewSafetyLabel(StrEnum):
    WORKFLOW_SKELETON_ONLY = "WORKFLOW_SKELETON_ONLY"
    NOT_APPROVAL = "NOT_APPROVAL"
    NOT_A_RECOMMENDATION = "NOT_A_RECOMMENDATION"
    NOT_READINESS_TO_TRADE = "NOT_READINESS_TO_TRADE"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _utc_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _non_empty_text(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} cannot be empty")
    return normalized


def sanitize_decision_human_review_notes(values: list[str]) -> list[str]:
    sanitized: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized:
            sanitized.append(normalized)
    return sanitized


class DecisionHumanReviewWorkflowContract(BaseModel):
    workflow_id: str
    name: str
    stage: DecisionHumanReviewStage = DecisionHumanReviewStage.WORKFLOW_SKELETON
    task_kinds: list[DecisionReviewTaskKind]
    reviewer_roles: list[DecisionReviewerRoleKind]
    queue_kinds: list[DecisionReviewQueueKind]
    active_workflow: bool = False
    task_assignment_allowed: bool = False
    reviewer_auth_allowed: bool = False
    notifications_allowed: bool = False
    approval_allowed: bool = False
    override_allowed: bool = False
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    readiness_to_trade_allowed: bool = False
    execution_allowed: bool = False
    returns_unavailable_by_default: bool = True
    forbidden_outputs: list[str]
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("workflow_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision human review workflow text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_human_review_notes(value)

    @model_validator(mode="after")
    def workflow_contract_must_fail_closed(self) -> DecisionHumanReviewWorkflowContract:
        if self.stage == DecisionHumanReviewStage.UNKNOWN:
            raise ValueError("UNKNOWN Decision Human Review stage is not allowed")
        if not self.task_kinds:
            raise ValueError("decision human review workflow requires task kinds")
        if DecisionReviewTaskKind.UNKNOWN in self.task_kinds:
            raise ValueError("UNKNOWN review task kind is not allowed")
        if not self.reviewer_roles:
            raise ValueError("decision human review workflow requires reviewer roles")
        if DecisionReviewerRoleKind.UNKNOWN in self.reviewer_roles:
            raise ValueError("UNKNOWN reviewer role kind is not allowed")
        if not self.queue_kinds:
            raise ValueError("decision human review workflow requires queue kinds")
        if DecisionReviewQueueKind.UNKNOWN in self.queue_kinds:
            raise ValueError("UNKNOWN review queue kind is not allowed")
        if self.active_workflow:
            raise ValueError("active workflows are forbidden in Prompt 45")
        if self.task_assignment_allowed:
            raise ValueError("task assignment is forbidden in Prompt 45")
        if self.reviewer_auth_allowed:
            raise ValueError("reviewer auth is forbidden in Prompt 45")
        if self.notifications_allowed:
            raise ValueError("notifications are forbidden in Prompt 45")
        if self.approval_allowed:
            raise ValueError("approval is forbidden in Prompt 45")
        if self.override_allowed:
            raise ValueError("override is forbidden in Prompt 45")
        if self.recommendations_allowed:
            raise ValueError("recommendations are forbidden in Prompt 45")
        if self.action_generation_allowed:
            raise ValueError("action generation is forbidden in Prompt 45")
        if self.confidence_scoring_allowed:
            raise ValueError("confidence scoring is forbidden in Prompt 45")
        if self.decision_object_generation_allowed:
            raise ValueError("DecisionObject generation is forbidden in Prompt 45")
        if self.readiness_to_trade_allowed:
            raise ValueError("readiness-to-trade is forbidden in Prompt 45")
        if self.execution_allowed:
            raise ValueError("execution is forbidden in Prompt 45")
        if not self.returns_unavailable_by_default:
            raise ValueError("decision human review workflow must return unavailable by default")
        required_terms = [
            "active workflow",
            "task assignment",
            "reviewer auth",
            "notifications",
            "approval",
            "override",
            "recommendation",
            "action",
            "confidence",
            "decisionobject",
            "readiness-to-trade",
            "execution",
        ]
        normalized_outputs = " ".join(self.forbidden_outputs).lower()
        missing = [term for term in required_terms if term not in normalized_outputs]
        if missing:
            raise ValueError(f"forbidden outputs missing required concepts: {', '.join(missing)}")
        return self


def default_decision_human_review_workflow_contract() -> DecisionHumanReviewWorkflowContract:
    return DecisionHumanReviewWorkflowContract(
        workflow_id="decision-human-review-workflow-contract-v1",
        name="Decision Human Review Workflow Skeleton",
        task_kinds=[
            DecisionReviewTaskKind.EVIDENCE_REVIEW,
            DecisionReviewTaskKind.SAFETY_REVIEW,
            DecisionReviewTaskKind.VALIDATION_REVIEW,
            DecisionReviewTaskKind.DISPLAY_REVIEW,
            DecisionReviewTaskKind.FINAL_REVIEW_PLACEHOLDER,
        ],
        reviewer_roles=[
            DecisionReviewerRoleKind.HUMAN_OPERATOR,
            DecisionReviewerRoleKind.RISK_REVIEWER,
            DecisionReviewerRoleKind.COMPLIANCE_REVIEWER,
            DecisionReviewerRoleKind.RESEARCH_REVIEWER,
            DecisionReviewerRoleKind.ADMIN_PLACEHOLDER,
        ],
        queue_kinds=[
            DecisionReviewQueueKind.PLACEHOLDER_QUEUE,
            DecisionReviewQueueKind.EVIDENCE_QUEUE,
            DecisionReviewQueueKind.SAFETY_QUEUE,
            DecisionReviewQueueKind.VALIDATION_QUEUE,
            DecisionReviewQueueKind.BLOCKED_QUEUE,
        ],
        forbidden_outputs=[
            "active workflow",
            "task assignment",
            "reviewer auth",
            "notifications",
            "approval_workflow",
            "override_workflow",
            "recommendation_generation",
            "action_generation",
            "confidence_scoring",
            "DecisionObject_generation",
            "readiness-to-trade",
            "execution_apis",
            "broker_behavior",
        ],
        notes=[
            "Prompt 45 defines workflow contracts only.",
            "Human review placeholders do not grant approval, override, readiness-to-trade, or execution.",
        ],
    )
