from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_analytics.foundation.contracts import sanitize_analytics_notes
from stark_terminal_analytics.regime.contracts import RegimeAnalyticsPlan, RegimePlanningStage
from stark_terminal_analytics.regime.evidence import RegimeEvidenceChecklist
from stark_terminal_analytics.regime.safety import RegimeSafetyResult


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _utc_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _non_empty_text(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} cannot be empty")
    return normalized


class RegimeReadinessReport(BaseModel):
    report_id: str
    plan_id: str
    planning_stage: RegimePlanningStage
    evidence_complete: bool
    safety_decision: str
    ready_for_feature_preparation: bool = False
    ready_for_classification: bool = False
    ready_for_production: bool = False
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    schema_version: str = "v1"
    generated_at: datetime = Field(default_factory=_utc_now)

    @field_validator("report_id", "plan_id", "safety_decision", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "regime readiness report text fields")

    @field_validator("blockers", "warnings")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_analytics_notes(value)

    @field_validator("generated_at")
    @classmethod
    def generated_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def report_must_remain_conservative(self) -> RegimeReadinessReport:
        if self.ready_for_classification:
            raise ValueError("regime readiness cannot allow classification in Prompt 33")
        if self.ready_for_production:
            raise ValueError("regime readiness cannot allow production use in Prompt 33")
        if self.ready_for_feature_preparation and (not self.evidence_complete or self.blockers):
            raise ValueError("feature preparation readiness requires complete evidence and no blockers")
        return self


def build_regime_readiness_report(
    plan: RegimeAnalyticsPlan,
    checklist: RegimeEvidenceChecklist,
    safety_result: RegimeSafetyResult,
) -> RegimeReadinessReport:
    blockers = list(checklist.blockers)
    warnings = list(checklist.warnings)
    if safety_result.decision == "blocked":
        blockers.extend(safety_result.reasons)
    else:
        warnings.extend(safety_result.reasons)
    ready_for_feature_preparation = checklist.complete and not blockers and safety_result.decision != "blocked"
    return RegimeReadinessReport(
        report_id="regime-readiness-report-v1",
        plan_id=plan.plan_id,
        planning_stage=plan.stage,
        evidence_complete=checklist.complete,
        safety_decision=safety_result.decision,
        ready_for_feature_preparation=ready_for_feature_preparation,
        ready_for_classification=False,
        ready_for_production=False,
        blockers=blockers,
        warnings=warnings,
    )


def regime_ready_for_feature_preparation(report: RegimeReadinessReport) -> bool:
    return report.ready_for_feature_preparation and not report.blockers


def regime_ready_for_classification(report: RegimeReadinessReport) -> bool:
    return False


def regime_ready_for_production(report: RegimeReadinessReport) -> bool:
    return False
