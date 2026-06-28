from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_decision_console.productization import (
    SERVICE_NAME,
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)
from stark_terminal_core.retail_decision_console.ui_descriptors import (
    FORBIDDEN_ACTIVE_CONTROL_LABELS,
)


class RetailDecisionConsoleUnavailableReason(StrEnum):
    DEMO_STATIC_PLACEHOLDER = "DEMO_STATIC_PLACEHOLDER"
    DATA_QUALITY_NOT_VALIDATED = "DATA_QUALITY_NOT_VALIDATED"
    PROVENANCE_NOT_VALIDATED = "PROVENANCE_NOT_VALIDATED"
    DECISION_VALIDATION_NOT_IMPLEMENTED = "DECISION_VALIDATION_NOT_IMPLEMENTED"


FORBIDDEN_ACTIVE_DECISION_OUTPUTS = (
    "Buy",
    "Sell",
    "Hold",
    "Watch",
    "Avoid",
    "Strong Buy",
    "Strong Sell",
    "Ready to Trade",
)


def _enabled_flags(flags: dict[str, bool]) -> list[str]:
    return [name for name, value in flags.items() if value]


def _contains_active_decision_label(labels: list[str]) -> list[str]:
    forbidden = {label.casefold() for label in (*FORBIDDEN_ACTIVE_CONTROL_LABELS, *FORBIDDEN_ACTIVE_DECISION_OUTPUTS)}
    return [label for label in labels if label.casefold() in forbidden]


class RetailDecisionConsoleProvenanceState(BaseModel):
    provenance_id: str
    label: str = "Demo/static/unavailable placeholder provenance"
    source_type: str = "demo_static_unavailable"
    demo_only: bool = True
    static_only: bool = True
    unavailable: bool = True
    source_validated: bool = False
    data_quality_validated: bool = False
    live_market_data_source: bool = False
    notes: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("provenance_id", "label", "source_type")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console provenance text")

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def provenance_must_remain_demo_static_unavailable(self) -> RetailDecisionConsoleProvenanceState:
        combined = " ".join([self.label, self.source_type, *self.notes]).casefold()
        for required in ("demo", "static", "unavailable"):
            if required not in combined:
                raise ValueError("retail decision console provenance must clearly say demo/static/unavailable")
        if not self.demo_only or not self.static_only or not self.unavailable:
            raise ValueError("retail decision console provenance must remain demo/static/unavailable")
        if self.source_validated or self.data_quality_validated or self.live_market_data_source:
            raise ValueError("retail decision console provenance cannot imply validated or live market data")
        return self


class RetailDecisionConsoleCardState(BaseModel):
    card_id: str
    title: str
    body: str
    unavailable_reason: RetailDecisionConsoleUnavailableReason = (
        RetailDecisionConsoleUnavailableReason.DEMO_STATIC_PLACEHOLDER
    )
    demo_only: bool = True
    unavailable: bool = True
    live_data_enabled: bool = False
    recommendations_enabled: bool = False
    action_generation_enabled: bool = False
    confidence_scoring_enabled: bool = False
    decision_object_generation_enabled: bool = False
    broker_controls_enabled: bool = False
    order_buttons_enabled: bool = False
    execution_enabled: bool = False
    active_decision_labels: list[str] = Field(default_factory=list)
    numeric_confidence_score: float | None = None
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("card_id", "title", "body")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console card state text")

    @field_validator("active_decision_labels")
    @classmethod
    def active_decision_labels_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def card_state_must_remain_demo_unavailable(self) -> RetailDecisionConsoleCardState:
        if not self.demo_only or not self.unavailable:
            raise ValueError("retail decision console card state must remain demo-only and unavailable")
        enabled = _enabled_flags(
            {
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
            raise ValueError("retail decision console card state cannot enable: " + ", ".join(enabled))
        forbidden_labels = _contains_active_decision_label(self.active_decision_labels)
        if forbidden_labels:
            raise ValueError("retail decision console card state cannot expose active labels: " + ", ".join(forbidden_labels))
        if self.numeric_confidence_score is not None:
            raise ValueError("retail decision console card state cannot expose confidence-like numeric scores")
        return self


class RetailDecisionConsoleSectionState(BaseModel):
    section_id: str
    title: str
    body: str
    cards: list[RetailDecisionConsoleCardState]
    unavailable_reason: RetailDecisionConsoleUnavailableReason = (
        RetailDecisionConsoleUnavailableReason.DEMO_STATIC_PLACEHOLDER
    )
    demo_only: bool = True
    unavailable: bool = True
    live_data_enabled: bool = False
    recommendations_enabled: bool = False
    action_generation_enabled: bool = False
    confidence_scoring_enabled: bool = False
    decision_object_generation_enabled: bool = False
    broker_controls_enabled: bool = False
    order_buttons_enabled: bool = False
    execution_enabled: bool = False
    active_decision_labels: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("section_id", "title", "body")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console section state text")

    @field_validator("active_decision_labels")
    @classmethod
    def active_decision_labels_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def section_state_must_remain_demo_unavailable(self) -> RetailDecisionConsoleSectionState:
        if not self.demo_only or not self.unavailable:
            raise ValueError("retail decision console section state must remain demo-only and unavailable")
        if not self.cards:
            raise ValueError("retail decision console section state requires demo cards")
        enabled = _enabled_flags(
            {
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
            raise ValueError("retail decision console section state cannot enable: " + ", ".join(enabled))
        forbidden_labels = _contains_active_decision_label(self.active_decision_labels)
        if forbidden_labels:
            raise ValueError(
                "retail decision console section state cannot expose active labels: " + ", ".join(forbidden_labels)
            )
        return self


class RetailDecisionConsoleStaticState(BaseModel):
    state_id: str
    service: str = SERVICE_NAME
    stage: str = "demo_static_state"
    schema_version: str = "v1"
    demo_static_state_only: bool = True
    demo_only: bool = True
    unavailable: bool = True
    read_only: bool = True
    live_data_enabled: bool = False
    recommendations_enabled: bool = False
    action_generation_enabled: bool = False
    confidence_scoring_enabled: bool = False
    decision_object_generation_enabled: bool = False
    broker_controls_enabled: bool = False
    order_buttons_enabled: bool = False
    execution_enabled: bool = False
    provenance: RetailDecisionConsoleProvenanceState
    sections: list[RetailDecisionConsoleSectionState]
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("state_id", "service", "stage", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console static state text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def static_state_must_remain_safe(self) -> RetailDecisionConsoleStaticState:
        if self.service != SERVICE_NAME:
            raise ValueError("retail decision console static state service name is fixed")
        if self.stage != "demo_static_state":
            raise ValueError("retail decision console static state stage must be demo_static_state")
        if not self.demo_static_state_only or not self.demo_only or not self.unavailable or not self.read_only:
            raise ValueError("retail decision console static state must remain demo-only, unavailable, and read-only")
        if not self.sections:
            raise ValueError("retail decision console static state requires sections")
        enabled = _enabled_flags(
            {
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
            raise ValueError("retail decision console static state cannot enable: " + ", ".join(enabled))
        return self
