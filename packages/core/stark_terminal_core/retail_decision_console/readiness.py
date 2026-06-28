from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_decision_console.productization import (
    non_empty_text,
    normalize_datetime,
    utc_now,
)


class RetailDecisionConsoleReadinessStatus(BaseModel):
    status_id: str = "retail-decision-console-readiness-v1"
    ready_for_productization_plan: bool = True
    ready_for_ui_shell_skeleton: bool = True
    ready_for_live_decisions: bool = False
    ready_for_recommendations: bool = False
    ready_for_action_generation: bool = False
    ready_for_confidence_scoring: bool = False
    ready_for_decision_object_generation: bool = False
    ready_for_live_market_data: bool = False
    ready_for_broker_controls: bool = False
    ready_for_order_buttons: bool = False
    ready_for_execution: bool = False
    next_allowed_phase: str = "ui_shell_skeleton"
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("status_id", "next_allowed_phase", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console readiness text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def readiness_must_not_allow_dangerous_capabilities(self) -> RetailDecisionConsoleReadinessStatus:
        if not self.ready_for_productization_plan or not self.ready_for_ui_shell_skeleton:
            raise ValueError("retail decision console must be ready for productization plan and UI shell skeleton")
        dangerous_readiness = {
            "live decisions": self.ready_for_live_decisions,
            "recommendations": self.ready_for_recommendations,
            "action generation": self.ready_for_action_generation,
            "confidence scoring": self.ready_for_confidence_scoring,
            "DecisionObject generation": self.ready_for_decision_object_generation,
            "live market data": self.ready_for_live_market_data,
            "broker controls": self.ready_for_broker_controls,
            "order buttons": self.ready_for_order_buttons,
            "execution": self.ready_for_execution,
        }
        enabled = [name for name, value in dangerous_readiness.items() if value]
        if enabled:
            raise ValueError("retail decision console readiness cannot allow: " + ", ".join(enabled))
        if self.next_allowed_phase != "ui_shell_skeleton":
            raise ValueError("retail decision console next phase must be ui_shell_skeleton")
        return self


def retail_decision_console_readiness(settings: object | None = None) -> RetailDecisionConsoleReadinessStatus:
    schema_version = getattr(settings, "retail_decision_console_schema_version", "v1")
    return RetailDecisionConsoleReadinessStatus(schema_version=schema_version)
