from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_trader_experience_display.contracts import (
    RetailTraderExperienceDisplayPersonaKind,
    RetailTraderExperienceDisplaySafetyLabel,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_retail_trader_experience_display_notes,
)


class RetailTraderExperienceDisplayPersonaPlaceholder(BaseModel):
    persona_id: str
    persona_kind: RetailTraderExperienceDisplayPersonaKind
    name: str
    description: str
    display_contract_only: bool = True
    active_ui: bool = False
    rendered_now: bool = False
    suitability_profile: bool = False
    trading_permission_profile: bool = False
    recommendations_allowed: bool = False
    action_generation_allowed: bool = False
    confidence_scoring_allowed: bool = False
    decision_object_generation_allowed: bool = False
    readiness_to_trade_allowed: bool = False
    broker_controls_allowed: bool = False
    execution_allowed: bool = False
    safety_label: RetailTraderExperienceDisplaySafetyLabel = (
        RetailTraderExperienceDisplaySafetyLabel.NOT_SUITABILITY_PROFILING
    )
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("persona_id", "name", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience display persona text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_retail_trader_experience_display_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def persona_placeholder_must_fail_closed(self) -> RetailTraderExperienceDisplayPersonaPlaceholder:
        if self.persona_kind == RetailTraderExperienceDisplayPersonaKind.UNKNOWN:
            raise ValueError("UNKNOWN Retail Trader Experience Display persona kind is not allowed")
        if not self.display_contract_only:
            raise ValueError("Retail Trader Experience Display persona must remain display-contract-only")
        if self.active_ui or self.rendered_now:
            raise ValueError("Retail Trader Experience Display persona cannot be active or rendered")
        if self.suitability_profile or self.trading_permission_profile:
            raise ValueError("Retail Trader Experience Display persona cannot be suitability or permission profiling")
        if (
            self.recommendations_allowed
            or self.action_generation_allowed
            or self.confidence_scoring_allowed
            or self.decision_object_generation_allowed
            or self.readiness_to_trade_allowed
            or self.broker_controls_allowed
            or self.execution_allowed
        ):
            raise ValueError("Retail Trader Experience Display persona dangerous flags must be false")
        if self.safety_label == RetailTraderExperienceDisplaySafetyLabel.UNKNOWN:
            raise ValueError("Retail Trader Experience Display persona safety label cannot be UNKNOWN")
        return self


def default_retail_trader_experience_display_persona_placeholders() -> list[
    RetailTraderExperienceDisplayPersonaPlaceholder
]:
    return [
        RetailTraderExperienceDisplayPersonaPlaceholder(
            persona_id="retail-trader-visual-placeholder",
            persona_kind=RetailTraderExperienceDisplayPersonaKind.RETAIL_TRADER_VISUAL_PLACEHOLDER,
            name="Retail trader visual placeholder",
            description="Display contract placeholder only; not active personalization or suitability profiling.",
        ),
        RetailTraderExperienceDisplayPersonaPlaceholder(
            persona_id="intraday-trader-visual-placeholder",
            persona_kind=RetailTraderExperienceDisplayPersonaKind.INTRADAY_TRADER_VISUAL_PLACEHOLDER,
            name="Intraday trader visual placeholder",
            description="Placeholder only; not trading advice, recommendation behavior, or execution permission.",
        ),
        RetailTraderExperienceDisplayPersonaPlaceholder(
            persona_id="swing-trader-visual-placeholder",
            persona_kind=RetailTraderExperienceDisplayPersonaKind.SWING_TRADER_VISUAL_PLACEHOLDER,
            name="Swing trader visual placeholder",
            description="Placeholder only; no action generation, confidence scoring, or broker linkage.",
        ),
        RetailTraderExperienceDisplayPersonaPlaceholder(
            persona_id="options-context-visual-placeholder",
            persona_kind=RetailTraderExperienceDisplayPersonaKind.OPTIONS_CONTEXT_VISUAL_PLACEHOLDER,
            name="Options context visual placeholder",
            description="Placeholder only; no options recommendation, pricing, strategy, or execution control.",
        ),
        RetailTraderExperienceDisplayPersonaPlaceholder(
            persona_id="risk-aware-beginner-visual-placeholder",
            persona_kind=RetailTraderExperienceDisplayPersonaKind.RISK_AWARE_BEGINNER_VISUAL_PLACEHOLDER,
            name="Risk-aware beginner visual placeholder",
            description="Placeholder only; not a suitability profile or trading permission profile.",
        ),
        RetailTraderExperienceDisplayPersonaPlaceholder(
            persona_id="quant-curious-trader-visual-placeholder",
            persona_kind=RetailTraderExperienceDisplayPersonaKind.QUANT_CURIOUS_TRADER_VISUAL_PLACEHOLDER,
            name="Quant-curious trader visual placeholder",
            description="Placeholder only; no model signal, feature computation, or DecisionObject display.",
        ),
    ]
