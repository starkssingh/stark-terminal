from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_decision_console.productization import (
    SERVICE_NAME,
    non_empty_text,
    normalize_datetime,
    utc_now,
)


STATIC_INTERACTION_STAGE = "static_interaction_placeholders"


class RetailDecisionConsoleInteractionType(StrEnum):
    SECTION_TOGGLE = "SECTION_TOGGLE"
    STATIC_TAB_SELECT = "STATIC_TAB_SELECT"
    SHOW_UNAVAILABLE_REASON = "SHOW_UNAVAILABLE_REASON"
    SHOW_PROVENANCE_LABEL = "SHOW_PROVENANCE_LABEL"
    SHOW_SAFETY_INFO = "SHOW_SAFETY_INFO"
    LOCAL_PLACEHOLDER_REFRESH = "LOCAL_PLACEHOLDER_REFRESH"
    STATIC_INSTRUMENT_PLACEHOLDER_SELECT = "STATIC_INSTRUMENT_PLACEHOLDER_SELECT"
    STATIC_TIMEFRAME_PLACEHOLDER_SELECT = "STATIC_TIMEFRAME_PLACEHOLDER_SELECT"


FORBIDDEN_RETAIL_DECISION_CONSOLE_INTERACTION_TYPES: tuple[str, ...] = (
    "LIVE_DATA_REFRESH",
    "RECOMMENDATION_REFRESH",
    "ACTION_GENERATION",
    "CONFIDENCE_RECALCULATION",
    "DECISION_OBJECT_GENERATION",
    "BROKER_CONNECT",
    "ORDER_PREVIEW",
    "ORDER_PLACE",
    "EXECUTION",
    "APPROVAL",
    "OVERRIDE",
    "AUTO_TRADE",
)


def _enabled_flags(flags: dict[str, bool]) -> list[str]:
    return [name for name, value in flags.items() if value]


def _safe_flag_snapshot() -> dict[str, bool]:
    return {
        "live_data_enabled": False,
        "recommendations_enabled": False,
        "action_generation_enabled": False,
        "confidence_scoring_enabled": False,
        "decision_object_generation_enabled": False,
        "broker_controls_enabled": False,
        "order_buttons_enabled": False,
        "execution_enabled": False,
    }


class RetailDecisionConsoleInteractionDescriptor(BaseModel):
    interaction_id: str
    label: str
    interaction_type: RetailDecisionConsoleInteractionType
    target_section_id: str
    demo_only: bool = True
    unavailable: bool = True
    local_only: bool = True
    read_only: bool = True
    live_data_enabled: bool = False
    recommendations_enabled: bool = False
    action_generation_enabled: bool = False
    confidence_scoring_enabled: bool = False
    decision_object_generation_enabled: bool = False
    broker_controls_enabled: bool = False
    order_buttons_enabled: bool = False
    execution_enabled: bool = False
    safety_note: str = (
        "Static demo placeholder only; no live data, no recommendation, no action generation, "
        "no confidence score, no DecisionObject, no order control, no execution."
    )
    safety_flags: dict[str, bool] = Field(default_factory=_safe_flag_snapshot)
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("interaction_type", mode="before")
    @classmethod
    def interaction_type_must_be_allowed(cls, value: object) -> object:
        raw_value = value.value if isinstance(value, StrEnum) else str(value)
        normalized = raw_value.strip().upper()
        if normalized in FORBIDDEN_RETAIL_DECISION_CONSOLE_INTERACTION_TYPES:
            raise ValueError("retail decision console interaction type is forbidden")
        return value

    @field_validator("interaction_id", "label", "target_section_id", "safety_note")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console interaction text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def interaction_must_remain_static_safe(self) -> RetailDecisionConsoleInteractionDescriptor:
        if not self.demo_only or not self.unavailable or not self.local_only or not self.read_only:
            raise ValueError("retail decision console interactions must remain demo, unavailable, local, and read-only")
        enabled = _enabled_flags(
            {
                **self.safety_flags,
                "live data": self.live_data_enabled,
                "recommendations": self.recommendations_enabled,
                "action generation": self.action_generation_enabled,
                "confidence scoring": self.confidence_scoring_enabled,
                "DecisionObject generation": self.decision_object_generation_enabled,
                "broker controls": self.broker_controls_enabled,
                "order buttons": self.order_buttons_enabled,
                "execution": self.execution_enabled,
            }
        )
        if enabled:
            raise ValueError("retail decision console interaction cannot enable: " + ", ".join(enabled))
        return self


class RetailDecisionConsoleInteractionState(BaseModel):
    interaction_state_id: str = "retail-decision-console-static-interactions-v1"
    service: str = SERVICE_NAME
    schema_version: str = "v1"
    stage: str = STATIC_INTERACTION_STAGE
    static_interaction_placeholders_only: bool = True
    demo_only: bool = True
    unavailable: bool = True
    local_only: bool = True
    read_only: bool = True
    interactions: list[RetailDecisionConsoleInteractionDescriptor]
    live_data_enabled: bool = False
    recommendations_enabled: bool = False
    action_generation_enabled: bool = False
    confidence_scoring_enabled: bool = False
    decision_object_generation_enabled: bool = False
    broker_controls_enabled: bool = False
    order_buttons_enabled: bool = False
    execution_enabled: bool = False
    safety_flags: dict[str, bool] = Field(default_factory=_safe_flag_snapshot)
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("interaction_state_id", "service", "schema_version", "stage")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console interaction state text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def interaction_state_must_remain_static_safe(self) -> RetailDecisionConsoleInteractionState:
        if self.stage != STATIC_INTERACTION_STAGE:
            raise ValueError("retail decision console interaction stage must be static_interaction_placeholders")
        if not self.interactions:
            raise ValueError("retail decision console interaction state requires interactions")
        if not (
            self.static_interaction_placeholders_only
            and self.demo_only
            and self.unavailable
            and self.local_only
            and self.read_only
        ):
            raise ValueError("retail decision console interaction state must remain static/demo/local/read-only")
        enabled = _enabled_flags(
            {
                **self.safety_flags,
                "live data": self.live_data_enabled,
                "recommendations": self.recommendations_enabled,
                "action generation": self.action_generation_enabled,
                "confidence scoring": self.confidence_scoring_enabled,
                "DecisionObject generation": self.decision_object_generation_enabled,
                "broker controls": self.broker_controls_enabled,
                "order buttons": self.order_buttons_enabled,
                "execution": self.execution_enabled,
            }
        )
        if enabled:
            raise ValueError("retail decision console interaction state cannot enable: " + ", ".join(enabled))
        return self


def retail_decision_console_static_interactions(
    created_at: datetime | None = None,
) -> RetailDecisionConsoleInteractionState:
    timestamp = created_at or utc_now()
    interactions = [
        RetailDecisionConsoleInteractionDescriptor(
            interaction_id="section-toggle-placeholder",
            label="Toggle section placeholder",
            interaction_type=RetailDecisionConsoleInteractionType.SECTION_TOGGLE,
            target_section_id="decision-summary",
            created_at=timestamp,
        ),
        RetailDecisionConsoleInteractionDescriptor(
            interaction_id="overview-tab-placeholder",
            label="Select overview tab placeholder",
            interaction_type=RetailDecisionConsoleInteractionType.STATIC_TAB_SELECT,
            target_section_id="header-status-banner",
            created_at=timestamp,
        ),
        RetailDecisionConsoleInteractionDescriptor(
            interaction_id="unavailable-reason-placeholder",
            label="Show unavailable reason placeholder",
            interaction_type=RetailDecisionConsoleInteractionType.SHOW_UNAVAILABLE_REASON,
            target_section_id="decision-summary",
            created_at=timestamp,
        ),
        RetailDecisionConsoleInteractionDescriptor(
            interaction_id="provenance-label-placeholder",
            label="Show provenance label placeholder",
            interaction_type=RetailDecisionConsoleInteractionType.SHOW_PROVENANCE_LABEL,
            target_section_id="evidence-panel",
            created_at=timestamp,
        ),
        RetailDecisionConsoleInteractionDescriptor(
            interaction_id="safety-info-placeholder",
            label="Show safety info placeholder",
            interaction_type=RetailDecisionConsoleInteractionType.SHOW_SAFETY_INFO,
            target_section_id="header-status-banner",
            created_at=timestamp,
        ),
        RetailDecisionConsoleInteractionDescriptor(
            interaction_id="local-refresh-placeholder",
            label="Local placeholder refresh",
            interaction_type=RetailDecisionConsoleInteractionType.LOCAL_PLACEHOLDER_REFRESH,
            target_section_id="refresh-placeholder",
            created_at=timestamp,
        ),
        RetailDecisionConsoleInteractionDescriptor(
            interaction_id="static-instrument-placeholder",
            label="Static instrument placeholder select",
            interaction_type=RetailDecisionConsoleInteractionType.STATIC_INSTRUMENT_PLACEHOLDER_SELECT,
            target_section_id="instrument-selector",
            created_at=timestamp,
        ),
        RetailDecisionConsoleInteractionDescriptor(
            interaction_id="static-timeframe-placeholder",
            label="Static timeframe placeholder select",
            interaction_type=RetailDecisionConsoleInteractionType.STATIC_TIMEFRAME_PLACEHOLDER_SELECT,
            target_section_id="timeframe-selector",
            created_at=timestamp,
        ),
    ]
    return RetailDecisionConsoleInteractionState(interactions=interactions, created_at=timestamp)
