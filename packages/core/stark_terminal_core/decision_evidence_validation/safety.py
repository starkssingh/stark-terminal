from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_evidence_validation.contracts import (
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_decision_evidence_validation_notes,
)
from stark_terminal_core.decision_evidence_validation.results import DecisionEvidenceValidationResult


class DecisionEvidenceValidationSafetyPolicy(BaseModel):
    policy_id: str
    name: str
    allow_recommendations: bool = False
    allow_action_generation: bool = False
    allow_confidence_scoring: bool = False
    allow_decision_object_generation: bool = False
    allow_execution: bool = False
    allow_approval: bool = False
    allow_override: bool = False
    allow_readiness_to_trade: bool = False
    require_validation_only: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)

    @field_validator("policy_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision evidence validation safety policy text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_evidence_validation_notes(value)

    @model_validator(mode="after")
    def policy_must_fail_closed(self) -> DecisionEvidenceValidationSafetyPolicy:
        if self.allow_recommendations:
            raise ValueError("recommendations are forbidden in Prompt 44")
        if self.allow_action_generation:
            raise ValueError("action generation is forbidden in Prompt 44")
        if self.allow_confidence_scoring:
            raise ValueError("confidence scoring is forbidden in Prompt 44")
        if self.allow_decision_object_generation:
            raise ValueError("DecisionObject generation is forbidden in Prompt 44")
        if self.allow_execution:
            raise ValueError("execution is forbidden in Prompt 44")
        if self.allow_approval:
            raise ValueError("approval is forbidden in Prompt 44")
        if self.allow_override:
            raise ValueError("override is forbidden in Prompt 44")
        if self.allow_readiness_to_trade:
            raise ValueError("readiness-to-trade is forbidden in Prompt 44")
        if not self.require_validation_only:
            raise ValueError("decision evidence validation must remain validation-only in Prompt 44")
        return self


class DecisionEvidenceValidationSafetyEvaluation(BaseModel):
    decision: str
    reasons: list[str]
    policy_id: str
    evaluated_at: datetime = Field(default_factory=_utc_now)
    schema_version: str = "v1"

    @field_validator("decision", "policy_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision evidence validation safety evaluation text fields")

    @field_validator("reasons")
    @classmethod
    def reasons_must_be_present(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_decision_evidence_validation_notes(value)
        if not sanitized:
            raise ValueError("decision evidence validation safety reasons cannot be empty")
        return sanitized

    @field_validator("evaluated_at")
    @classmethod
    def evaluated_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)


def default_decision_evidence_validation_safety_policy(
    settings: Any | None = None,
) -> DecisionEvidenceValidationSafetyPolicy:
    notes = ["Prompt 44 permits validation-only evidence bundle checks."]
    if settings is not None:
        notes.append(f"stage={settings.decision_evidence_validation_stage}")
    return DecisionEvidenceValidationSafetyPolicy(
        policy_id="decision-evidence-validation-safety-policy-v1",
        name="Decision Evidence Validation Safety Policy",
        notes=notes,
    )


def evaluate_decision_evidence_validation_result_safety(
    result: DecisionEvidenceValidationResult,
    policy: DecisionEvidenceValidationSafetyPolicy,
) -> DecisionEvidenceValidationSafetyEvaluation:
    reasons: list[str] = []
    if not result.validation_only or not policy.require_validation_only:
        reasons.append("validation result must remain validation-only")
    if result.recommendations_allowed or policy.allow_recommendations:
        reasons.append("validation cannot allow recommendations")
    if result.action_generation_allowed or policy.allow_action_generation:
        reasons.append("validation cannot allow action generation")
    if result.confidence_scoring_allowed or policy.allow_confidence_scoring:
        reasons.append("validation cannot allow confidence scoring")
    if result.decision_object_generation_allowed or policy.allow_decision_object_generation:
        reasons.append("validation cannot allow DecisionObject generation")
    if result.execution_allowed or policy.allow_execution:
        reasons.append("validation cannot allow execution")
    if result.approval_granted or policy.allow_approval:
        reasons.append("validation cannot grant approval")
    if result.override_granted or policy.allow_override:
        reasons.append("validation cannot grant override")
    if result.readiness_to_trade or policy.allow_readiness_to_trade:
        reasons.append("validation cannot grant readiness-to-trade")
    if result.blocker_count > 0:
        reasons.append("validation blockers remain unresolved")
    if reasons:
        return DecisionEvidenceValidationSafetyEvaluation(
            decision="blocked",
            reasons=reasons,
            policy_id=policy.policy_id,
        )
    return DecisionEvidenceValidationSafetyEvaluation(
        decision="validation_only_allowed",
        reasons=[
            "validation result is validation-only",
            "recommendations, approvals, readiness-to-trade, DecisionObject generation, and execution remain blocked",
        ],
        policy_id=policy.policy_id,
    )


def reject_validation_as_recommendation(
    reason: str = "validation results cannot be treated as recommendations in Prompt 44",
) -> DecisionEvidenceValidationSafetyEvaluation:
    return DecisionEvidenceValidationSafetyEvaluation(
        decision="blocked",
        reasons=[reason],
        policy_id="decision-evidence-validation-safety-policy-v1",
    )


def reject_validation_as_decision_object_readiness(
    reason: str = "validation results cannot be treated as DecisionObject readiness in Prompt 44",
) -> DecisionEvidenceValidationSafetyEvaluation:
    return DecisionEvidenceValidationSafetyEvaluation(
        decision="blocked",
        reasons=[reason],
        policy_id="decision-evidence-validation-safety-policy-v1",
    )

