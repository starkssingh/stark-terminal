from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator


class RetailDecisionDeskStage(StrEnum):
    PLANNING_ONLY = "PLANNING_ONLY"
    EVIDENCE_REQUIREMENTS = "EVIDENCE_REQUIREMENTS"
    DISPLAY_CONTRACTS_PLANNED = "DISPLAY_CONTRACTS_PLANNED"
    DECISION_OBJECT_CONTRACTS_PLANNED = "DECISION_OBJECT_CONTRACTS_PLANNED"
    HUMAN_REVIEW_PLANNED = "HUMAN_REVIEW_PLANNED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class RetailDecisionDeskSafetyLabel(StrEnum):
    PLANNING_ONLY = "PLANNING_ONLY"
    NOT_A_RECOMMENDATION = "NOT_A_RECOMMENDATION"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class RetailEvidenceKind(StrEnum):
    INSTRUMENT_CONTEXT = "INSTRUMENT_CONTEXT"
    DATA_QUALITY = "DATA_QUALITY"
    RETURNS = "RETURNS"
    VOLATILITY = "VOLATILITY"
    DRAWDOWN = "DRAWDOWN"
    CORRELATION_BETA = "CORRELATION_BETA"
    TIME_SERIES_DIAGNOSTICS = "TIME_SERIES_DIAGNOSTICS"
    REGIME_CONTEXT = "REGIME_CONTEXT"
    FEATURE_CONTEXT = "FEATURE_CONTEXT"
    RISK_CONTEXT = "RISK_CONTEXT"
    HUMAN_REVIEW = "HUMAN_REVIEW"
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


def sanitize_decision_notes(values: list[str]) -> list[str]:
    sanitized: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized:
            sanitized.append(normalized)
    return sanitized


class RetailDecisionDeskPlan(BaseModel):
    plan_id: str
    name: str
    stage: RetailDecisionDeskStage = RetailDecisionDeskStage.PLANNING_ONLY
    purpose: str
    planned_action_placeholders: list[str]
    required_evidence_kinds: list[str]
    forbidden_outputs: list[str]
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    execution_allowed: bool = False
    requires_human_review: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("plan_id", "name", "purpose", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail decision desk plan text fields")

    @field_validator("planned_action_placeholders", "required_evidence_kinds")
    @classmethod
    def required_lists_must_be_present(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_decision_notes(value)
        if not sanitized:
            raise ValueError("retail decision desk plan lists cannot be empty")
        return sanitized

    @field_validator("forbidden_outputs")
    @classmethod
    def forbidden_outputs_must_cover_safety_boundary(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_decision_notes(value)
        joined = " ".join(sanitized).lower()
        required_concepts = ("recommendation", "action", "confidence", "decisionobject", "execution")
        missing = [concept for concept in required_concepts if concept not in joined]
        if missing:
            raise ValueError("forbidden_outputs must include recommendation/action/confidence/DecisionObject/execution concepts")
        return sanitized

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def plan_must_remain_planning_only(self) -> RetailDecisionDeskPlan:
        if self.stage == RetailDecisionDeskStage.UNKNOWN:
            raise ValueError("retail decision desk stage cannot be UNKNOWN")
        if self.recommendations_allowed:
            raise ValueError("recommendation generation is forbidden in Prompt 36")
        if self.action_generation_allowed:
            raise ValueError("action generation is forbidden in Prompt 36")
        if self.confidence_scoring_allowed:
            raise ValueError("confidence scoring is forbidden in Prompt 36")
        if self.decision_object_generation_allowed:
            raise ValueError("DecisionObject generation is forbidden in Prompt 36")
        if self.execution_allowed:
            raise ValueError("execution APIs are forbidden in Prompt 36")
        if not self.requires_human_review:
            raise ValueError("human review is required for Decision Desk planning in Prompt 36")
        return self


def default_forbidden_decision_desk_outputs() -> list[str]:
    return [
        "recommendation_generation",
        "action_generation",
        "confidence_scoring",
        "DecisionObject_generation",
        "execution_apis",
        "broker_integration",
        "market_data_input_for_decisions",
    ]


def default_retail_decision_desk_plan() -> RetailDecisionDeskPlan:
    return RetailDecisionDeskPlan(
        plan_id="retail-decision-desk-plan-v1",
        name="Retail Decision Desk Planning and Guardrails",
        stage=RetailDecisionDeskStage.PLANNING_ONLY,
        purpose="Define planning-only Decision Desk boundaries before any recommendation or DecisionObject work.",
        planned_action_placeholders=[
            "BUY_BIAS",
            "SELL_BIAS",
            "HOLD",
            "WATCH",
            "AVOID",
            "REDUCE",
        ],
        required_evidence_kinds=[kind.value for kind in RetailEvidenceKind if kind != RetailEvidenceKind.UNKNOWN],
        forbidden_outputs=default_forbidden_decision_desk_outputs(),
        notes=[
            "Prompt 36 permits planning, evidence requirements, human-review guardrails, and display boundaries only.",
            "Placeholders are planned categories and are not generated outputs.",
        ],
    )


def create_retail_decision_desk_plan(
    plan_id: str,
    name: str,
    purpose: str,
    planned_action_placeholders: list[str],
    required_evidence_kinds: list[str],
    forbidden_outputs: list[str] | None = None,
    stage: RetailDecisionDeskStage = RetailDecisionDeskStage.PLANNING_ONLY,
) -> RetailDecisionDeskPlan:
    return RetailDecisionDeskPlan(
        plan_id=plan_id,
        name=name,
        stage=stage,
        purpose=purpose,
        planned_action_placeholders=planned_action_placeholders,
        required_evidence_kinds=required_evidence_kinds,
        forbidden_outputs=forbidden_outputs or default_forbidden_decision_desk_outputs(),
    )
