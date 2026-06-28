from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_decision_console.productization import (
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)


class ConsoleNavigationItemPlaceholder(BaseModel):
    item_id: str
    label: str
    target_placeholder: str
    placeholder_only: bool = True
    launch_execution_enabled: bool = False
    broker_controls_enabled: bool = False
    active_trading_implied: bool = False
    recommendation_trigger_enabled: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("item_id", "label", "target_placeholder", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console navigation item text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def item_must_not_trigger_active_behavior(self) -> ConsoleNavigationItemPlaceholder:
        if not self.placeholder_only:
            raise ValueError("navigation items must remain placeholders")
        dangerous_flags = {
            "launch execution": self.launch_execution_enabled,
            "broker controls": self.broker_controls_enabled,
            "active trading implication": self.active_trading_implied,
            "recommendation trigger": self.recommendation_trigger_enabled,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("retail decision console navigation item cannot enable: " + ", ".join(enabled))
        return self


class RetailDecisionConsoleNavigationPlaceholder(BaseModel):
    navigation_id: str
    label: str
    items: list[ConsoleNavigationItemPlaceholder]
    placeholder_only: bool = True
    read_only: bool = True
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("navigation_id", "label", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console navigation text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def navigation_must_remain_placeholder_only(self) -> RetailDecisionConsoleNavigationPlaceholder:
        if not self.placeholder_only or not self.read_only:
            raise ValueError("navigation must remain read-only placeholder metadata")
        if not self.items:
            raise ValueError("navigation must include placeholder items")
        return self


def default_retail_decision_console_navigation_placeholder() -> RetailDecisionConsoleNavigationPlaceholder:
    return RetailDecisionConsoleNavigationPlaceholder(
        navigation_id="retail-decision-console-navigation-placeholder-v1",
        label="Retail Decision Console navigation placeholder",
        items=[
            ConsoleNavigationItemPlaceholder(
                item_id="console-nav-decision-summary",
                label="Decision Summary",
                target_placeholder="decision-summary-section-placeholder",
            ),
            ConsoleNavigationItemPlaceholder(
                item_id="console-nav-evidence",
                label="Evidence",
                target_placeholder="evidence-section-placeholder",
            ),
            ConsoleNavigationItemPlaceholder(
                item_id="console-nav-risk",
                label="Risk / Invalidation",
                target_placeholder="risk-invalidation-section-placeholder",
            ),
            ConsoleNavigationItemPlaceholder(
                item_id="console-nav-research",
                label="Research Context",
                target_placeholder="research-context-section-placeholder",
            ),
        ],
        notes=["Navigation is placeholder-only and cannot trigger recommendations, broker controls, or execution."],
    )
