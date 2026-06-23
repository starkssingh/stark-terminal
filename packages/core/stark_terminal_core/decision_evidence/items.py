from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator


class DecisionEvidenceStage(StrEnum):
    CONTRACTS_ONLY = "CONTRACTS_ONLY"
    BUNDLE_VALIDATION_PLANNED = "BUNDLE_VALIDATION_PLANNED"
    HUMAN_REVIEW_PLANNED = "HUMAN_REVIEW_PLANNED"
    DECISION_OBJECT_GENERATION_PLANNED = "DECISION_OBJECT_GENERATION_PLANNED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class DecisionEvidenceItemKind(StrEnum):
    INSTRUMENT_CONTEXT = "INSTRUMENT_CONTEXT"
    DATA_QUALITY = "DATA_QUALITY"
    RETURNS = "RETURNS"
    VOLATILITY = "VOLATILITY"
    DRAWDOWN = "DRAWDOWN"
    CORRELATION_BETA = "CORRELATION_BETA"
    TIME_SERIES_DIAGNOSTICS = "TIME_SERIES_DIAGNOSTICS"
    REGIME_CONTEXT = "REGIME_CONTEXT"
    REGIME_FEATURE_CONTEXT = "REGIME_FEATURE_CONTEXT"
    RISK_CONTEXT = "RISK_CONTEXT"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    UNKNOWN = "UNKNOWN"


class DecisionEvidenceStatus(StrEnum):
    PLANNED = "PLANNED"
    REQUIRED = "REQUIRED"
    MISSING = "MISSING"
    PRESENT = "PRESENT"
    INVALID = "INVALID"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class DecisionEvidenceSafetyLabel(StrEnum):
    CONTRACTS_ONLY = "CONTRACTS_ONLY"
    NOT_A_RECOMMENDATION = "NOT_A_RECOMMENDATION"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
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


def sanitize_decision_evidence_notes(values: list[str]) -> list[str]:
    sanitized: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized:
            sanitized.append(normalized)
    return sanitized


class DecisionEvidenceItemContract(BaseModel):
    item_id: str
    kind: DecisionEvidenceItemKind
    name: str
    description: str
    required: bool = True
    status: DecisionEvidenceStatus = DecisionEvidenceStatus.PLANNED
    source_reference_required: bool = True
    validation_required: bool = True
    human_review_required: bool = True
    value_payload_allowed: bool = False
    recommendation: bool = False
    action_generated: bool = False
    confidence_generated: bool = False
    decision_object_generated: bool = False
    execution_ready: bool = False
    safety_label: DecisionEvidenceSafetyLabel = DecisionEvidenceSafetyLabel.CONTRACTS_ONLY
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("item_id", "name", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision evidence item text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_evidence_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def item_must_remain_contract_only(self) -> DecisionEvidenceItemContract:
        if self.kind == DecisionEvidenceItemKind.UNKNOWN:
            raise ValueError("UNKNOWN decision evidence item kind is not allowed")
        if self.status == DecisionEvidenceStatus.UNKNOWN:
            raise ValueError("UNKNOWN decision evidence status is not allowed")
        if self.value_payload_allowed:
            raise ValueError("decision evidence value payloads are forbidden in Prompt 38")
        if self.recommendation:
            raise ValueError("decision evidence items cannot generate recommendations in Prompt 38")
        if self.action_generated:
            raise ValueError("decision evidence items cannot generate actions in Prompt 38")
        if self.confidence_generated:
            raise ValueError("decision evidence items cannot generate confidence scores in Prompt 38")
        if self.decision_object_generated:
            raise ValueError("decision evidence items cannot generate DecisionObjects in Prompt 38")
        if self.execution_ready:
            raise ValueError("decision evidence items cannot be execution-ready in Prompt 38")
        if self.safety_label == DecisionEvidenceSafetyLabel.UNKNOWN:
            raise ValueError("decision evidence safety label cannot be UNKNOWN")
        return self


def create_decision_evidence_item_contract(
    item_id: str,
    kind: DecisionEvidenceItemKind,
    name: str,
    description: str,
    status: DecisionEvidenceStatus = DecisionEvidenceStatus.PLANNED,
    notes: list[str] | None = None,
) -> DecisionEvidenceItemContract:
    return DecisionEvidenceItemContract(
        item_id=item_id,
        kind=kind,
        name=name,
        description=description,
        status=status,
        notes=notes or [],
    )


def default_decision_evidence_item_contracts() -> list[DecisionEvidenceItemContract]:
    descriptions = {
        DecisionEvidenceItemKind.INSTRUMENT_CONTEXT: "Instrument identity and context contract for future evidence bundles.",
        DecisionEvidenceItemKind.DATA_QUALITY: "Validation and quality status contract for any future evidence bundle input.",
        DecisionEvidenceItemKind.RETURNS: "Descriptive returns evidence contract only; no recommendation payload.",
        DecisionEvidenceItemKind.VOLATILITY: "Descriptive volatility evidence contract only; no action payload.",
        DecisionEvidenceItemKind.DRAWDOWN: "Descriptive drawdown evidence contract only; no confidence payload.",
        DecisionEvidenceItemKind.CORRELATION_BETA: "Correlation and beta evidence contract only; no decision payload.",
        DecisionEvidenceItemKind.TIME_SERIES_DIAGNOSTICS: "Timestamp diagnostics evidence contract for data-quality context.",
        DecisionEvidenceItemKind.REGIME_CONTEXT: "Regime planning context contract only; no classification output.",
        DecisionEvidenceItemKind.REGIME_FEATURE_CONTEXT: "Regime feature preparation context contract only; no feature values.",
        DecisionEvidenceItemKind.RISK_CONTEXT: "Risk context evidence contract for future review-only use.",
        DecisionEvidenceItemKind.HUMAN_REVIEW: "Human-review attachment evidence contract; not an approval.",
    }
    return [
        create_decision_evidence_item_contract(
            item_id=f"decision-evidence-{kind.value.lower().replace('_', '-')}",
            kind=kind,
            name=kind.value.lower(),
            description=description,
            status=DecisionEvidenceStatus.REQUIRED,
            notes=["Contracts-only evidence item; no value payload in Prompt 38."],
        )
        for kind, description in descriptions.items()
    ]

