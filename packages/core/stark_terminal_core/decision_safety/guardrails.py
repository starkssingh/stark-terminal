from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator


class DecisionSafetyStage(StrEnum):
    GUARDRAILS_ONLY = "GUARDRAILS_ONLY"
    HUMAN_REVIEW_PLANNED = "HUMAN_REVIEW_PLANNED"
    APPROVAL_WORKFLOW_PLANNED = "APPROVAL_WORKFLOW_PLANNED"
    DECISION_OBJECT_GENERATION_PLANNED = "DECISION_OBJECT_GENERATION_PLANNED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class DecisionSafetyDecision(StrEnum):
    ALLOW_PLANNING_ONLY = "ALLOW_PLANNING_ONLY"
    BLOCK = "BLOCK"
    WARN = "WARN"
    UNKNOWN = "UNKNOWN"


class DecisionApprovalPlaceholderStatus(StrEnum):
    NOT_REQUESTED = "NOT_REQUESTED"
    PLACEHOLDER_ONLY = "PLACEHOLDER_ONLY"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class DecisionBlockedOutputKind(StrEnum):
    RECOMMENDATION = "RECOMMENDATION"
    ACTION_GENERATION = "ACTION_GENERATION"
    CONFIDENCE_SCORE = "CONFIDENCE_SCORE"
    DECISION_OBJECT = "DECISION_OBJECT"
    EXECUTION = "EXECUTION"
    BROKER_ORDER = "BROKER_ORDER"
    MARKET_STATE_DECISION = "MARKET_STATE_DECISION"
    UNKNOWN = "UNKNOWN"


class DecisionSafetyLabel(StrEnum):
    GUARDRAILS_ONLY = "GUARDRAILS_ONLY"
    NOT_APPROVAL = "NOT_APPROVAL"
    NOT_A_RECOMMENDATION = "NOT_A_RECOMMENDATION"
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


def sanitize_decision_safety_notes(values: list[str]) -> list[str]:
    sanitized: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized:
            sanitized.append(normalized)
    return sanitized


def default_blocked_output_kinds() -> list[DecisionBlockedOutputKind]:
    return [
        DecisionBlockedOutputKind.RECOMMENDATION,
        DecisionBlockedOutputKind.ACTION_GENERATION,
        DecisionBlockedOutputKind.CONFIDENCE_SCORE,
        DecisionBlockedOutputKind.DECISION_OBJECT,
        DecisionBlockedOutputKind.EXECUTION,
        DecisionBlockedOutputKind.BROKER_ORDER,
        DecisionBlockedOutputKind.MARKET_STATE_DECISION,
    ]


class DecisionSafetyGuardrail(BaseModel):
    guardrail_id: str
    name: str
    description: str
    blocked_outputs: list[DecisionBlockedOutputKind]
    required: bool = True
    enabled: bool = True
    blocks_recommendations: bool = True
    blocks_action_generation: bool = True
    blocks_confidence_scoring: bool = True
    blocks_decision_object_generation: bool = True
    blocks_execution: bool = True
    safety_label: DecisionSafetyLabel = DecisionSafetyLabel.GUARDRAILS_ONLY
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("guardrail_id", "name", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision safety guardrail text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_safety_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def guardrail_must_fail_closed(self) -> DecisionSafetyGuardrail:
        if not self.blocked_outputs:
            raise ValueError("decision safety guardrail blocked outputs cannot be empty")
        if DecisionBlockedOutputKind.UNKNOWN in self.blocked_outputs:
            raise ValueError("UNKNOWN blocked output is not allowed")
        if not self.blocks_recommendations:
            raise ValueError("decision safety guardrails must block recommendations in Prompt 39")
        if not self.blocks_action_generation:
            raise ValueError("decision safety guardrails must block action generation in Prompt 39")
        if not self.blocks_confidence_scoring:
            raise ValueError("decision safety guardrails must block confidence scoring in Prompt 39")
        if not self.blocks_decision_object_generation:
            raise ValueError("decision safety guardrails must block DecisionObject generation in Prompt 39")
        if not self.blocks_execution:
            raise ValueError("decision safety guardrails must block execution in Prompt 39")
        if self.safety_label == DecisionSafetyLabel.UNKNOWN:
            raise ValueError("decision safety label cannot be UNKNOWN")
        return self


class DecisionSafetyGuardrailSet(BaseModel):
    guardrail_set_id: str
    guardrails: list[DecisionSafetyGuardrail]
    complete: bool = False
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    execution_allowed: bool = False
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("guardrail_set_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision safety guardrail set text fields")

    @field_validator("blockers", "warnings")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_safety_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def guardrail_set_must_fail_closed(self) -> DecisionSafetyGuardrailSet:
        if not self.guardrails:
            raise ValueError("decision safety guardrail set requires guardrails")
        if self.recommendations_allowed:
            raise ValueError("recommendations are forbidden in Prompt 39")
        if self.action_generation_allowed:
            raise ValueError("action generation is forbidden in Prompt 39")
        if self.confidence_scoring_allowed:
            raise ValueError("confidence scoring is forbidden in Prompt 39")
        if self.decision_object_generation_allowed:
            raise ValueError("DecisionObject generation is forbidden in Prompt 39")
        if self.execution_allowed:
            raise ValueError("execution is forbidden in Prompt 39")
        if self.complete and self.blockers:
            raise ValueError("complete guardrail sets cannot have blockers")
        return self


def default_decision_safety_guardrails() -> list[DecisionSafetyGuardrail]:
    definitions = [
        (
            "decision-safety-recommendation-block",
            "Recommendation Block",
            "Blocks recommendation-like outputs until a future audited prompt explicitly permits them.",
        ),
        (
            "decision-safety-action-block",
            "Action Generation Block",
            "Blocks action-state generation and market-state decision outputs.",
        ),
        (
            "decision-safety-confidence-block",
            "Confidence Scoring Block",
            "Blocks confidence score generation and confidence-like trading logic.",
        ),
        (
            "decision-safety-decision-object-block",
            "DecisionObject Generation Block",
            "Blocks active DecisionObject generation until future safety gates are implemented and audited.",
        ),
        (
            "decision-safety-execution-block",
            "Execution Block",
            "Blocks execution APIs, broker orders, and broker integration behavior.",
        ),
    ]
    return [
        DecisionSafetyGuardrail(
            guardrail_id=guardrail_id,
            name=name,
            description=description,
            blocked_outputs=default_blocked_output_kinds(),
            notes=["Guardrails-only contract; not an approval or recommendation."],
        )
        for guardrail_id, name, description in definitions
    ]


def build_decision_safety_guardrail_set(
    guardrails: list[DecisionSafetyGuardrail] | None = None,
    blockers: list[str] | None = None,
    warnings: list[str] | None = None,
    complete: bool = False,
) -> DecisionSafetyGuardrailSet:
    return DecisionSafetyGuardrailSet(
        guardrail_set_id="decision-safety-guardrail-set-v1",
        guardrails=list(guardrails or default_decision_safety_guardrails()),
        complete=complete,
        blockers=blockers or [],
        warnings=warnings or [],
    )


def evaluate_decision_safety_guardrail_set(
    guardrail_set: DecisionSafetyGuardrailSet,
) -> DecisionSafetyGuardrailSet:
    blockers = list(guardrail_set.blockers)
    warnings = list(guardrail_set.warnings)
    if not guardrail_set.guardrails:
        blockers.append("decision safety guardrails are missing")
    for guardrail in guardrail_set.guardrails:
        if not guardrail.enabled:
            blockers.append(f"{guardrail.guardrail_id}: guardrail is disabled")
        if guardrail.required and not guardrail.enabled:
            blockers.append(f"{guardrail.guardrail_id}: required guardrail is not enabled")
    if not blockers:
        warnings.append("guardrails are present for planning only; no approval is granted")
    return DecisionSafetyGuardrailSet(
        guardrail_set_id=guardrail_set.guardrail_set_id,
        guardrails=list(guardrail_set.guardrails),
        complete=not blockers,
        blockers=blockers,
        warnings=warnings,
        schema_version=guardrail_set.schema_version,
        created_at=guardrail_set.created_at,
    )
