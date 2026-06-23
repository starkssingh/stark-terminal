from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator


class DecisionReadinessAPIStage(StrEnum):
    READINESS_CONTRACT_SKELETON = "READINESS_CONTRACT_SKELETON"
    UNAVAILABLE_ONLY = "UNAVAILABLE_ONLY"
    EVIDENCE_REFERENCE_PLANNED = "EVIDENCE_REFERENCE_PLANNED"
    SAFETY_REFERENCE_PLANNED = "SAFETY_REFERENCE_PLANNED"
    DECISION_OBJECT_GENERATION_PLANNED = "DECISION_OBJECT_GENERATION_PLANNED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class DecisionReadinessRequestKind(StrEnum):
    READINESS_STATUS_REQUEST = "READINESS_STATUS_REQUEST"
    EVIDENCE_READINESS_REQUEST = "EVIDENCE_READINESS_REQUEST"
    SAFETY_READINESS_REQUEST = "SAFETY_READINESS_REQUEST"
    HUMAN_REVIEW_READINESS_REQUEST = "HUMAN_REVIEW_READINESS_REQUEST"
    BLOCKED_OUTPUT_READINESS_REQUEST = "BLOCKED_OUTPUT_READINESS_REQUEST"
    UNKNOWN = "UNKNOWN"


class DecisionReadinessUnavailableReason(StrEnum):
    RECOMMENDATIONS_DISABLED = "RECOMMENDATIONS_DISABLED"
    ACTION_GENERATION_DISABLED = "ACTION_GENERATION_DISABLED"
    CONFIDENCE_SCORING_DISABLED = "CONFIDENCE_SCORING_DISABLED"
    DECISION_OBJECT_GENERATION_DISABLED = "DECISION_OBJECT_GENERATION_DISABLED"
    EXECUTION_DISABLED = "EXECUTION_DISABLED"
    APPROVAL_DISABLED = "APPROVAL_DISABLED"
    OVERRIDE_DISABLED = "OVERRIDE_DISABLED"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
    EVIDENCE_BUNDLE_REQUIRED = "EVIDENCE_BUNDLE_REQUIRED"
    SAFETY_GUARDRAILS_REQUIRED = "SAFETY_GUARDRAILS_REQUIRED"
    CONTRACT_SKELETON_ONLY = "CONTRACT_SKELETON_ONLY"
    UNKNOWN = "UNKNOWN"


class DecisionReadinessSafetyLabel(StrEnum):
    READINESS_CONTRACT_SKELETON_ONLY = "READINESS_CONTRACT_SKELETON_ONLY"
    UNAVAILABLE = "UNAVAILABLE"
    NOT_A_RECOMMENDATION = "NOT_A_RECOMMENDATION"
    NOT_APPROVAL = "NOT_APPROVAL"
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


def sanitize_decision_readiness_notes(values: list[str]) -> list[str]:
    sanitized: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized:
            sanitized.append(normalized)
    return sanitized


class DecisionReadinessRequestPlaceholder(BaseModel):
    request_id: str
    request_kind: DecisionReadinessRequestKind
    instrument_id: str | None = None
    timeframe: str | None = None
    requested_readiness_sections: list[str] = Field(default_factory=list)
    evidence_reference_required: bool = True
    safety_reference_required: bool = True
    human_review_reference_required: bool = True
    blocked_output_reference_required: bool = True
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    execution_allowed: bool = False
    approval_allowed: bool = False
    override_allowed: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("request_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision readiness request placeholder text fields")

    @field_validator("instrument_id", "timeframe")
    @classmethod
    def optional_text_fields_must_be_trimmed(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("requested_readiness_sections", "notes")
    @classmethod
    def lists_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_readiness_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def request_placeholder_must_fail_closed(self) -> DecisionReadinessRequestPlaceholder:
        if self.request_kind == DecisionReadinessRequestKind.UNKNOWN:
            raise ValueError("UNKNOWN readiness request kind is not allowed")
        if not self.evidence_reference_required:
            raise ValueError("evidence references are required in Prompt 42")
        if not self.safety_reference_required:
            raise ValueError("decision safety references are required in Prompt 42")
        if not self.human_review_reference_required:
            raise ValueError("human-review references are required in Prompt 42")
        if not self.blocked_output_reference_required:
            raise ValueError("blocked-output references are required in Prompt 42")
        if self.recommendations_allowed:
            raise ValueError("recommendations are forbidden in Prompt 42")
        if self.action_generation_allowed:
            raise ValueError("action generation is forbidden in Prompt 42")
        if self.confidence_scoring_allowed:
            raise ValueError("confidence scoring is forbidden in Prompt 42")
        if self.decision_object_generation_allowed:
            raise ValueError("DecisionObject generation is forbidden in Prompt 42")
        if self.execution_allowed:
            raise ValueError("execution is forbidden in Prompt 42")
        if self.approval_allowed:
            raise ValueError("approval is forbidden in Prompt 42")
        if self.override_allowed:
            raise ValueError("override is forbidden in Prompt 42")
        return self


def create_decision_readiness_request_placeholder(
    request_id: str,
    request_kind: DecisionReadinessRequestKind = DecisionReadinessRequestKind.READINESS_STATUS_REQUEST,
    instrument_id: str | None = None,
    timeframe: str | None = None,
    requested_readiness_sections: list[str] | None = None,
    notes: list[str] | None = None,
) -> DecisionReadinessRequestPlaceholder:
    return DecisionReadinessRequestPlaceholder(
        request_id=request_id,
        request_kind=request_kind,
        instrument_id=instrument_id,
        timeframe=timeframe,
        requested_readiness_sections=list(requested_readiness_sections or []),
        notes=list(notes or ["Readiness contract skeleton request placeholder; not a recommendation request."]),
    )


def default_decision_readiness_request_placeholder() -> DecisionReadinessRequestPlaceholder:
    return create_decision_readiness_request_placeholder(
        request_id="decision-readiness-request-placeholder-v1",
        request_kind=DecisionReadinessRequestKind.READINESS_STATUS_REQUEST,
        requested_readiness_sections=[
            "evidence_reference_placeholder",
            "safety_reference_placeholder",
            "human_review_reference_placeholder",
            "blocked_output_reference_placeholder",
            "unavailable_readiness_response",
        ],
    )
