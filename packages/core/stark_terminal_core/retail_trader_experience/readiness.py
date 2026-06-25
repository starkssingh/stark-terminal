from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_trader_experience.cards import RetailTraderExperienceCardPlaceholder
from stark_terminal_core.retail_trader_experience.interactions import RetailTraderExperienceForbiddenInteraction
from stark_terminal_core.retail_trader_experience.journeys import RetailTraderJourneyPlaceholder
from stark_terminal_core.retail_trader_experience.personas import RetailTraderPersonaPlaceholder
from stark_terminal_core.retail_trader_experience.planning import (
    RetailTraderExperiencePlanningContract,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
)
from stark_terminal_core.retail_trader_experience.safety import RetailTraderExperienceSafetyResult
from stark_terminal_core.retail_trader_experience.sections import RetailTraderExperienceSectionPlaceholder


class RetailTraderExperienceReadinessReport(BaseModel):
    report_id: str
    plan_id: str
    persona_count: int = Field(ge=0)
    journey_count: int = Field(ge=0)
    section_count: int = Field(ge=0)
    card_count: int = Field(ge=0)
    forbidden_interaction_count: int = Field(ge=0)
    safety_result_safe: bool
    ready_for_api_contract_skeleton: bool = False
    ready_for_display_contract_skeleton: bool = False
    ready_for_active_ui: bool = False
    ready_for_recommendations: bool = False
    ready_for_action_generation: bool = False
    ready_for_confidence_scoring: bool = False
    ready_for_decision_objects: bool = False
    ready_for_readiness_to_trade: bool = False
    ready_for_broker_controls: bool = False
    ready_for_execution: bool = False
    ready_for_suitability_profiling: bool = False
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("report_id", "plan_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail trader experience readiness report text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def readiness_report_must_fail_closed(self) -> RetailTraderExperienceReadinessReport:
        if self.ready_for_active_ui:
            raise ValueError("Retail Trader Experience active UI readiness is forbidden in Prompt 56")
        if self.ready_for_recommendations:
            raise ValueError("Retail Trader Experience recommendation readiness is forbidden in Prompt 56")
        if self.ready_for_action_generation:
            raise ValueError("Retail Trader Experience action generation readiness is forbidden in Prompt 56")
        if self.ready_for_confidence_scoring:
            raise ValueError("Retail Trader Experience confidence scoring readiness is forbidden in Prompt 56")
        if self.ready_for_decision_objects:
            raise ValueError("Retail Trader Experience DecisionObject readiness is forbidden in Prompt 56")
        if self.ready_for_readiness_to_trade:
            raise ValueError("Retail Trader Experience readiness-to-trade is forbidden in Prompt 56")
        if self.ready_for_broker_controls:
            raise ValueError("Retail Trader Experience broker control readiness is forbidden in Prompt 56")
        if self.ready_for_execution:
            raise ValueError("Retail Trader Experience execution readiness is forbidden in Prompt 56")
        if self.ready_for_suitability_profiling:
            raise ValueError("Retail Trader Experience suitability profiling readiness is forbidden in Prompt 56")
        return self


def build_retail_trader_experience_readiness_report(
    plan: RetailTraderExperiencePlanningContract,
    personas: list[RetailTraderPersonaPlaceholder],
    journeys: list[RetailTraderJourneyPlaceholder],
    sections: list[RetailTraderExperienceSectionPlaceholder],
    cards: list[RetailTraderExperienceCardPlaceholder],
    forbidden_interactions: list[RetailTraderExperienceForbiddenInteraction],
    safety_result: RetailTraderExperienceSafetyResult,
) -> RetailTraderExperienceReadinessReport:
    blockers = [] if safety_result.safe else list(safety_result.reasons)
    warnings = [
        "Retail Trader Experience is ready for API/display contract skeleton planning only, not active UI.",
        "No suitability profiling, recommendation cards, broker controls, readiness-to-trade, or execution are allowed.",
    ]
    return RetailTraderExperienceReadinessReport(
        report_id="retail-trader-experience-readiness-report-v1",
        plan_id=plan.plan_id,
        persona_count=len(personas),
        journey_count=len(journeys),
        section_count=len(sections),
        card_count=len(cards),
        forbidden_interaction_count=len(forbidden_interactions),
        safety_result_safe=safety_result.safe,
        ready_for_api_contract_skeleton=safety_result.safe and not blockers,
        ready_for_display_contract_skeleton=safety_result.safe and not blockers,
        blockers=blockers,
        warnings=warnings,
    )


def retail_trader_experience_ready_for_active_ui(report: RetailTraderExperienceReadinessReport) -> bool:
    return False


def retail_trader_experience_ready_for_recommendations(report: RetailTraderExperienceReadinessReport) -> bool:
    return False


def retail_trader_experience_ready_for_execution(report: RetailTraderExperienceReadinessReport) -> bool:
    return False


def retail_trader_experience_ready_for_suitability_profiling(
    report: RetailTraderExperienceReadinessReport,
) -> bool:
    return False
