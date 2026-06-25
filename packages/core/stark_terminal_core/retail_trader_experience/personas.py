from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_trader_experience.planning import (
    RetailTraderExperienceSafetyLabel,
    RetailTraderPersonaKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_trader_experience_notes,
)


class RetailTraderPersonaPlaceholder(BaseModel):
    persona_id: str
    persona_kind: RetailTraderPersonaKind
    name: str
    description: str
    planning_only: bool = True
    active_profile: bool = False
    suitability_profile: bool = False
    trading_permission_profile: bool = False
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    readiness_to_trade_allowed: bool = False
    broker_controls_allowed: bool = False
    execution_allowed: bool = False
    safety_label: RetailTraderExperienceSafetyLabel = RetailTraderExperienceSafetyLabel.NOT_SUITABILITY_PROFILING
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("persona_id", "name", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader persona text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_trader_experience_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def persona_placeholder_must_fail_closed(self) -> RetailTraderPersonaPlaceholder:
        if self.persona_kind == RetailTraderPersonaKind.UNKNOWN:
            raise ValueError("UNKNOWN retail trader persona kind is not allowed")
        if not self.planning_only:
            raise ValueError("retail trader persona placeholder must remain planning-only")
        if self.active_profile:
            raise ValueError("retail trader persona placeholder cannot be an active profile")
        if self.suitability_profile:
            raise ValueError("retail trader suitability profiling is forbidden")
        if self.trading_permission_profile:
            raise ValueError("retail trader trading permission profiling is forbidden")
        if self.recommendations_allowed:
            raise ValueError("retail trader persona placeholder cannot allow recommendations")
        if self.action_generation_allowed:
            raise ValueError("retail trader persona placeholder cannot allow action generation")
        if self.confidence_scoring_allowed:
            raise ValueError("retail trader persona placeholder cannot allow confidence scoring")
        if self.decision_object_generation_allowed:
            raise ValueError("retail trader persona placeholder cannot allow DecisionObject generation")
        if self.readiness_to_trade_allowed:
            raise ValueError("retail trader persona placeholder cannot allow readiness-to-trade")
        if self.broker_controls_allowed:
            raise ValueError("retail trader persona placeholder cannot allow broker controls")
        if self.execution_allowed:
            raise ValueError("retail trader persona placeholder cannot allow execution")
        if self.safety_label == RetailTraderExperienceSafetyLabel.UNKNOWN:
            raise ValueError("retail trader persona safety label cannot be UNKNOWN")
        return self


def default_retail_trader_persona_placeholders() -> list[RetailTraderPersonaPlaceholder]:
    specs = [
        (
            "retail-trader-persona-retail-placeholder-v1",
            RetailTraderPersonaKind.RETAIL_TRADER_PLACEHOLDER,
            "Retail Trader Placeholder",
            "Planning-only retail trader context placeholder with no suitability profile.",
        ),
        (
            "retail-trader-persona-intraday-placeholder-v1",
            RetailTraderPersonaKind.INTRADAY_TRADER_PLACEHOLDER,
            "Intraday Trader Placeholder",
            "Planning-only intraday context placeholder with no trading permission profile.",
        ),
        (
            "retail-trader-persona-swing-placeholder-v1",
            RetailTraderPersonaKind.SWING_TRADER_PLACEHOLDER,
            "Swing Trader Placeholder",
            "Planning-only swing trading context placeholder with no recommendation behavior.",
        ),
        (
            "retail-trader-persona-options-placeholder-v1",
            RetailTraderPersonaKind.OPTIONS_CONTEXT_PLACEHOLDER,
            "Options Context Placeholder",
            "Planning-only options context placeholder with no suitability or execution behavior.",
        ),
        (
            "retail-trader-persona-beginner-placeholder-v1",
            RetailTraderPersonaKind.RISK_AWARE_BEGINNER_PLACEHOLDER,
            "Risk Aware Beginner Placeholder",
            "Planning-only education context placeholder with no active personalization.",
        ),
        (
            "retail-trader-persona-quant-curious-placeholder-v1",
            RetailTraderPersonaKind.QUANT_CURIOUS_TRADER_PLACEHOLDER,
            "Quant Curious Trader Placeholder",
            "Planning-only quant context placeholder with no active profile or recommendation.",
        ),
    ]
    return [
        RetailTraderPersonaPlaceholder(
            persona_id=persona_id,
            persona_kind=persona_kind,
            name=name,
            description=description,
            notes=["Persona placeholder is not suitability profiling, active personalization, or trading permissioning."],
        )
        for persona_id, persona_kind, name, description in specs
    ]
