from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.domain.enums import (
    ActionState,
    ConfidenceMethod,
    DecisionSource,
    MarketSegment,
    RiskLevel,
)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class DecisionObject(BaseModel):
    instrument: str
    exchange: str
    segment: MarketSegment
    timeframe: str
    regime: str | None = None
    state: str | None = None
    action_state: ActionState
    confidence: float = Field(ge=0, le=100)
    confidence_method: ConfidenceMethod = ConfidenceMethod.UNKNOWN
    risk: RiskLevel
    evidence: list[str] = Field(default_factory=list)
    invalidation: str | None = None
    horizon: str | None = None
    source_data_reference: str | None = None
    decision_source: DecisionSource = DecisionSource.UNKNOWN
    audit_id: str | None = None
    model_or_rule_version: str | None = None
    generated_at: datetime = Field(default_factory=utc_now)

    @field_validator("generated_at")
    @classmethod
    def generated_at_must_be_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @model_validator(mode="after")
    def directional_action_states_require_evidence(self) -> DecisionObject:
        directional_states = {
            ActionState.BUY_BIAS,
            ActionState.STRONG_BUY_BIAS,
            ActionState.SELL_BIAS,
            ActionState.STRONG_SELL_BIAS,
        }
        if self.action_state in directional_states and not self.evidence:
            raise ValueError("directional action states require evidence")
        return self
