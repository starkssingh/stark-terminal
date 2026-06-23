from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator


class DecisionEvidenceValidationStage(StrEnum):
    VALIDATION_V0 = "VALIDATION_V0"
    UNAVAILABLE_ONLY = "UNAVAILABLE_ONLY"
    BUNDLE_VALIDATION_PLANNED = "BUNDLE_VALIDATION_PLANNED"
    DECISION_OBJECT_GENERATION_PLANNED = "DECISION_OBJECT_GENERATION_PLANNED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class DecisionEvidenceValidationIssueSeverity(StrEnum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    BLOCKER = "BLOCKER"
    UNKNOWN = "UNKNOWN"


class DecisionEvidenceValidationIssueKind(StrEnum):
    MISSING_EVIDENCE_ITEM = "MISSING_EVIDENCE_ITEM"
    INVALID_EVIDENCE_ITEM = "INVALID_EVIDENCE_ITEM"
    MISSING_SOURCE_REFERENCE = "MISSING_SOURCE_REFERENCE"
    INVALID_SOURCE_REFERENCE = "INVALID_SOURCE_REFERENCE"
    MISSING_PROVENANCE = "MISSING_PROVENANCE"
    INCOMPLETE_PROVENANCE = "INCOMPLETE_PROVENANCE"
    MISSING_VALIDATION_CHECKLIST = "MISSING_VALIDATION_CHECKLIST"
    INCOMPLETE_VALIDATION_CHECKLIST = "INCOMPLETE_VALIDATION_CHECKLIST"
    MISSING_HUMAN_REVIEW_ATTACHMENT = "MISSING_HUMAN_REVIEW_ATTACHMENT"
    INCOMPLETE_HUMAN_REVIEW_ATTACHMENT = "INCOMPLETE_HUMAN_REVIEW_ATTACHMENT"
    UNSAFE_GENERATED_OUTPUT_FLAG = "UNSAFE_GENERATED_OUTPUT_FLAG"
    UNKNOWN = "UNKNOWN"


class DecisionEvidenceValidationSafetyLabel(StrEnum):
    VALIDATION_ONLY = "VALIDATION_ONLY"
    NOT_A_RECOMMENDATION = "NOT_A_RECOMMENDATION"
    NOT_APPROVAL = "NOT_APPROVAL"
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


def sanitize_decision_evidence_validation_notes(values: list[str]) -> list[str]:
    sanitized: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized:
            sanitized.append(normalized)
    return sanitized


class DecisionEvidenceValidationRequest(BaseModel):
    request_id: str
    bundle_id: str | None = None
    validate_items: bool = True
    validate_provenance: bool = True
    validate_checklist: bool = True
    validate_human_review: bool = True
    validate_safety_flags: bool = True
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    execution_allowed: bool = False
    approval_allowed: bool = False
    override_allowed: bool = False
    readiness_to_trade_allowed: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("request_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision evidence validation request text fields")

    @field_validator("bundle_id")
    @classmethod
    def optional_text_fields_must_be_sanitized(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_evidence_validation_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def request_must_remain_validation_only(self) -> DecisionEvidenceValidationRequest:
        if not any(
            [
                self.validate_items,
                self.validate_provenance,
                self.validate_checklist,
                self.validate_human_review,
                self.validate_safety_flags,
            ]
        ):
            raise ValueError("at least one decision evidence validation flag must be true")
        if self.recommendations_allowed:
            raise ValueError("recommendations are forbidden in Prompt 44")
        if self.action_generation_allowed:
            raise ValueError("action generation is forbidden in Prompt 44")
        if self.confidence_scoring_allowed:
            raise ValueError("confidence scoring is forbidden in Prompt 44")
        if self.decision_object_generation_allowed:
            raise ValueError("DecisionObject generation is forbidden in Prompt 44")
        if self.execution_allowed:
            raise ValueError("execution is forbidden in Prompt 44")
        if self.approval_allowed:
            raise ValueError("approval is forbidden in Prompt 44")
        if self.override_allowed:
            raise ValueError("override is forbidden in Prompt 44")
        if self.readiness_to_trade_allowed:
            raise ValueError("readiness-to-trade is forbidden in Prompt 44")
        return self


def create_decision_evidence_validation_request(
    request_id: str,
    bundle_id: str | None = None,
    validate_items: bool = True,
    validate_provenance: bool = True,
    validate_checklist: bool = True,
    validate_human_review: bool = True,
    validate_safety_flags: bool = True,
    notes: list[str] | None = None,
) -> DecisionEvidenceValidationRequest:
    return DecisionEvidenceValidationRequest(
        request_id=request_id,
        bundle_id=bundle_id,
        validate_items=validate_items,
        validate_provenance=validate_provenance,
        validate_checklist=validate_checklist,
        validate_human_review=validate_human_review,
        validate_safety_flags=validate_safety_flags,
        notes=notes or [],
    )


def default_decision_evidence_validation_request() -> DecisionEvidenceValidationRequest:
    return create_decision_evidence_validation_request(
        request_id="decision-evidence-validation-request-v1",
        notes=[
            "Prompt 44 validates contract completeness only.",
            "Validation is not a recommendation, approval, readiness-to-trade, or DecisionObject generation gate.",
        ],
    )

