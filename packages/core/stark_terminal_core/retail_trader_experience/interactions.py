from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_trader_experience.planning import (
    RetailTraderExperienceForbiddenInteractionKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_trader_experience_notes,
)


class RetailTraderExperienceForbiddenInteraction(BaseModel):
    interaction_id: str
    kind: RetailTraderExperienceForbiddenInteractionKind
    name: str
    description: str
    forbidden_now: bool = True
    requires_future_prompt: bool = True
    requires_audit_before_unlock: bool = True
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("interaction_id", "name", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience forbidden interaction text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_trader_experience_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def forbidden_interaction_must_fail_closed(self) -> RetailTraderExperienceForbiddenInteraction:
        if self.kind == RetailTraderExperienceForbiddenInteractionKind.UNKNOWN:
            raise ValueError("UNKNOWN retail trader experience forbidden interaction kind is not allowed")
        if not self.forbidden_now:
            raise ValueError("retail trader experience forbidden interactions cannot be unlocked in Prompt 56")
        if not self.requires_future_prompt:
            raise ValueError("retail trader experience forbidden interactions require a future prompt before unlock")
        if not self.requires_audit_before_unlock:
            raise ValueError("retail trader experience forbidden interactions require audit before unlock")
        return self


def default_retail_trader_experience_forbidden_interactions() -> list[RetailTraderExperienceForbiddenInteraction]:
    specs = [
        (RetailTraderExperienceForbiddenInteractionKind.RECOMMENDATION_CARD, "Recommendation card"),
        (RetailTraderExperienceForbiddenInteractionKind.ACTION_BUTTON, "Action button"),
        (RetailTraderExperienceForbiddenInteractionKind.CONFIDENCE_SCORE, "Confidence score"),
        (RetailTraderExperienceForbiddenInteractionKind.DECISION_OBJECT_DISPLAY, "DecisionObject display"),
        (RetailTraderExperienceForbiddenInteractionKind.READINESS_TO_TRADE_BADGE, "Readiness-to-trade badge"),
        (RetailTraderExperienceForbiddenInteractionKind.BROKER_CONTROL, "Broker control"),
        (RetailTraderExperienceForbiddenInteractionKind.ORDER_BUTTON, "Order button"),
        (RetailTraderExperienceForbiddenInteractionKind.APPROVAL_CONTROL, "Approval control"),
        (RetailTraderExperienceForbiddenInteractionKind.OVERRIDE_CONTROL, "Override control"),
        (RetailTraderExperienceForbiddenInteractionKind.SUITABILITY_PROFILING, "Suitability profiling"),
        (RetailTraderExperienceForbiddenInteractionKind.LIVE_DATA_CONTROL, "Live data control"),
    ]
    return [
        RetailTraderExperienceForbiddenInteraction(
            interaction_id=f"retail-trader-experience-forbidden-{kind.value.lower().replace('_', '-')}-v1",
            kind=kind,
            name=name,
            description=f"{name} is forbidden in Prompt 56 Retail Trader Experience planning and guardrails.",
            notes=[
                "Requires a future prompt before unlock.",
                "Requires audit-before-unlock and does not enable active UI, suitability profiling, recommendation, broker control, or execution.",
            ],
        )
        for kind, name in specs
    ]
