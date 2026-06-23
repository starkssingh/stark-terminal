from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_analytics.foundation.contracts import sanitize_analytics_notes
from stark_terminal_analytics.regime_features.contracts import (
    RegimeFeatureCandidate,
    default_regime_feature_candidates,
)


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


class RegimeFeatureProvenanceRequirement(BaseModel):
    provenance_id: str
    feature_id: str
    required_source_references: list[str]
    required_analytics_families: list[str]
    requires_dataset_manifest: bool = False
    requires_validation_report: bool = True
    synthetic_or_local_only_until_approved: bool = True
    schema_version: str = "v1"

    @field_validator("provenance_id", "feature_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "regime feature provenance text fields")

    @field_validator("required_source_references", "required_analytics_families")
    @classmethod
    def list_fields_must_be_present(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_analytics_notes(value)
        if not sanitized:
            raise ValueError("regime feature provenance list fields cannot be empty")
        return sanitized


class RegimeFeatureProvenanceMap(BaseModel):
    map_id: str
    requirements: list[RegimeFeatureProvenanceRequirement]
    complete: bool = False
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("map_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "regime feature provenance map text fields")

    @field_validator("requirements")
    @classmethod
    def requirements_must_be_present(
        cls,
        value: list[RegimeFeatureProvenanceRequirement],
    ) -> list[RegimeFeatureProvenanceRequirement]:
        if not value:
            raise ValueError("regime feature provenance map requirements cannot be empty")
        return value

    @field_validator("blockers", "warnings")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_analytics_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def complete_map_cannot_have_blockers(self) -> RegimeFeatureProvenanceMap:
        if self.complete and self.blockers:
            raise ValueError("complete regime feature provenance map cannot have blockers")
        return self


def default_regime_feature_provenance_requirements(
    candidates: list[RegimeFeatureCandidate] | None = None,
) -> list[RegimeFeatureProvenanceRequirement]:
    resolved_candidates = candidates or default_regime_feature_candidates()
    return [
        RegimeFeatureProvenanceRequirement(
            provenance_id=f"provenance-{candidate.name}",
            feature_id=candidate.feature_id,
            required_source_references=[f"{candidate.name}:source_reference"],
            required_analytics_families=candidate.planned_input_analytics,
            requires_dataset_manifest=candidate.group.value in {
                "VOLUME_LIQUIDITY",
                "OPTIONS_CONTEXT",
                "MACRO_CONTEXT",
                "MARKET_MICROSTRUCTURE",
            },
            requires_validation_report=True,
        )
        for candidate in resolved_candidates
    ]


def build_regime_feature_provenance_map(
    requirements: list[RegimeFeatureProvenanceRequirement] | None = None,
    completed_feature_ids: set[str] | None = None,
    warnings: list[str] | None = None,
) -> RegimeFeatureProvenanceMap:
    resolved_requirements = requirements or default_regime_feature_provenance_requirements()
    completed = completed_feature_ids or set()
    blockers = [
        f"missing provenance for feature: {requirement.feature_id}"
        for requirement in resolved_requirements
        if requirement.feature_id not in completed
    ]
    return RegimeFeatureProvenanceMap(
        map_id="regime-feature-provenance-map-v1",
        requirements=resolved_requirements,
        complete=not blockers,
        blockers=blockers,
        warnings=warnings or [],
    )


def evaluate_regime_feature_provenance_map(
    provenance_map: RegimeFeatureProvenanceMap,
) -> RegimeFeatureProvenanceMap:
    if provenance_map.complete:
        return provenance_map
    blockers = provenance_map.blockers or ["required regime feature provenance remains incomplete"]
    return provenance_map.model_copy(update={"complete": False, "blockers": sanitize_analytics_notes(blockers)})
