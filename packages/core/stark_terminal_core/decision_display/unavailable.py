from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_display.contracts import (
    DecisionDisplaySafetyLabel,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_decision_display_notes,
)


class DecisionDisplayUnavailableResponse(BaseModel):
    response_id: str
    unavailable: bool = True
    message: str
    planning_only: bool = True
    display_contract_only: bool = True
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    readiness_to_trade_allowed: bool = False
    execution_allowed: bool = False
    approval_granted: bool = False
    override_granted: bool = False
    safety_label: DecisionDisplaySafetyLabel = DecisionDisplaySafetyLabel.UNAVAILABLE
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("response_id", "message", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision display unavailable response text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_display_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def unavailable_response_must_fail_closed(self) -> DecisionDisplayUnavailableResponse:
        if not self.unavailable:
            raise ValueError("Decision display responses must be unavailable in Prompt 43")
        if not self.planning_only:
            raise ValueError("Decision display responses must remain planning-only")
        if not self.display_contract_only:
            raise ValueError("Decision display responses must remain display-contract-only")
        if self.recommendations_allowed:
            raise ValueError("recommendations are forbidden in Prompt 43")
        if self.action_generation_allowed:
            raise ValueError("action generation is forbidden in Prompt 43")
        if self.confidence_scoring_allowed:
            raise ValueError("confidence scoring is forbidden in Prompt 43")
        if self.decision_object_generation_allowed:
            raise ValueError("DecisionObject generation is forbidden in Prompt 43")
        if self.readiness_to_trade_allowed:
            raise ValueError("readiness-to-trade is forbidden in Prompt 43")
        if self.execution_allowed:
            raise ValueError("execution is forbidden in Prompt 43")
        if self.approval_granted:
            raise ValueError("approval cannot be granted in Prompt 43")
        if self.override_granted:
            raise ValueError("override cannot be granted in Prompt 43")
        if self.safety_label == DecisionDisplaySafetyLabel.UNKNOWN:
            raise ValueError("decision display safety label cannot be UNKNOWN")
        return self


def default_decision_display_unavailable_response() -> DecisionDisplayUnavailableResponse:
    return DecisionDisplayUnavailableResponse(
        response_id="decision-display-unavailable-response-v1",
        message=(
            "Decision Display is a display contract skeleton only and returns unavailable "
            "responses in Prompt 43."
        ),
        notes=["Unavailable-by-default; not readiness-to-trade and not a recommendation."],
    )

