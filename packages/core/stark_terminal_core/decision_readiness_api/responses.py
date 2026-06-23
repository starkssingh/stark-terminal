from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_readiness_api.references import (
    DecisionReadinessBlockedOutputReference,
    DecisionReadinessEvidenceReference,
    DecisionReadinessHumanReviewReference,
    DecisionReadinessSafetyReference,
    default_decision_readiness_blocked_output_reference,
    default_decision_readiness_evidence_reference,
    default_decision_readiness_human_review_reference,
    default_decision_readiness_safety_reference,
)
from stark_terminal_core.decision_readiness_api.requests import (
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_decision_readiness_notes,
)
from stark_terminal_core.decision_readiness_api.unavailable import (
    DecisionReadinessUnavailableResponse,
    default_decision_readiness_unavailable_response,
)


class DecisionReadinessResponsePlaceholder(BaseModel):
    response_id: str
    request_id: str | None = None
    evidence_reference: DecisionReadinessEvidenceReference
    safety_reference: DecisionReadinessSafetyReference
    human_review_reference: DecisionReadinessHumanReviewReference
    blocked_output_reference: DecisionReadinessBlockedOutputReference
    unavailable_response: DecisionReadinessUnavailableResponse
    planning_only: bool = True
    readiness_status_generated: bool = False
    recommendation_generated: bool = False
    action_generated: bool = False
    confidence_generated: bool = False
    decision_object_generated: bool = False
    approval_granted: bool = False
    override_granted: bool = False
    execution_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("response_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision readiness response placeholder text fields")

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
        return sanitize_decision_readiness_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def response_placeholder_must_fail_closed(self) -> DecisionReadinessResponsePlaceholder:
        if not self.planning_only:
            raise ValueError("Decision readiness response placeholders must remain planning-only")
        if self.readiness_status_generated:
            raise ValueError("readiness status generation is forbidden in Prompt 42")
        if self.recommendation_generated:
            raise ValueError("recommendations are forbidden in Prompt 42")
        if self.action_generated:
            raise ValueError("action generation is forbidden in Prompt 42")
        if self.confidence_generated:
            raise ValueError("confidence scoring is forbidden in Prompt 42")
        if self.decision_object_generated:
            raise ValueError("DecisionObject generation is forbidden in Prompt 42")
        if self.approval_granted:
            raise ValueError("approval cannot be granted in Prompt 42")
        if self.override_granted:
            raise ValueError("override cannot be granted in Prompt 42")
        if self.execution_ready:
            raise ValueError("execution readiness is forbidden in Prompt 42")
        return self


def create_decision_readiness_response_placeholder(
    response_id: str,
    request_id: str | None = None,
    evidence_reference: DecisionReadinessEvidenceReference | None = None,
    safety_reference: DecisionReadinessSafetyReference | None = None,
    human_review_reference: DecisionReadinessHumanReviewReference | None = None,
    blocked_output_reference: DecisionReadinessBlockedOutputReference | None = None,
    unavailable_response: DecisionReadinessUnavailableResponse | None = None,
    notes: list[str] | None = None,
) -> DecisionReadinessResponsePlaceholder:
    resolved_unavailable = unavailable_response or default_decision_readiness_unavailable_response(
        request_id=request_id
    )
    return DecisionReadinessResponsePlaceholder(
        response_id=response_id,
        request_id=request_id,
        evidence_reference=evidence_reference or default_decision_readiness_evidence_reference(),
        safety_reference=safety_reference or default_decision_readiness_safety_reference(),
        human_review_reference=human_review_reference or default_decision_readiness_human_review_reference(),
        blocked_output_reference=blocked_output_reference or default_decision_readiness_blocked_output_reference(),
        unavailable_response=resolved_unavailable,
        notes=list(notes or ["Readiness response placeholder contains no generated outputs."]),
    )


def default_decision_readiness_response_placeholder() -> DecisionReadinessResponsePlaceholder:
    return create_decision_readiness_response_placeholder(
        response_id="decision-readiness-response-placeholder-v1",
    )
