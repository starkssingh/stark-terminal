from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_analytics.regime_features.contracts import (
    default_regime_feature_candidates,
    default_regime_feature_group_plans,
)


class RegimeFeaturePreparationHealthStatus(BaseModel):
    enabled: bool
    schema_version: str
    dependency_stage: str
    real_data_allowed: bool
    feature_computation_allowed: bool
    feature_registry_writes_allowed: bool
    classification_allowed: bool
    trade_signals_allowed: bool
    recommendations_allowed: bool
    decision_objects_allowed: bool
    execution_allowed: bool = False
    provenance_required: bool
    evidence_mapping_required: bool
    candidate_count: int
    group_count: int
    status: str
    error: str | None = None


def check_regime_feature_preparation_health(
    settings: Settings | None = None,
) -> RegimeFeaturePreparationHealthStatus:
    resolved = settings or get_settings()
    candidates = default_regime_feature_candidates()
    groups = default_regime_feature_group_plans()
    unsafe_flags = (
        resolved.regime_feature_preparation_allow_real_data
        or resolved.regime_feature_preparation_allow_feature_computation
        or resolved.regime_feature_preparation_allow_feature_registry_writes
        or resolved.regime_feature_preparation_allow_classification
        or resolved.regime_feature_preparation_allow_trade_signals
        or resolved.regime_feature_preparation_allow_recommendations
        or resolved.regime_feature_preparation_allow_decision_objects
        or resolved.execution_apis_enabled
    )
    has_required_configuration = (
        bool(resolved.regime_feature_preparation_schema_version.strip())
        and resolved.regime_feature_preparation_dependency_stage == "contracts_only"
        and resolved.regime_feature_preparation_require_provenance
        and resolved.regime_feature_preparation_require_evidence_mapping
        and bool(candidates)
        and bool(groups)
    )
    status = "healthy" if resolved.regime_feature_preparation_enabled and not unsafe_flags and has_required_configuration else "blocked"
    error = None if status == "healthy" else "regime feature preparation safety flags are not fail-closed"
    return RegimeFeaturePreparationHealthStatus(
        enabled=resolved.regime_feature_preparation_enabled,
        schema_version=resolved.regime_feature_preparation_schema_version,
        dependency_stage=resolved.regime_feature_preparation_dependency_stage,
        real_data_allowed=resolved.regime_feature_preparation_allow_real_data,
        feature_computation_allowed=resolved.regime_feature_preparation_allow_feature_computation,
        feature_registry_writes_allowed=resolved.regime_feature_preparation_allow_feature_registry_writes,
        classification_allowed=resolved.regime_feature_preparation_allow_classification,
        trade_signals_allowed=resolved.regime_feature_preparation_allow_trade_signals,
        recommendations_allowed=resolved.regime_feature_preparation_allow_recommendations,
        decision_objects_allowed=resolved.regime_feature_preparation_allow_decision_objects,
        execution_allowed=False,
        provenance_required=resolved.regime_feature_preparation_require_provenance,
        evidence_mapping_required=resolved.regime_feature_preparation_require_evidence_mapping,
        candidate_count=len(candidates),
        group_count=len(groups),
        status=status,
        error=error,
    )
