from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_desk.action_placeholders import RetailActionPlaceholderContract
from stark_terminal_core.decision_desk.planning import (
    RetailDecisionDeskPlan,
    _non_empty_text,
    sanitize_decision_notes,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _utc_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


class RetailDecisionDeskSafetyPolicy(BaseModel):
    policy_id: str
    name: str
    allow_real_data: bool = False
    allow_recommendations: bool = False
    allow_action_generation: bool = False
    allow_confidence_scoring: bool = False
    allow_decision_objects: bool = False
    allow_execution: bool = False
    require_evidence: bool = True
    require_human_review: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)

    @field_validator("policy_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail decision desk safety policy text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_notes(value)

    @model_validator(mode="after")
    def policy_must_fail_closed(self) -> RetailDecisionDeskSafetyPolicy:
        if self.allow_real_data:
            raise ValueError("real data is forbidden for Retail Decision Desk planning in Prompt 36")
        if self.allow_recommendations:
            raise ValueError("recommendations are forbidden in Prompt 36")
        if self.allow_action_generation:
            raise ValueError("action generation is forbidden in Prompt 36")
        if self.allow_confidence_scoring:
            raise ValueError("confidence scoring is forbidden in Prompt 36")
        if self.allow_decision_objects:
            raise ValueError("DecisionObject generation is forbidden in Prompt 36")
        if self.allow_execution:
            raise ValueError("execution is forbidden in Prompt 36")
        if not self.require_evidence:
            raise ValueError("Decision Desk evidence is required in Prompt 36")
        if not self.require_human_review:
            raise ValueError("human review is required in Prompt 36")
        return self


class RetailDecisionDeskSafetyResult(BaseModel):
    decision: str
    reasons: list[str]
    policy_id: str
    evaluated_at: datetime = Field(default_factory=_utc_now)
    schema_version: str = "v1"

    @field_validator("decision", "policy_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail decision desk safety result text fields")

    @field_validator("reasons")
    @classmethod
    def reasons_must_be_present(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_decision_notes(value)
        if not sanitized:
            raise ValueError("retail decision desk safety result reasons cannot be empty")
        return sanitized

    @field_validator("evaluated_at")
    @classmethod
    def evaluated_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)


def default_retail_decision_desk_safety_policy(settings: Any | None = None) -> RetailDecisionDeskSafetyPolicy:
    notes = ["Prompt 36 permits planning and guardrails only."]
    if settings is not None:
        notes.append(f"planning_stage={settings.retail_decision_desk_planning_stage}")
    return RetailDecisionDeskSafetyPolicy(
        policy_id="retail-decision-desk-safety-policy-v1",
        name="Retail Decision Desk Planning Safety Policy",
        notes=notes,
    )


def evaluate_retail_decision_desk_plan_safety(
    plan: RetailDecisionDeskPlan,
    policy: RetailDecisionDeskSafetyPolicy,
) -> RetailDecisionDeskSafetyResult:
    reasons: list[str] = []
    if policy.allow_real_data:
        reasons.append("real data is not allowed")
    if plan.recommendations_allowed or policy.allow_recommendations:
        reasons.append("recommendations are not allowed")
    if plan.action_generation_allowed or policy.allow_action_generation:
        reasons.append("action generation is not allowed")
    if plan.confidence_scoring_allowed or policy.allow_confidence_scoring:
        reasons.append("confidence scoring is not allowed")
    if plan.decision_object_generation_allowed or policy.allow_decision_objects:
        reasons.append("DecisionObject generation is not allowed")
    if plan.execution_allowed or policy.allow_execution:
        reasons.append("execution is not allowed")
    if not plan.requires_human_review or not policy.require_human_review:
        reasons.append("human review is required")
    if not policy.require_evidence:
        reasons.append("evidence is required")
    if reasons:
        return RetailDecisionDeskSafetyResult(decision="blocked", reasons=reasons, policy_id=policy.policy_id)
    return RetailDecisionDeskSafetyResult(
        decision="planning_allowed",
        reasons=[
            "Decision Desk plan is planning-only",
            "recommendations, action generation, confidence scoring, DecisionObject generation, and execution remain blocked",
        ],
        policy_id=policy.policy_id,
    )


def evaluate_action_placeholder_safety(
    placeholders: list[RetailActionPlaceholderContract],
    policy: RetailDecisionDeskSafetyPolicy,
) -> RetailDecisionDeskSafetyResult:
    reasons: list[str] = []
    if not placeholders:
        reasons.append("action placeholders are missing")
    for placeholder in placeholders:
        if not placeholder.planning_only:
            reasons.append(f"{placeholder.placeholder_id}: placeholder must remain planning-only")
        if placeholder.generated_now or policy.allow_action_generation:
            reasons.append(f"{placeholder.placeholder_id}: action generation is not allowed")
        if placeholder.recommendation or policy.allow_recommendations:
            reasons.append(f"{placeholder.placeholder_id}: recommendations are not allowed")
        if placeholder.trade_signal:
            reasons.append(f"{placeholder.placeholder_id}: trade signals are not allowed")
        if placeholder.decision_object_generated or policy.allow_decision_objects:
            reasons.append(f"{placeholder.placeholder_id}: DecisionObject generation is not allowed")
        if placeholder.execution_ready or policy.allow_execution:
            reasons.append(f"{placeholder.placeholder_id}: execution readiness is not allowed")
    if policy.allow_real_data:
        reasons.append("real data is not allowed")
    if policy.allow_confidence_scoring:
        reasons.append("confidence scoring is not allowed")
    if reasons:
        return RetailDecisionDeskSafetyResult(decision="blocked", reasons=reasons, policy_id=policy.policy_id)
    return RetailDecisionDeskSafetyResult(
        decision="planning_allowed",
        reasons=["action placeholders are inactive planning metadata only"],
        policy_id=policy.policy_id,
    )


def reject_recommendation_or_action_generation(
    reason: str = "recommendation or action generation is forbidden",
) -> RetailDecisionDeskSafetyResult:
    return RetailDecisionDeskSafetyResult(
        decision="blocked",
        reasons=[reason],
        policy_id="retail-decision-desk-safety-policy-v1",
    )


def reject_confidence_or_decision_object_generation(
    reason: str = "confidence scoring or DecisionObject generation is forbidden",
) -> RetailDecisionDeskSafetyResult:
    return RetailDecisionDeskSafetyResult(
        decision="blocked",
        reasons=[reason],
        policy_id="retail-decision-desk-safety-policy-v1",
    )
