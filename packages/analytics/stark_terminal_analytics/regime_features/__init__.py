"""Regime feature preparation contracts.

Prompt 34 keeps this package contracts-only: no feature computation, no
registry writes, no regime classification, no signals, and no execution APIs.
"""

from stark_terminal_analytics.regime_features.contracts import (
    RegimeFeatureCandidate,
    RegimeFeatureCandidateStatus,
    RegimeFeatureGroup,
    RegimeFeatureGroupPlan,
    RegimeFeaturePreparationStage,
    RegimeFeatureSafetyLabel,
    default_regime_feature_candidates,
    default_regime_feature_group_plans,
)

__all__ = [
    "RegimeFeatureCandidate",
    "RegimeFeatureCandidateStatus",
    "RegimeFeatureGroup",
    "RegimeFeatureGroupPlan",
    "RegimeFeaturePreparationStage",
    "RegimeFeatureSafetyLabel",
    "default_regime_feature_candidates",
    "default_regime_feature_group_plans",
]
