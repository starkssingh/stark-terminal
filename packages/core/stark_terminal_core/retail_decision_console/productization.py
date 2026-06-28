from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator


SERVICE_NAME = "stark-terminal-retail-decision-console"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def normalize_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def non_empty_text(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} cannot be empty")
    return normalized


def sanitized_text_list(value: list[str]) -> list[str]:
    normalized = [item.strip() for item in value if item.strip()]
    if len(normalized) != len(value):
        raise ValueError("text lists cannot contain empty values")
    return normalized


class RetailDecisionConsoleProductizationPlan(BaseModel):
    plan_id: str
    service: str = SERVICE_NAME
    stage: str = "productization_plan"
    schema_version: str = "v1"
    planning_only: bool = True
    productization_plan_only: bool = True
    read_only: bool = True
    unavailable_by_default: bool = True
    live_decisions_enabled: bool = False
    recommendations_enabled: bool = False
    action_generation_enabled: bool = False
    confidence_scoring_enabled: bool = False
    decision_object_generation_enabled: bool = False
    live_market_data_enabled: bool = False
    broker_controls_enabled: bool = False
    execution_enabled: bool = False
    order_buttons_enabled: bool = False
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("plan_id", "service", "stage", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console productization text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def plan_must_remain_safe(self) -> RetailDecisionConsoleProductizationPlan:
        if self.service != SERVICE_NAME:
            raise ValueError("retail decision console service name is fixed")
        if self.stage != "productization_plan":
            raise ValueError("retail decision console stage must be productization_plan")
        if not self.planning_only or not self.productization_plan_only or not self.read_only:
            raise ValueError("retail decision console must remain a read-only productization plan")
        if not self.unavailable_by_default:
            raise ValueError("retail decision console must remain unavailable by default")
        dangerous_flags = {
            "live decisions": self.live_decisions_enabled,
            "recommendations": self.recommendations_enabled,
            "action generation": self.action_generation_enabled,
            "confidence scoring": self.confidence_scoring_enabled,
            "DecisionObject generation": self.decision_object_generation_enabled,
            "live market data": self.live_market_data_enabled,
            "broker controls": self.broker_controls_enabled,
            "execution": self.execution_enabled,
            "order buttons": self.order_buttons_enabled,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("retail decision console productization cannot enable: " + ", ".join(enabled))
        return self


def default_retail_decision_console_productization_plan(
    settings: object | None = None,
) -> RetailDecisionConsoleProductizationPlan:
    schema_version = getattr(settings, "retail_decision_console_schema_version", "v1")
    return RetailDecisionConsoleProductizationPlan(
        plan_id="retail-decision-console-productization-plan-v1",
        schema_version=schema_version,
        notes=[
            "Defines the flagship Retail Decision Console product surface.",
            "Keeps all decision, recommendation, confidence, broker, and execution behavior disabled.",
        ],
    )
