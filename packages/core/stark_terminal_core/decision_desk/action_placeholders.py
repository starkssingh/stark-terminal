from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_desk.planning import (
    RetailDecisionDeskSafetyLabel,
    _non_empty_text,
    sanitize_decision_notes,
)


class RetailActionPlaceholder(StrEnum):
    BUY_BIAS = "BUY_BIAS"
    SELL_BIAS = "SELL_BIAS"
    HOLD = "HOLD"
    WATCH = "WATCH"
    AVOID = "AVOID"
    REDUCE = "REDUCE"
    UNKNOWN = "UNKNOWN"
    UNASSIGNED = "UNASSIGNED"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _utc_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


class RetailActionPlaceholderContract(BaseModel):
    placeholder_id: str
    action: RetailActionPlaceholder
    display_name: str
    description: str
    planning_only: bool = True
    generated_now: bool = False
    recommendation: bool = False
    trade_signal: bool = False
    decision_object_generated: bool = False
    execution_ready: bool = False
    safety_label: RetailDecisionDeskSafetyLabel = RetailDecisionDeskSafetyLabel.PLANNING_ONLY
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("placeholder_id", "display_name", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail action placeholder text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def placeholder_must_remain_inactive(self) -> RetailActionPlaceholderContract:
        if self.action == RetailActionPlaceholder.UNKNOWN:
            raise ValueError("retail action placeholder cannot be UNKNOWN")
        if not self.planning_only:
            raise ValueError("retail action placeholders must remain planning-only in Prompt 36")
        if self.generated_now:
            raise ValueError("action-state generation is forbidden in Prompt 36")
        if self.recommendation:
            raise ValueError("action placeholders cannot be recommendations")
        if self.trade_signal:
            raise ValueError("action placeholders cannot be trade signals")
        if self.decision_object_generated:
            raise ValueError("action placeholders cannot generate DecisionObjects")
        if self.execution_ready:
            raise ValueError("action placeholders cannot be execution-ready")
        if self.safety_label == RetailDecisionDeskSafetyLabel.UNKNOWN:
            raise ValueError("retail decision desk safety label cannot be UNKNOWN")
        return self


def create_retail_action_placeholder_contract(
    placeholder_id: str,
    action: RetailActionPlaceholder,
    display_name: str,
    description: str,
) -> RetailActionPlaceholderContract:
    return RetailActionPlaceholderContract(
        placeholder_id=placeholder_id,
        action=action,
        display_name=display_name,
        description=description,
    )


def default_retail_action_placeholder_contracts() -> list[RetailActionPlaceholderContract]:
    placeholder_descriptions = {
        RetailActionPlaceholder.BUY_BIAS: "Planning placeholder for a possible future display category; not generated in Prompt 36.",
        RetailActionPlaceholder.SELL_BIAS: "Planning placeholder for a possible future display category; not generated in Prompt 36.",
        RetailActionPlaceholder.HOLD: "Planning placeholder for a possible future display category; not generated in Prompt 36.",
        RetailActionPlaceholder.WATCH: "Planning placeholder for a possible future display category; not generated in Prompt 36.",
        RetailActionPlaceholder.AVOID: "Planning placeholder for a possible future display category; not generated in Prompt 36.",
        RetailActionPlaceholder.REDUCE: "Planning placeholder for a possible future display category; not generated in Prompt 36.",
    }
    return [
        create_retail_action_placeholder_contract(
            placeholder_id=f"retail-action-placeholder-{action.value.lower().replace('_', '-')}",
            action=action,
            display_name=action.value.replace("_", " ").title(),
            description=description,
        )
        for action, description in placeholder_descriptions.items()
    ]


def placeholder_names(placeholders: list[RetailActionPlaceholderContract] | None = None) -> list[str]:
    resolved = placeholders or default_retail_action_placeholder_contracts()
    return sanitize_decision_notes([placeholder.action.value for placeholder in resolved])
