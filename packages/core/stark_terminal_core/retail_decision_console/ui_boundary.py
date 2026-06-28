from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_decision_console.productization import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)


ALLOWED_SHELL_CONCEPTS = (
    "app frame placeholder",
    "top navigation placeholder",
    "instrument selector placeholder",
    "timeframe selector placeholder",
    "status banner placeholder",
    "decision summary placeholder",
    "evidence panel placeholder",
    "risk/invalidation placeholder",
    "regime/state placeholder",
    "options context placeholder",
    "research context placeholder",
    "journal link placeholder",
    "settings link placeholder",
)

FORBIDDEN_SHELL_CAPABILITIES = (
    "active recommendation cards",
    "active buy/sell/hold/watch/avoid generation",
    "confidence scoring",
    "active DecisionObjects",
    "broker controls",
    "order buttons",
    "execution controls",
    "live market data claims",
)


class RetailDecisionConsoleUiShellBoundary(BaseModel):
    boundary_id: str
    service: str = "stark-terminal-retail-decision-console"
    stage: str = "productization_plan"
    schema_version: str = "v1"
    placeholder_only: bool = True
    read_only: bool = True
    allowed_shell_concepts: tuple[str, ...] = ALLOWED_SHELL_CONCEPTS
    forbidden_shell_capabilities: tuple[str, ...] = FORBIDDEN_SHELL_CAPABILITIES
    active_recommendation_cards_enabled: bool = False
    action_state_generation_enabled: bool = False
    confidence_scoring_enabled: bool = False
    active_decision_objects_enabled: bool = False
    broker_controls_enabled: bool = False
    order_buttons_enabled: bool = False
    execution_controls_enabled: bool = False
    live_market_data_claims_enabled: bool = False
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("boundary_id", "service", "stage", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console UI boundary text")

    @field_validator("allowed_shell_concepts", "forbidden_shell_capabilities")
    @classmethod
    def tuple_values_must_be_clean(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(sanitized_text_list(list(value)))

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def boundary_must_remain_placeholder_only(self) -> RetailDecisionConsoleUiShellBoundary:
        if not self.placeholder_only or not self.read_only:
            raise ValueError("retail decision console UI boundary must remain placeholder-only and read-only")
        dangerous_flags = {
            "active recommendation cards": self.active_recommendation_cards_enabled,
            "action state generation": self.action_state_generation_enabled,
            "confidence scoring": self.confidence_scoring_enabled,
            "active DecisionObjects": self.active_decision_objects_enabled,
            "broker controls": self.broker_controls_enabled,
            "order buttons": self.order_buttons_enabled,
            "execution controls": self.execution_controls_enabled,
            "live market data claims": self.live_market_data_claims_enabled,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("retail decision console UI boundary cannot enable: " + ", ".join(enabled))
        return self


def default_retail_decision_console_ui_boundary(
    settings: object | None = None,
) -> RetailDecisionConsoleUiShellBoundary:
    schema_version = getattr(settings, "retail_decision_console_schema_version", "v1")
    return RetailDecisionConsoleUiShellBoundary(
        boundary_id="retail-decision-console-ui-shell-boundary-v1",
        schema_version=schema_version,
        notes=[
            "Defines safe UI shell placeholders only.",
            "No live decisions, recommendations, confidence, broker controls, order buttons, or execution controls.",
        ],
    )
