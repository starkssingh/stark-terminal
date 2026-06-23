from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_safety.guardrails import (
    DecisionBlockedOutputKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    default_blocked_output_kinds,
    sanitize_decision_safety_notes,
)


class DecisionBlockedOutputPolicy(BaseModel):
    policy_id: str
    name: str
    blocked_outputs: list[DecisionBlockedOutputKind]
    blocks_all_recommendation_like_outputs: bool = True
    blocks_all_execution_like_outputs: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)

    @field_validator("policy_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision blocked output policy text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_safety_notes(value)

    @model_validator(mode="after")
    def policy_must_block_all_required_outputs(self) -> DecisionBlockedOutputPolicy:
        if not self.blocked_outputs:
            raise ValueError("blocked outputs cannot be empty")
        if DecisionBlockedOutputKind.UNKNOWN in self.blocked_outputs:
            raise ValueError("UNKNOWN blocked output is not allowed")
        required = set(default_blocked_output_kinds())
        missing = required - set(self.blocked_outputs)
        if missing:
            missing_names = ", ".join(sorted(item.value for item in missing))
            raise ValueError(f"blocked output policy is missing required outputs: {missing_names}")
        if not self.blocks_all_recommendation_like_outputs:
            raise ValueError("recommendation-like outputs must remain blocked in Prompt 39")
        if not self.blocks_all_execution_like_outputs:
            raise ValueError("execution-like outputs must remain blocked in Prompt 39")
        return self


class DecisionBlockedOutputEvaluation(BaseModel):
    evaluation_id: str
    policy_id: str
    blocked: bool = True
    forbidden_outputs: list[DecisionBlockedOutputKind]
    reasons: list[str]
    schema_version: str = "v1"
    evaluated_at: datetime = Field(default_factory=_utc_now)

    @field_validator("evaluation_id", "policy_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision blocked output evaluation text fields")

    @field_validator("reasons")
    @classmethod
    def reasons_must_be_present(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_decision_safety_notes(value)
        if not sanitized:
            raise ValueError("decision blocked output evaluation reasons cannot be empty")
        return sanitized

    @field_validator("evaluated_at")
    @classmethod
    def evaluated_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def evaluation_must_remain_blocked(self) -> DecisionBlockedOutputEvaluation:
        if not self.blocked:
            raise ValueError("blocked output evaluation must remain blocked in Prompt 39")
        if not self.forbidden_outputs:
            raise ValueError("forbidden outputs cannot be empty")
        if DecisionBlockedOutputKind.UNKNOWN in self.forbidden_outputs:
            raise ValueError("UNKNOWN forbidden output is not allowed")
        return self


def default_decision_blocked_output_policy() -> DecisionBlockedOutputPolicy:
    return DecisionBlockedOutputPolicy(
        policy_id="decision-blocked-output-policy-v1",
        name="Decision Safety Blocked Output Policy",
        blocked_outputs=default_blocked_output_kinds(),
        notes=[
            "Blocks recommendations, action generation, confidence scoring, DecisionObject generation, execution, broker orders, and market-state decisions.",
        ],
    )


def evaluate_decision_blocked_output_policy(
    policy: DecisionBlockedOutputPolicy | None = None,
) -> DecisionBlockedOutputEvaluation:
    resolved = policy or default_decision_blocked_output_policy()
    return DecisionBlockedOutputEvaluation(
        evaluation_id="decision-blocked-output-evaluation-v1",
        policy_id=resolved.policy_id,
        blocked=True,
        forbidden_outputs=list(resolved.blocked_outputs),
        reasons=[
            "Prompt 39 keeps all recommendation-like, action-like, confidence-like, DecisionObject, and execution-like outputs blocked.",
        ],
    )
