from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_api.references import (
    DecisionEvidenceBundleReferencePlaceholder,
    DecisionSafetyReferencePlaceholder,
    default_decision_safety_reference_placeholder,
    default_evidence_bundle_reference_placeholder,
)
from stark_terminal_core.decision_api.requests import (
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_decision_api_notes,
)
from stark_terminal_core.decision_api.unavailable import (
    DecisionDeskUnavailableResponse,
    default_decision_desk_unavailable_response,
)


class DecisionDeskResponsePlaceholder(BaseModel):
    response_id: str
    request_id: str | None = None
    evidence_reference: DecisionEvidenceBundleReferencePlaceholder
    safety_reference: DecisionSafetyReferencePlaceholder
    unavailable_response: DecisionDeskUnavailableResponse
    planning_only: bool = True
    recommendation_generated: bool = False
    action_generated: bool = False
    confidence_generated: bool = False
    decision_object_generated: bool = False
    execution_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("response_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision desk response placeholder text fields")

    @field_validator("request_id")
    @classmethod
    def optional_text_fields_must_be_trimmed(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_api_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def response_placeholder_must_fail_closed(self) -> DecisionDeskResponsePlaceholder:
        if not self.planning_only:
            raise ValueError("Decision Desk API response placeholders must remain planning-only")
        if self.recommendation_generated:
            raise ValueError("recommendations are forbidden in Prompt 40")
        if self.action_generated:
            raise ValueError("action generation is forbidden in Prompt 40")
        if self.confidence_generated:
            raise ValueError("confidence scoring is forbidden in Prompt 40")
        if self.decision_object_generated:
            raise ValueError("DecisionObject generation is forbidden in Prompt 40")
        if self.execution_ready:
            raise ValueError("execution readiness is forbidden in Prompt 40")
        return self


def create_decision_desk_response_placeholder(
    response_id: str,
    request_id: str | None = None,
    evidence_reference: DecisionEvidenceBundleReferencePlaceholder | None = None,
    safety_reference: DecisionSafetyReferencePlaceholder | None = None,
    unavailable_response: DecisionDeskUnavailableResponse | None = None,
    notes: list[str] | None = None,
) -> DecisionDeskResponsePlaceholder:
    resolved_unavailable = unavailable_response or default_decision_desk_unavailable_response(request_id=request_id)
    return DecisionDeskResponsePlaceholder(
        response_id=response_id,
        request_id=request_id,
        evidence_reference=evidence_reference or default_evidence_bundle_reference_placeholder(),
        safety_reference=safety_reference or default_decision_safety_reference_placeholder(),
        unavailable_response=resolved_unavailable,
        notes=list(notes or ["Response placeholder contains no generated outputs."]),
    )


def default_decision_desk_response_placeholder() -> DecisionDeskResponsePlaceholder:
    return create_decision_desk_response_placeholder(
        response_id="decision-desk-response-placeholder-v1",
    )

