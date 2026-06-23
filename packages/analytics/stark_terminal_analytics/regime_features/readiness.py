from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_analytics.foundation.contracts import sanitize_analytics_notes
from stark_terminal_analytics.regime_features.contracts import (
    RegimeFeatureCandidate,
    RegimeFeatureGroupPlan,
)
from stark_terminal_analytics.regime_features.evidence_mapping import RegimeFeatureEvidenceMap
from stark_terminal_analytics.regime_features.provenance import RegimeFeatureProvenanceMap
from stark_terminal_analytics.regime_features.safety import RegimeFeatureSafetyResult


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


class RegimeFeatureReadinessReport(BaseModel):
    report_id: str
    candidate_count: int = Field(ge=0)
    group_count: int = Field(ge=0)
    provenance_complete: bool
    evidence_mapping_complete: bool
    ready_for_feature_computation: bool = False
    ready_for_registry_write: bool = False
    ready_for_classification: bool = False
    ready_for_production: bool = False
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    schema_version: str = "v1"
    generated_at: datetime = Field(default_factory=_utc_now)

    @field_validator("report_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "regime feature readiness text fields")

    @field_validator("blockers", "warnings")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_analytics_notes(value)

    @field_validator("generated_at")
    @classmethod
    def generated_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def report_must_remain_contract_only(self) -> RegimeFeatureReadinessReport:
        if self.ready_for_feature_computation:
            raise ValueError("feature computation is forbidden in Prompt 34")
        if self.ready_for_registry_write:
            raise ValueError("feature registry writes are forbidden in Prompt 34")
        if self.ready_for_classification:
            raise ValueError("regime classification is forbidden in Prompt 34")
        if self.ready_for_production:
            raise ValueError("production use is forbidden in Prompt 34")
        return self


def build_regime_feature_readiness_report(
    candidates: list[RegimeFeatureCandidate],
    groups: list[RegimeFeatureGroupPlan],
    provenance_map: RegimeFeatureProvenanceMap,
    evidence_map: RegimeFeatureEvidenceMap,
    safety_result: RegimeFeatureSafetyResult | None = None,
) -> RegimeFeatureReadinessReport:
    blockers = [*provenance_map.blockers, *evidence_map.blockers]
    warnings = [*provenance_map.warnings, *evidence_map.warnings]
    if safety_result is not None:
        if safety_result.decision == "blocked":
            blockers.extend(safety_result.reasons)
        else:
            warnings.extend(safety_result.reasons)
    if not candidates:
        blockers.append("no regime feature candidates defined")
    if not groups:
        blockers.append("no regime feature groups defined")
    return RegimeFeatureReadinessReport(
        report_id="regime-feature-readiness-report-v1",
        candidate_count=len(candidates),
        group_count=len(groups),
        provenance_complete=provenance_map.complete,
        evidence_mapping_complete=evidence_map.complete,
        ready_for_feature_computation=False,
        ready_for_registry_write=False,
        ready_for_classification=False,
        ready_for_production=False,
        blockers=blockers,
        warnings=warnings,
    )


def regime_features_ready_for_computation(report: RegimeFeatureReadinessReport) -> bool:
    return False


def regime_features_ready_for_registry_write(report: RegimeFeatureReadinessReport) -> bool:
    return False


def regime_features_ready_for_classification(report: RegimeFeatureReadinessReport) -> bool:
    return False
