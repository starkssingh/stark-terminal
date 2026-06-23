from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_dashboard.cards import RetailDashboardCardPlaceholder
from stark_terminal_core.retail_dashboard.interactions import RetailDashboardForbiddenInteraction
from stark_terminal_core.retail_dashboard.planning import (
    RetailDashboardPlanningContract,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
)
from stark_terminal_core.retail_dashboard.safety import RetailDashboardSafetyResult
from stark_terminal_core.retail_dashboard.sections import RetailDashboardSectionPlaceholder


class RetailDashboardReadinessReport(BaseModel):
    report_id: str
    plan_id: str
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
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("report_id", "plan_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard readiness report text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def readiness_report_must_fail_closed(self) -> RetailDashboardReadinessReport:
        if self.ready_for_active_ui:
            raise ValueError("Retail Dashboard active UI readiness is forbidden in Prompt 49")
        if self.ready_for_recommendations:
            raise ValueError("Retail Dashboard recommendation readiness is forbidden in Prompt 49")
        if self.ready_for_action_generation:
            raise ValueError("Retail Dashboard action generation readiness is forbidden in Prompt 49")
        if self.ready_for_confidence_scoring:
            raise ValueError("Retail Dashboard confidence scoring readiness is forbidden in Prompt 49")
        if self.ready_for_decision_objects:
            raise ValueError("Retail Dashboard DecisionObject readiness is forbidden in Prompt 49")
        if self.ready_for_readiness_to_trade:
            raise ValueError("Retail Dashboard readiness-to-trade is forbidden in Prompt 49")
        if self.ready_for_broker_controls:
            raise ValueError("Retail Dashboard broker control readiness is forbidden in Prompt 49")
        if self.ready_for_execution:
            raise ValueError("Retail Dashboard execution readiness is forbidden in Prompt 49")
        return self


def build_retail_dashboard_readiness_report(
    plan: RetailDashboardPlanningContract,
    sections: list[RetailDashboardSectionPlaceholder],
    cards: list[RetailDashboardCardPlaceholder],
    forbidden_interactions: list[RetailDashboardForbiddenInteraction],
    safety_result: RetailDashboardSafetyResult,
) -> RetailDashboardReadinessReport:
    blockers = [] if safety_result.safe else list(safety_result.reasons)
    warnings = [
        "Retail Dashboard is ready for API/display contract skeleton planning only, not active UI.",
        "No recommendation cards, broker controls, readiness-to-trade, or execution are allowed.",
    ]
    return RetailDashboardReadinessReport(
        report_id="retail-dashboard-readiness-report-v1",
        plan_id=plan.plan_id,
        section_count=len(sections),
        card_count=len(cards),
        forbidden_interaction_count=len(forbidden_interactions),
        safety_result_safe=safety_result.safe,
        ready_for_api_contract_skeleton=safety_result.safe and not blockers,
        ready_for_display_contract_skeleton=safety_result.safe and not blockers,
        blockers=blockers,
        warnings=warnings,
    )


def retail_dashboard_ready_for_active_ui(report: RetailDashboardReadinessReport) -> bool:
    return False


def retail_dashboard_ready_for_recommendations(report: RetailDashboardReadinessReport) -> bool:
    return False


def retail_dashboard_ready_for_execution(report: RetailDashboardReadinessReport) -> bool:
    return False
