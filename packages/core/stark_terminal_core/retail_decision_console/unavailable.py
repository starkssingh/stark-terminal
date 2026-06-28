from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_decision_console.productization import (
    non_empty_text,
    normalize_datetime,
    utc_now,
)


class RetailDecisionConsoleUnavailableState(BaseModel):
    state_id: str = "retail-decision-console-unavailable-state-v1"
    unavailable: bool = True
    reason: str
    allowed_stage: str = "productization_plan"
    live_decisions_enabled: bool = False
    recommendations_enabled: bool = False
    action_generation_enabled: bool = False
    confidence_scoring_enabled: bool = False
    decision_object_generation_enabled: bool = False
    live_market_data_enabled: bool = False
    broker_controls_enabled: bool = False
    order_buttons_enabled: bool = False
    execution_enabled: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("state_id", "reason", "allowed_stage", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console unavailable state text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def unavailable_state_must_remain_blocking(self) -> RetailDecisionConsoleUnavailableState:
        if not self.unavailable:
            raise ValueError("retail decision console unavailable state must remain unavailable")
        if self.allowed_stage != "productization_plan":
            raise ValueError("retail decision console unavailable state must allow productization_plan only")
        dangerous_flags = {
            "live decisions": self.live_decisions_enabled,
            "recommendations": self.recommendations_enabled,
            "action generation": self.action_generation_enabled,
            "confidence scoring": self.confidence_scoring_enabled,
            "DecisionObject generation": self.decision_object_generation_enabled,
            "live market data": self.live_market_data_enabled,
            "broker controls": self.broker_controls_enabled,
            "order buttons": self.order_buttons_enabled,
            "execution": self.execution_enabled,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("retail decision console unavailable state cannot enable: " + ", ".join(enabled))
        return self


def unavailable_retail_decision_console_state(
    reason: str = "Retail Decision Console is unavailable until UI shell skeleton and decision validation are implemented.",
) -> RetailDecisionConsoleUnavailableState:
    return RetailDecisionConsoleUnavailableState(reason=reason)
