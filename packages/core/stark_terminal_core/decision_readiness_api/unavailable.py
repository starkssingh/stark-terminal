from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_readiness_api.requests import (
    DecisionReadinessSafetyLabel,
    DecisionReadinessUnavailableReason,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_decision_readiness_notes,
)


class DecisionReadinessUnavailableResponse(BaseModel):
    response_id: str
    request_id: str | None = None
    unavailable: bool = True
    reason: DecisionReadinessUnavailableReason
    message: str
    planning_only: bool = True
    readiness_status_available: bool = False
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    execution_allowed: bool = False
    approval_granted: bool = False
    override_granted: bool = False
    safety_label: DecisionReadinessSafetyLabel = DecisionReadinessSafetyLabel.UNAVAILABLE
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("response_id", "message", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision readiness unavailable response text fields")

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
    def unavailable_response_must_fail_closed(self) -> DecisionReadinessUnavailableResponse:
        if not self.unavailable:
            raise ValueError("Decision readiness API skeleton responses must be unavailable in Prompt 42")
        if self.reason == DecisionReadinessUnavailableReason.UNKNOWN:
            raise ValueError("UNKNOWN unavailable reason is not allowed")
        if not self.planning_only:
            raise ValueError("Decision readiness API skeleton responses must remain planning-only")
        if self.readiness_status_available:
            raise ValueError("readiness status generation is forbidden in Prompt 42")
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
        if self.approval_granted:
            raise ValueError("approval cannot be granted in Prompt 42")
        if self.override_granted:
            raise ValueError("override cannot be granted in Prompt 42")
        if self.safety_label == DecisionReadinessSafetyLabel.UNKNOWN:
            raise ValueError("decision readiness safety label cannot be UNKNOWN")
        return self


def create_decision_readiness_unavailable_response(
    response_id: str,
    reason: DecisionReadinessUnavailableReason = DecisionReadinessUnavailableReason.CONTRACT_SKELETON_ONLY,
    request_id: str | None = None,
    message: str = (
        "Decision Readiness API is a readiness contract skeleton only and returns unavailable "
        "responses in Prompt 42."
    ),
    notes: list[str] | None = None,
) -> DecisionReadinessUnavailableResponse:
    return DecisionReadinessUnavailableResponse(
        response_id=response_id,
        request_id=request_id,
        reason=reason,
        message=message,
        notes=list(notes or ["Unavailable-by-default; not readiness-to-trade and not a recommendation."]),
    )


def default_decision_readiness_unavailable_response(
    request_id: str | None = None,
) -> DecisionReadinessUnavailableResponse:
    return create_decision_readiness_unavailable_response(
        response_id="decision-readiness-unavailable-response-v1",
        request_id=request_id,
    )
