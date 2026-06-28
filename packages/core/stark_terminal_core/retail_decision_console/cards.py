from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_decision_console.productization import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)


class RetailDecisionConsoleCardKind(StrEnum):
    DECISION_BIAS = "DECISION_BIAS"
    EVIDENCE = "EVIDENCE"
    RISK = "RISK"
    INVALIDATION = "INVALIDATION"
    REGIME = "REGIME"
    OPTIONS_CONTEXT = "OPTIONS_CONTEXT"
    RESEARCH_CONTEXT = "RESEARCH_CONTEXT"


class RetailDecisionConsoleCardPlaceholder(BaseModel):
    card_id: str
    card_kind: RetailDecisionConsoleCardKind
    label: str
    description: str
    display_planning_only: bool = True
    read_only: bool = True
    generated_recommendations_enabled: bool = False
    generated_confidence_scores_enabled: bool = False
    active_decision_objects_enabled: bool = False
    live_market_data_enabled: bool = False
    broker_controls_enabled: bool = False
    execution_controls_enabled: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("card_id", "label", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console card text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def card_must_not_display_active_behavior(self) -> RetailDecisionConsoleCardPlaceholder:
        if not self.display_planning_only or not self.read_only:
            raise ValueError("retail decision console cards must remain display planning placeholders")
        dangerous_flags = {
            "generated recommendations": self.generated_recommendations_enabled,
            "generated confidence scores": self.generated_confidence_scores_enabled,
            "active DecisionObjects": self.active_decision_objects_enabled,
            "live market data": self.live_market_data_enabled,
            "broker controls": self.broker_controls_enabled,
            "execution controls": self.execution_controls_enabled,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("retail decision console card cannot enable: " + ", ".join(enabled))
        return self


class DecisionBiasCardPlaceholder(RetailDecisionConsoleCardPlaceholder):
    card_kind: RetailDecisionConsoleCardKind = RetailDecisionConsoleCardKind.DECISION_BIAS


class EvidenceCardPlaceholder(RetailDecisionConsoleCardPlaceholder):
    card_kind: RetailDecisionConsoleCardKind = RetailDecisionConsoleCardKind.EVIDENCE


class RiskCardPlaceholder(RetailDecisionConsoleCardPlaceholder):
    card_kind: RetailDecisionConsoleCardKind = RetailDecisionConsoleCardKind.RISK


class InvalidationCardPlaceholder(RetailDecisionConsoleCardPlaceholder):
    card_kind: RetailDecisionConsoleCardKind = RetailDecisionConsoleCardKind.INVALIDATION


class RegimeCardPlaceholder(RetailDecisionConsoleCardPlaceholder):
    card_kind: RetailDecisionConsoleCardKind = RetailDecisionConsoleCardKind.REGIME


class OptionsContextCardPlaceholder(RetailDecisionConsoleCardPlaceholder):
    card_kind: RetailDecisionConsoleCardKind = RetailDecisionConsoleCardKind.OPTIONS_CONTEXT


class ResearchContextCardPlaceholder(RetailDecisionConsoleCardPlaceholder):
    card_kind: RetailDecisionConsoleCardKind = RetailDecisionConsoleCardKind.RESEARCH_CONTEXT


def default_retail_decision_console_card_placeholders() -> list[RetailDecisionConsoleCardPlaceholder]:
    return [
        DecisionBiasCardPlaceholder(
            card_id="decision-bias-card-placeholder",
            label="Decision bias card placeholder",
            description="Unavailable bias card placeholder; no generated buy/sell/hold/watch/avoid output.",
        ),
        EvidenceCardPlaceholder(
            card_id="evidence-card-placeholder",
            label="Evidence card placeholder",
            description="Evidence card shell placeholder; no validated evidence bundle displayed.",
        ),
        RiskCardPlaceholder(
            card_id="risk-card-placeholder",
            label="Risk card placeholder",
            description="Risk card shell placeholder; no live risk computation.",
        ),
        InvalidationCardPlaceholder(
            card_id="invalidation-card-placeholder",
            label="Invalidation card placeholder",
            description="Invalidation card shell placeholder; no live invalidation state.",
        ),
        RegimeCardPlaceholder(
            card_id="regime-card-placeholder",
            label="Regime card placeholder",
            description="Regime card shell placeholder; no active regime classification.",
        ),
        OptionsContextCardPlaceholder(
            card_id="options-context-card-placeholder",
            label="Options context card placeholder",
            description="Options context shell placeholder; no options recommendation.",
        ),
        ResearchContextCardPlaceholder(
            card_id="research-context-card-placeholder",
            label="Research context card placeholder",
            description="Research card shell placeholder; no retrieval or generated strategy.",
        ),
    ]
