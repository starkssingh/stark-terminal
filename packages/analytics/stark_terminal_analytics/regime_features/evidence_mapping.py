from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_analytics.foundation.contracts import sanitize_analytics_notes
from stark_terminal_analytics.regime.contracts import RegimeEvidenceKind
from stark_terminal_analytics.regime_features.contracts import (
    RegimeFeatureCandidate,
    RegimeFeatureGroup,
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


class RegimeFeatureEvidenceMapping(BaseModel):
    mapping_id: str
    feature_id: str
    feature_group: RegimeFeatureGroup
    evidence_kinds: list[RegimeEvidenceKind]
    required: bool = True
    evidence_description: str
    computation_allowed: bool = False
    classification_allowed: bool = False
    schema_version: str = "v1"

    @field_validator("mapping_id", "feature_id", "evidence_description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "regime feature evidence mapping text fields")

    @field_validator("evidence_kinds")
    @classmethod
    def evidence_kinds_must_be_present(cls, value: list[RegimeEvidenceKind]) -> list[RegimeEvidenceKind]:
        if not value:
            raise ValueError("regime feature evidence mapping kinds cannot be empty")
        if RegimeEvidenceKind.UNKNOWN in value:
            raise ValueError("UNKNOWN evidence kind is not allowed")
        return value

    @model_validator(mode="after")
    def mapping_must_remain_contract_only(self) -> RegimeFeatureEvidenceMapping:
        if self.feature_group == RegimeFeatureGroup.UNKNOWN:
            raise ValueError("UNKNOWN feature group is not allowed")
        if self.computation_allowed:
            raise ValueError("regime feature computation is forbidden in Prompt 34")
        if self.classification_allowed:
            raise ValueError("regime classification is forbidden in Prompt 34")
        return self


class RegimeFeatureEvidenceMap(BaseModel):
    map_id: str
    mappings: list[RegimeFeatureEvidenceMapping]
    complete: bool = False
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("map_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "regime feature evidence map text fields")

    @field_validator("mappings")
    @classmethod
    def mappings_must_be_present(
        cls,
        value: list[RegimeFeatureEvidenceMapping],
    ) -> list[RegimeFeatureEvidenceMapping]:
        if not value:
            raise ValueError("regime feature evidence map mappings cannot be empty")
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
    def complete_map_cannot_have_blockers(self) -> RegimeFeatureEvidenceMap:
        if self.complete and self.blockers:
            raise ValueError("complete regime feature evidence map cannot have blockers")
        return self


def _evidence_for_candidate(candidate: RegimeFeatureCandidate) -> list[RegimeEvidenceKind]:
    mapping = {
        RegimeFeatureGroup.RETURNS: [RegimeEvidenceKind.RETURNS],
        RegimeFeatureGroup.VOLATILITY: [RegimeEvidenceKind.VOLATILITY],
        RegimeFeatureGroup.DRAWDOWN: [RegimeEvidenceKind.DRAWDOWN],
        RegimeFeatureGroup.RELATIONSHIP: [RegimeEvidenceKind.CORRELATION, RegimeEvidenceKind.BETA],
        RegimeFeatureGroup.TIME_SERIES_DIAGNOSTICS: [RegimeEvidenceKind.TIME_SERIES_DIAGNOSTICS],
        RegimeFeatureGroup.VOLUME_LIQUIDITY: [RegimeEvidenceKind.VOLUME, RegimeEvidenceKind.LIQUIDITY],
        RegimeFeatureGroup.OPTIONS_CONTEXT: [RegimeEvidenceKind.OPTIONS_CONTEXT],
        RegimeFeatureGroup.MACRO_CONTEXT: [RegimeEvidenceKind.MACRO_CONTEXT],
        RegimeFeatureGroup.MARKET_MICROSTRUCTURE: [RegimeEvidenceKind.VOLUME, RegimeEvidenceKind.LIQUIDITY],
    }
    return mapping[candidate.group]


def default_regime_feature_evidence_mappings(
    candidates: list[RegimeFeatureCandidate] | None = None,
) -> list[RegimeFeatureEvidenceMapping]:
    resolved_candidates = candidates or default_regime_feature_candidates()
    return [
        RegimeFeatureEvidenceMapping(
            mapping_id=f"evidence-map-{candidate.name}",
            feature_id=candidate.feature_id,
            feature_group=candidate.group,
            evidence_kinds=_evidence_for_candidate(candidate),
            evidence_description=f"Contracts-only evidence mapping for {candidate.name}; no value is computed.",
        )
        for candidate in resolved_candidates
    ]


def build_regime_feature_evidence_map(
    mappings: list[RegimeFeatureEvidenceMapping] | None = None,
    completed_feature_ids: set[str] | None = None,
    warnings: list[str] | None = None,
) -> RegimeFeatureEvidenceMap:
    resolved_mappings = mappings or default_regime_feature_evidence_mappings()
    completed = completed_feature_ids or set()
    blockers = [
        f"missing evidence mapping for feature: {mapping.feature_id}"
        for mapping in resolved_mappings
        if mapping.required and mapping.feature_id not in completed
    ]
    return RegimeFeatureEvidenceMap(
        map_id="regime-feature-evidence-map-v1",
        mappings=resolved_mappings,
        complete=not blockers,
        blockers=blockers,
        warnings=warnings or [],
    )


def evaluate_regime_feature_evidence_map(
    evidence_map: RegimeFeatureEvidenceMap,
) -> RegimeFeatureEvidenceMap:
    if evidence_map.complete:
        return evidence_map
    blockers = evidence_map.blockers or ["required regime feature evidence mapping remains incomplete"]
    return evidence_map.model_copy(update={"complete": False, "blockers": sanitize_analytics_notes(blockers)})
