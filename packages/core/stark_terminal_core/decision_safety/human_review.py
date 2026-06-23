from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_safety.guardrails import (
    DecisionSafetyLabel,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_decision_safety_notes,
)


class DecisionHumanReviewGate(BaseModel):
    gate_id: str
    title: str
    description: str
    reviewer_role: str = "human_operator"
    required: bool = True
    approval_granted: bool = False
    blocks_recommendations: bool = True
    blocks_action_generation: bool = True
    blocks_confidence_scoring: bool = True
    blocks_decision_object_generation: bool = True
    blocks_execution: bool = True
    safety_label: DecisionSafetyLabel = DecisionSafetyLabel.NOT_APPROVAL
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("gate_id", "title", "description", "reviewer_role", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision human-review gate text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_safety_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def gate_must_not_approve(self) -> DecisionHumanReviewGate:
        if self.approval_granted:
            raise ValueError("human-review gates cannot grant approval in Prompt 39")
        if not self.blocks_recommendations:
            raise ValueError("human-review gates must block recommendations in Prompt 39")
        if not self.blocks_action_generation:
            raise ValueError("human-review gates must block action generation in Prompt 39")
        if not self.blocks_confidence_scoring:
            raise ValueError("human-review gates must block confidence scoring in Prompt 39")
        if not self.blocks_decision_object_generation:
            raise ValueError("human-review gates must block DecisionObject generation in Prompt 39")
        if not self.blocks_execution:
            raise ValueError("human-review gates must block execution in Prompt 39")
        if self.safety_label == DecisionSafetyLabel.UNKNOWN:
            raise ValueError("decision human-review gate safety label cannot be UNKNOWN")
        return self


class DecisionHumanReviewGateSet(BaseModel):
    gate_set_id: str
    gates: list[DecisionHumanReviewGate]
    complete: bool = False
    approval_granted: bool = False
    recommendations_allowed: bool = False
    decision_object_generation_allowed: bool = False
    execution_allowed: bool = False
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("gate_set_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision human-review gate set text fields")

    @field_validator("blockers", "warnings")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_safety_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def gate_set_must_not_approve(self) -> DecisionHumanReviewGateSet:
        if not self.gates:
            raise ValueError("decision human-review gate set requires gates")
        if self.approval_granted:
            raise ValueError("human-review gate sets cannot grant approval in Prompt 39")
        if self.recommendations_allowed:
            raise ValueError("recommendations are forbidden in Prompt 39")
        if self.decision_object_generation_allowed:
            raise ValueError("DecisionObject generation is forbidden in Prompt 39")
        if self.execution_allowed:
            raise ValueError("execution is forbidden in Prompt 39")
        if self.complete and self.blockers:
            raise ValueError("complete human-review gate sets cannot have blockers")
        return self


def default_decision_human_review_gates() -> list[DecisionHumanReviewGate]:
    definitions = [
        (
            "decision-human-review-evidence-gate",
            "Evidence Review Gate",
            "Requires a future human operator to review evidence completeness; this is not approval.",
        ),
        (
            "decision-human-review-safety-gate",
            "Safety Review Gate",
            "Requires a future human operator to review safety blockers; this is not approval.",
        ),
        (
            "decision-human-review-display-gate",
            "Retail Display Review Gate",
            "Requires review before any future retail-facing surface; this is not approval.",
        ),
    ]
    return [
        DecisionHumanReviewGate(
            gate_id=gate_id,
            title=title,
            description=description,
            notes=["Human-review gate placeholder; approval_granted remains false."],
        )
        for gate_id, title, description in definitions
    ]


def build_decision_human_review_gate_set(
    gates: list[DecisionHumanReviewGate] | None = None,
    blockers: list[str] | None = None,
    warnings: list[str] | None = None,
    complete: bool = False,
) -> DecisionHumanReviewGateSet:
    return DecisionHumanReviewGateSet(
        gate_set_id="decision-human-review-gate-set-v1",
        gates=list(gates or default_decision_human_review_gates()),
        complete=complete,
        blockers=blockers or [],
        warnings=warnings or [],
    )


def evaluate_decision_human_review_gate_set(
    gate_set: DecisionHumanReviewGateSet,
) -> DecisionHumanReviewGateSet:
    blockers = list(gate_set.blockers)
    warnings = list(gate_set.warnings)
    if not gate_set.gates:
        blockers.append("decision human-review gates are missing")
    for gate in gate_set.gates:
        if gate.required and not gate.blocks_decision_object_generation:
            blockers.append(f"{gate.gate_id}: required gate does not block DecisionObject generation")
        if gate.approval_granted:
            blockers.append(f"{gate.gate_id}: approval cannot be granted")
    if not blockers:
        warnings.append("human-review gates are present but do not grant approval")
    return DecisionHumanReviewGateSet(
        gate_set_id=gate_set.gate_set_id,
        gates=list(gate_set.gates),
        complete=not blockers,
        blockers=blockers,
        warnings=warnings,
        schema_version=gate_set.schema_version,
        created_at=gate_set.created_at,
    )
