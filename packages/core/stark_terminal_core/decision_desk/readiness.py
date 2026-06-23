from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_desk.evidence import RetailDecisionEvidenceChecklist
from stark_terminal_core.decision_desk.human_review import RetailHumanReviewChecklist
from stark_terminal_core.decision_desk.planning import (
    RetailDecisionDeskPlan,
    RetailDecisionDeskStage,
    _non_empty_text,
    sanitize_decision_notes,
)
from stark_terminal_core.decision_desk.safety import RetailDecisionDeskSafetyResult


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _utc_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


class RetailDecisionDeskReadinessReport(BaseModel):
    report_id: str
    plan_id: str
    planning_stage: RetailDecisionDeskStage
    evidence_complete: bool
    human_review_complete: bool
    safety_decision: str
    ready_for_display_contracts: bool = False
    ready_for_evidence_bundle_contracts: bool = False
    ready_for_recommendations: bool = False
    ready_for_confidence_scoring: bool = False
    ready_for_decision_objects: bool = False
    ready_for_execution: bool = False
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    schema_version: str = "v1"
    generated_at: datetime = Field(default_factory=_utc_now)

    @field_validator("report_id", "plan_id", "safety_decision", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail decision desk readiness report text fields")

    @field_validator("blockers", "warnings")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_notes(value)

    @field_validator("generated_at")
    @classmethod
    def generated_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def report_must_remain_planning_only(self) -> RetailDecisionDeskReadinessReport:
        if self.ready_for_recommendations:
            raise ValueError("recommendations are forbidden in Prompt 36")
        if self.ready_for_confidence_scoring:
            raise ValueError("confidence scoring is forbidden in Prompt 36")
        if self.ready_for_decision_objects:
            raise ValueError("DecisionObject generation is forbidden in Prompt 36")
        if self.ready_for_execution:
            raise ValueError("execution is forbidden in Prompt 36")
        if self.ready_for_display_contracts and self.blockers:
            raise ValueError("display contract readiness requires no blockers")
        if self.ready_for_evidence_bundle_contracts and self.blockers:
            raise ValueError("evidence bundle contract readiness requires no blockers")
        return self


def build_retail_decision_desk_readiness_report(
    plan: RetailDecisionDeskPlan,
    evidence_checklist: RetailDecisionEvidenceChecklist,
    human_review_checklist: RetailHumanReviewChecklist,
    safety_result: RetailDecisionDeskSafetyResult,
) -> RetailDecisionDeskReadinessReport:
    blockers = [*evidence_checklist.blockers, *human_review_checklist.blockers]
    warnings = [*evidence_checklist.warnings, *human_review_checklist.warnings]
    if safety_result.decision == "blocked":
        blockers.extend(safety_result.reasons)
    else:
        warnings.extend(safety_result.reasons)
    ready_for_planning_contracts = (
        evidence_checklist.complete
        and human_review_checklist.complete
        and safety_result.decision != "blocked"
        and not blockers
    )
    return RetailDecisionDeskReadinessReport(
        report_id="retail-decision-desk-readiness-report-v1",
        plan_id=plan.plan_id,
        planning_stage=plan.stage,
        evidence_complete=evidence_checklist.complete,
        human_review_complete=human_review_checklist.complete,
        safety_decision=safety_result.decision,
        ready_for_display_contracts=ready_for_planning_contracts,
        ready_for_evidence_bundle_contracts=ready_for_planning_contracts,
        ready_for_recommendations=False,
        ready_for_confidence_scoring=False,
        ready_for_decision_objects=False,
        ready_for_execution=False,
        blockers=blockers,
        warnings=warnings,
    )


def retail_decision_desk_ready_for_display_contracts(report: RetailDecisionDeskReadinessReport) -> bool:
    return report.ready_for_display_contracts and not report.blockers


def retail_decision_desk_ready_for_evidence_bundle_contracts(report: RetailDecisionDeskReadinessReport) -> bool:
    return report.ready_for_evidence_bundle_contracts and not report.blockers


def retail_decision_desk_ready_for_recommendations(report: RetailDecisionDeskReadinessReport) -> bool:
    return False


def retail_decision_desk_ready_for_decision_objects(report: RetailDecisionDeskReadinessReport) -> bool:
    return False


def retail_decision_desk_ready_for_execution(report: RetailDecisionDeskReadinessReport) -> bool:
    return False
