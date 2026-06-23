from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_analytics.foundation.contracts import sanitize_analytics_notes
from stark_terminal_analytics.regime.contracts import RegimeEvidenceKind


class RegimeFeatureGroup(StrEnum):
    RETURNS = "RETURNS"
    VOLATILITY = "VOLATILITY"
    DRAWDOWN = "DRAWDOWN"
    RELATIONSHIP = "RELATIONSHIP"
    TIME_SERIES_DIAGNOSTICS = "TIME_SERIES_DIAGNOSTICS"
    VOLUME_LIQUIDITY = "VOLUME_LIQUIDITY"
    OPTIONS_CONTEXT = "OPTIONS_CONTEXT"
    MACRO_CONTEXT = "MACRO_CONTEXT"
    MARKET_MICROSTRUCTURE = "MARKET_MICROSTRUCTURE"
    UNKNOWN = "UNKNOWN"


class RegimeFeaturePreparationStage(StrEnum):
    CONTRACTS_ONLY = "CONTRACTS_ONLY"
    EVIDENCE_MAPPING = "EVIDENCE_MAPPING"
    PROVENANCE_READY = "PROVENANCE_READY"
    FEATURE_COMPUTATION_PLANNED = "FEATURE_COMPUTATION_PLANNED"
    REGISTRY_INTEGRATION_PLANNED = "REGISTRY_INTEGRATION_PLANNED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class RegimeFeatureCandidateStatus(StrEnum):
    PLANNED = "PLANNED"
    NEEDS_EVIDENCE = "NEEDS_EVIDENCE"
    NEEDS_PROVENANCE = "NEEDS_PROVENANCE"
    READY_FOR_FUTURE_COMPUTATION = "READY_FOR_FUTURE_COMPUTATION"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class RegimeFeatureSafetyLabel(StrEnum):
    PREPARATION_ONLY = "PREPARATION_ONLY"
    RESEARCH_ONLY = "RESEARCH_ONLY"
    NOT_A_SIGNAL = "NOT_A_SIGNAL"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


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


class RegimeFeatureCandidate(BaseModel):
    feature_id: str
    name: str
    display_name: str
    group: RegimeFeatureGroup
    description: str
    planned_input_analytics: list[str]
    planned_output_kind: str
    status: RegimeFeatureCandidateStatus = RegimeFeatureCandidateStatus.PLANNED
    preparation_stage: RegimeFeaturePreparationStage = RegimeFeaturePreparationStage.CONTRACTS_ONLY
    computation_allowed: bool = False
    registry_write_allowed: bool = False
    classification_allowed: bool = False
    trade_signal: bool = False
    recommendation: bool = False
    decision_object_generated: bool = False
    safety_label: RegimeFeatureSafetyLabel = RegimeFeatureSafetyLabel.PREPARATION_ONLY
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("feature_id", "name", "display_name", "description", "planned_output_kind", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "regime feature candidate text fields")

    @field_validator("planned_input_analytics")
    @classmethod
    def planned_inputs_must_be_present(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_analytics_notes(value)
        if not sanitized:
            raise ValueError("planned_input_analytics cannot be empty")
        return sanitized

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_analytics_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def candidate_must_remain_preparation_only(self) -> RegimeFeatureCandidate:
        if self.group == RegimeFeatureGroup.UNKNOWN:
            raise ValueError("regime feature group cannot be UNKNOWN")
        if self.status == RegimeFeatureCandidateStatus.UNKNOWN:
            raise ValueError("regime feature candidate status cannot be UNKNOWN")
        if self.preparation_stage == RegimeFeaturePreparationStage.UNKNOWN:
            raise ValueError("regime feature preparation stage cannot be UNKNOWN")
        if self.computation_allowed:
            raise ValueError("regime feature computation is forbidden in Prompt 34")
        if self.registry_write_allowed:
            raise ValueError("regime feature registry writes are forbidden in Prompt 34")
        if self.classification_allowed:
            raise ValueError("regime classification is forbidden in Prompt 34")
        if self.trade_signal:
            raise ValueError("regime feature candidates cannot be trade signals")
        if self.recommendation:
            raise ValueError("regime feature candidates cannot be recommendations")
        if self.decision_object_generated:
            raise ValueError("regime feature candidates cannot generate DecisionObjects")
        if self.safety_label == RegimeFeatureSafetyLabel.UNKNOWN:
            raise ValueError("regime feature safety label cannot be UNKNOWN")
        return self


class RegimeFeatureGroupPlan(BaseModel):
    group_id: str
    group: RegimeFeatureGroup
    description: str
    candidates: list[RegimeFeatureCandidate]
    required_evidence_kinds: list[RegimeEvidenceKind]
    computation_allowed: bool = False
    classification_allowed: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("group_id", "description", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "regime feature group text fields")

    @field_validator("candidates")
    @classmethod
    def candidates_must_be_present(cls, value: list[RegimeFeatureCandidate]) -> list[RegimeFeatureCandidate]:
        if not value:
            raise ValueError("regime feature group plans must include candidates")
        return value

    @field_validator("required_evidence_kinds")
    @classmethod
    def evidence_kinds_must_be_present(cls, value: list[RegimeEvidenceKind]) -> list[RegimeEvidenceKind]:
        if not value:
            raise ValueError("regime feature group plans must include evidence kinds")
        if RegimeEvidenceKind.UNKNOWN in value:
            raise ValueError("UNKNOWN evidence kind is not allowed")
        return value

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def group_must_remain_preparation_only(self) -> RegimeFeatureGroupPlan:
        if self.group == RegimeFeatureGroup.UNKNOWN:
            raise ValueError("regime feature group cannot be UNKNOWN")
        if self.computation_allowed:
            raise ValueError("regime feature computation is forbidden in Prompt 34")
        if self.classification_allowed:
            raise ValueError("regime classification is forbidden in Prompt 34")
        for candidate in self.candidates:
            if candidate.group != self.group:
                raise ValueError("candidate group must match group plan")
        return self


def create_regime_feature_candidate(
    feature_id: str,
    name: str,
    display_name: str,
    group: RegimeFeatureGroup,
    description: str,
    planned_input_analytics: list[str],
    planned_output_kind: str = "metadata-contract",
    status: RegimeFeatureCandidateStatus = RegimeFeatureCandidateStatus.PLANNED,
) -> RegimeFeatureCandidate:
    return RegimeFeatureCandidate(
        feature_id=feature_id,
        name=name,
        display_name=display_name,
        group=group,
        description=description,
        planned_input_analytics=planned_input_analytics,
        planned_output_kind=planned_output_kind,
        status=status,
    )


def default_regime_feature_candidates() -> list[RegimeFeatureCandidate]:
    return [
        create_regime_feature_candidate(
            "regime-feature-returns-momentum-summary",
            "returns_momentum_summary",
            "Returns Momentum Summary",
            RegimeFeatureGroup.RETURNS,
            "Planned metadata contract for future descriptive returns context; no value is computed in Prompt 34.",
            ["returns_analytics_v0"],
        ),
        create_regime_feature_candidate(
            "regime-feature-volatility-level-summary",
            "volatility_level_summary",
            "Volatility Level Summary",
            RegimeFeatureGroup.VOLATILITY,
            "Planned metadata contract for future volatility context; no value is computed in Prompt 34.",
            ["volatility_analytics_v0"],
        ),
        create_regime_feature_candidate(
            "regime-feature-drawdown-pressure-summary",
            "drawdown_pressure_summary",
            "Drawdown Pressure Summary",
            RegimeFeatureGroup.DRAWDOWN,
            "Planned metadata contract for future drawdown context; no value is computed in Prompt 34.",
            ["drawdown_analytics_v0"],
        ),
        create_regime_feature_candidate(
            "regime-feature-correlation-context-summary",
            "correlation_context_summary",
            "Correlation Context Summary",
            RegimeFeatureGroup.RELATIONSHIP,
            "Planned metadata contract for future correlation context; no value is computed in Prompt 34.",
            ["correlation_analytics_v0"],
        ),
        create_regime_feature_candidate(
            "regime-feature-beta-sensitivity-summary",
            "beta_sensitivity_summary",
            "Beta Sensitivity Summary",
            RegimeFeatureGroup.RELATIONSHIP,
            "Planned metadata contract for future beta context; no value is computed in Prompt 34.",
            ["beta_analytics_v0"],
        ),
        create_regime_feature_candidate(
            "regime-feature-timestamp-gap-quality-flag",
            "timestamp_gap_quality_flag",
            "Timestamp Gap Quality Flag",
            RegimeFeatureGroup.TIME_SERIES_DIAGNOSTICS,
            "Planned metadata contract for future timestamp-gap quality context; no value is computed in Prompt 34.",
            ["time_series_diagnostics_foundation"],
        ),
        create_regime_feature_candidate(
            "regime-feature-interval-irregularity-summary",
            "interval_irregularity_summary",
            "Interval Irregularity Summary",
            RegimeFeatureGroup.TIME_SERIES_DIAGNOSTICS,
            "Planned metadata contract for future interval quality context; no value is computed in Prompt 34.",
            ["time_series_diagnostics_foundation"],
        ),
        create_regime_feature_candidate(
            "regime-feature-volume-liquidity-context-placeholder",
            "volume_liquidity_context_placeholder",
            "Volume Liquidity Context Placeholder",
            RegimeFeatureGroup.VOLUME_LIQUIDITY,
            "Placeholder contract for future volume and liquidity evidence; no value is computed in Prompt 34.",
            ["future_volume_liquidity_evidence"],
        ),
        create_regime_feature_candidate(
            "regime-feature-options-context-placeholder",
            "options_context_placeholder",
            "Options Context Placeholder",
            RegimeFeatureGroup.OPTIONS_CONTEXT,
            "Placeholder contract for future options context evidence; no value is computed in Prompt 34.",
            ["future_options_context_evidence"],
        ),
        create_regime_feature_candidate(
            "regime-feature-macro-context-placeholder",
            "macro_context_placeholder",
            "Macro Context Placeholder",
            RegimeFeatureGroup.MACRO_CONTEXT,
            "Placeholder contract for future macro context evidence; no value is computed in Prompt 34.",
            ["future_macro_context_evidence"],
        ),
        create_regime_feature_candidate(
            "regime-feature-market-microstructure-placeholder",
            "market_microstructure_context_placeholder",
            "Market Microstructure Context Placeholder",
            RegimeFeatureGroup.MARKET_MICROSTRUCTURE,
            "Placeholder contract for future market microstructure evidence; no value is computed in Prompt 34.",
            ["future_market_microstructure_evidence"],
        ),
    ]


def _group_evidence(group: RegimeFeatureGroup) -> list[RegimeEvidenceKind]:
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
    return mapping[group]


def default_regime_feature_group_plans() -> list[RegimeFeatureGroupPlan]:
    candidates = default_regime_feature_candidates()
    groups: list[RegimeFeatureGroupPlan] = []
    for group in [
        RegimeFeatureGroup.RETURNS,
        RegimeFeatureGroup.VOLATILITY,
        RegimeFeatureGroup.DRAWDOWN,
        RegimeFeatureGroup.RELATIONSHIP,
        RegimeFeatureGroup.TIME_SERIES_DIAGNOSTICS,
        RegimeFeatureGroup.VOLUME_LIQUIDITY,
        RegimeFeatureGroup.OPTIONS_CONTEXT,
        RegimeFeatureGroup.MACRO_CONTEXT,
        RegimeFeatureGroup.MARKET_MICROSTRUCTURE,
    ]:
        group_candidates = [candidate for candidate in candidates if candidate.group == group]
        groups.append(
            RegimeFeatureGroupPlan(
                group_id=f"regime-feature-group-{group.value.lower()}",
                group=group,
                description=f"Contracts-only feature preparation group for {group.value.lower()} evidence.",
                candidates=group_candidates,
                required_evidence_kinds=_group_evidence(group),
            )
        )
    return groups
