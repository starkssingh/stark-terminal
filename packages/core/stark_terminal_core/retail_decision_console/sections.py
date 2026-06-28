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


class RetailDecisionConsoleSectionKind(StrEnum):
    DECISION_SUMMARY = "DECISION_SUMMARY"
    EVIDENCE = "EVIDENCE"
    RISK_INVALIDATION = "RISK_INVALIDATION"
    REGIME_STATE = "REGIME_STATE"
    OPTIONS_CONTEXT = "OPTIONS_CONTEXT"
    RESEARCH_CONTEXT = "RESEARCH_CONTEXT"
    JOURNAL = "JOURNAL"


class RetailDecisionConsoleSectionPlaceholder(BaseModel):
    section_id: str
    section_kind: RetailDecisionConsoleSectionKind
    label: str
    description: str
    display_planning_only: bool = True
    read_only: bool = True
    active_ui_enabled: bool = False
    live_decisions_enabled: bool = False
    recommendations_enabled: bool = False
    action_generation_enabled: bool = False
    confidence_scoring_enabled: bool = False
    decision_object_generation_enabled: bool = False
    live_market_data_enabled: bool = False
    broker_controls_enabled: bool = False
    execution_enabled: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("section_id", "label", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console section text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @model_validator(mode="after")
    def section_must_remain_display_planning_only(self) -> RetailDecisionConsoleSectionPlaceholder:
        if not self.display_planning_only or not self.read_only:
            raise ValueError("retail decision console sections must remain display planning placeholders")
        dangerous_flags = {
            "active UI": self.active_ui_enabled,
            "live decisions": self.live_decisions_enabled,
            "recommendations": self.recommendations_enabled,
            "action generation": self.action_generation_enabled,
            "confidence scoring": self.confidence_scoring_enabled,
            "DecisionObject generation": self.decision_object_generation_enabled,
            "live market data": self.live_market_data_enabled,
            "broker controls": self.broker_controls_enabled,
            "execution": self.execution_enabled,
        }
        enabled = [name for name, value in dangerous_flags.items() if value]
        if enabled:
            raise ValueError("retail decision console section cannot enable: " + ", ".join(enabled))
        return self


class DecisionSummarySectionPlaceholder(RetailDecisionConsoleSectionPlaceholder):
    section_kind: RetailDecisionConsoleSectionKind = RetailDecisionConsoleSectionKind.DECISION_SUMMARY


class EvidenceSectionPlaceholder(RetailDecisionConsoleSectionPlaceholder):
    section_kind: RetailDecisionConsoleSectionKind = RetailDecisionConsoleSectionKind.EVIDENCE


class RiskInvalidationSectionPlaceholder(RetailDecisionConsoleSectionPlaceholder):
    section_kind: RetailDecisionConsoleSectionKind = RetailDecisionConsoleSectionKind.RISK_INVALIDATION


class RegimeStateSectionPlaceholder(RetailDecisionConsoleSectionPlaceholder):
    section_kind: RetailDecisionConsoleSectionKind = RetailDecisionConsoleSectionKind.REGIME_STATE


class OptionsContextSectionPlaceholder(RetailDecisionConsoleSectionPlaceholder):
    section_kind: RetailDecisionConsoleSectionKind = RetailDecisionConsoleSectionKind.OPTIONS_CONTEXT


class ResearchContextSectionPlaceholder(RetailDecisionConsoleSectionPlaceholder):
    section_kind: RetailDecisionConsoleSectionKind = RetailDecisionConsoleSectionKind.RESEARCH_CONTEXT


class JournalSectionPlaceholder(RetailDecisionConsoleSectionPlaceholder):
    section_kind: RetailDecisionConsoleSectionKind = RetailDecisionConsoleSectionKind.JOURNAL


def default_retail_decision_console_section_placeholders() -> list[RetailDecisionConsoleSectionPlaceholder]:
    return [
        DecisionSummarySectionPlaceholder(
            section_id="decision-summary-section-placeholder",
            label="Decision summary placeholder",
            description="Unavailable decision summary shell area; no generated bias or action state.",
        ),
        EvidenceSectionPlaceholder(
            section_id="evidence-section-placeholder",
            label="Evidence placeholder",
            description="Future evidence panel placeholder; no validated decision evidence yet.",
        ),
        RiskInvalidationSectionPlaceholder(
            section_id="risk-invalidation-section-placeholder",
            label="Risk and invalidation placeholder",
            description="Future risk and invalidation shell placeholder; no live risk signal.",
        ),
        RegimeStateSectionPlaceholder(
            section_id="regime-state-section-placeholder",
            label="Regime/state placeholder",
            description="Future regime/state context placeholder; no active regime decision.",
        ),
        OptionsContextSectionPlaceholder(
            section_id="options-context-section-placeholder",
            label="Options context placeholder",
            description="Future options context placeholder; no options recommendation.",
        ),
        ResearchContextSectionPlaceholder(
            section_id="research-context-section-placeholder",
            label="Research context placeholder",
            description="Future research context placeholder; no retrieval or generated strategy.",
        ),
        JournalSectionPlaceholder(
            section_id="journal-section-placeholder",
            label="Journal placeholder",
            description="Future journal link placeholder; no trade or execution workflow.",
        ),
    ]
