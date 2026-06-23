from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_safety.guardrails import (
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_decision_safety_notes,
)


class DecisionOverrideProhibition(BaseModel):
    prohibition_id: str
    name: str
    description: str
    overrides_allowed: bool = False
    emergency_bypass_allowed: bool = False
    bypass_requires_future_prompt: bool = True
    blocks_recommendations: bool = True
    blocks_decision_object_generation: bool = True
    blocks_execution: bool = True
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("prohibition_id", "name", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "decision override prohibition text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_safety_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def prohibition_must_fail_closed(self) -> DecisionOverrideProhibition:
        if self.overrides_allowed:
            raise ValueError("overrides are forbidden in Prompt 39")
        if self.emergency_bypass_allowed:
            raise ValueError("emergency bypass is forbidden in Prompt 39")
        if not self.bypass_requires_future_prompt:
            raise ValueError("any bypass must require a future prompt and audit")
        if not self.blocks_recommendations:
            raise ValueError("override prohibitions must block recommendations")
        if not self.blocks_decision_object_generation:
            raise ValueError("override prohibitions must block DecisionObject generation")
        if not self.blocks_execution:
            raise ValueError("override prohibitions must block execution")
        return self


def default_decision_override_prohibitions() -> list[DecisionOverrideProhibition]:
    definitions = [
        (
            "decision-override-prohibition-default",
            "Default Override Prohibition",
            "Disallows manual override of decision safety blocked outputs in Prompt 39.",
        ),
        (
            "decision-override-prohibition-emergency-bypass",
            "Emergency Bypass Prohibition",
            "Confirms emergency bypass is not implemented and requires a future prompt and audit.",
        ),
    ]
    return [
        DecisionOverrideProhibition(
            prohibition_id=prohibition_id,
            name=name,
            description=description,
            notes=["Overrides prohibited; no bypass path exists in Prompt 39."],
        )
        for prohibition_id, name, description in definitions
    ]


def evaluate_decision_override_prohibitions(
    prohibitions: list[DecisionOverrideProhibition],
) -> list[str]:
    blockers: list[str] = []
    if not prohibitions:
        blockers.append("decision override prohibitions are missing")
    for prohibition in prohibitions:
        if prohibition.overrides_allowed:
            blockers.append(f"{prohibition.prohibition_id}: overrides cannot be allowed")
        if prohibition.emergency_bypass_allowed:
            blockers.append(f"{prohibition.prohibition_id}: emergency bypass cannot be allowed")
        if not prohibition.bypass_requires_future_prompt:
            blockers.append(f"{prohibition.prohibition_id}: bypass must require a future prompt")
    return blockers
