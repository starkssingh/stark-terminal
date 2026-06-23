from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_human_review.workflow import (
    DecisionReviewerRoleKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_decision_human_review_notes,
)


class DecisionReviewerRolePlaceholder(BaseModel):
    role_id: str
    role_kind: DecisionReviewerRoleKind
    display_name: str
    description: str
    authenticated: bool = False
    active_user_bound: bool = False
    can_approve: bool = False
    can_override: bool = False
    can_generate_recommendations: bool = False
    can_generate_decision_objects: bool = False
    can_execute: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("role_id", "display_name", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision reviewer role text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_human_review_notes(value)

    @model_validator(mode="after")
    def role_placeholder_must_remain_inactive(self) -> DecisionReviewerRolePlaceholder:
        if self.role_kind == DecisionReviewerRoleKind.UNKNOWN:
            raise ValueError("UNKNOWN reviewer role kind is not allowed")
        if self.authenticated:
            raise ValueError("reviewer authentication is forbidden in Prompt 45")
        if self.active_user_bound:
            raise ValueError("active reviewer user binding is forbidden in Prompt 45")
        if self.can_approve:
            raise ValueError("reviewer roles cannot approve in Prompt 45")
        if self.can_override:
            raise ValueError("reviewer roles cannot override in Prompt 45")
        if self.can_generate_recommendations:
            raise ValueError("reviewer roles cannot generate recommendations in Prompt 45")
        if self.can_generate_decision_objects:
            raise ValueError("reviewer roles cannot generate DecisionObjects in Prompt 45")
        if self.can_execute:
            raise ValueError("reviewer roles cannot execute in Prompt 45")
        return self


def default_decision_reviewer_role_placeholders() -> list[DecisionReviewerRolePlaceholder]:
    return [
        DecisionReviewerRolePlaceholder(
            role_id="decision-reviewer-role-human-operator-placeholder",
            role_kind=DecisionReviewerRoleKind.HUMAN_OPERATOR,
            display_name="Human operator placeholder",
            description="Unauthenticated role placeholder for future review workflow planning.",
            notes=["Role is not a user account and grants no approval capability."],
        ),
        DecisionReviewerRolePlaceholder(
            role_id="decision-reviewer-role-risk-placeholder",
            role_kind=DecisionReviewerRoleKind.RISK_REVIEWER,
            display_name="Risk reviewer placeholder",
            description="Unauthenticated role placeholder for future risk review planning.",
            notes=["Risk role cannot override guardrails."],
        ),
        DecisionReviewerRolePlaceholder(
            role_id="decision-reviewer-role-compliance-placeholder",
            role_kind=DecisionReviewerRoleKind.COMPLIANCE_REVIEWER,
            display_name="Compliance reviewer placeholder",
            description="Unauthenticated role placeholder for future compliance review planning.",
            notes=["Compliance role cannot approve or execute."],
        ),
        DecisionReviewerRolePlaceholder(
            role_id="decision-reviewer-role-research-placeholder",
            role_kind=DecisionReviewerRoleKind.RESEARCH_REVIEWER,
            display_name="Research reviewer placeholder",
            description="Unauthenticated role placeholder for future research review planning.",
            notes=["Research role cannot generate recommendations or DecisionObjects."],
        ),
    ]
