import pytest
from pydantic import ValidationError

from stark_terminal_analytics.regime.contracts import RegimeEvidenceKind
from stark_terminal_analytics.regime_features.contracts import (
    RegimeFeatureCandidate,
    RegimeFeatureCandidateStatus,
    RegimeFeatureGroup,
    RegimeFeatureGroupPlan,
    RegimeFeaturePreparationStage,
    create_regime_feature_candidate,
    default_regime_feature_candidates,
    default_regime_feature_group_plans,
)


def _candidate() -> RegimeFeatureCandidate:
    return create_regime_feature_candidate(
        "feature-test",
        "returns_momentum_summary",
        "Returns Momentum Summary",
        RegimeFeatureGroup.RETURNS,
        "Metadata-only candidate.",
        ["returns_analytics_v0"],
    )


def test_valid_regime_feature_candidate() -> None:
    candidate = _candidate()

    assert candidate.computation_allowed is False
    assert candidate.registry_write_allowed is False
    assert candidate.classification_allowed is False
    assert candidate.trade_signal is False
    assert candidate.recommendation is False
    assert candidate.decision_object_generated is False
    assert candidate.preparation_stage == RegimeFeaturePreparationStage.CONTRACTS_ONLY


@pytest.mark.parametrize(
    "override",
    [
        {"feature_id": " "},
        {"name": " "},
        {"display_name": " "},
        {"description": " "},
        {"planned_input_analytics": []},
        {"planned_output_kind": " "},
        {"group": RegimeFeatureGroup.UNKNOWN},
        {"status": RegimeFeatureCandidateStatus.UNKNOWN},
        {"preparation_stage": RegimeFeaturePreparationStage.UNKNOWN},
        {"computation_allowed": True},
        {"registry_write_allowed": True},
        {"classification_allowed": True},
        {"trade_signal": True},
        {"recommendation": True},
        {"decision_object_generated": True},
    ],
)
def test_regime_feature_candidate_rejects_unsafe_or_invalid_fields(override: dict[str, object]) -> None:
    data = _candidate().model_dump()
    data.update(override)
    with pytest.raises(ValidationError):
        RegimeFeatureCandidate(**data)


def test_default_candidates_exist_and_are_metadata_only() -> None:
    candidates = default_regime_feature_candidates()

    assert {candidate.name for candidate in candidates} >= {
        "returns_momentum_summary",
        "volatility_level_summary",
        "drawdown_pressure_summary",
        "correlation_context_summary",
        "beta_sensitivity_summary",
        "timestamp_gap_quality_flag",
        "interval_irregularity_summary",
        "volume_liquidity_context_placeholder",
        "options_context_placeholder",
        "macro_context_placeholder",
    }
    assert all(not candidate.computation_allowed for candidate in candidates)
    assert all(not candidate.registry_write_allowed for candidate in candidates)
    assert all(not candidate.classification_allowed for candidate in candidates)


def test_valid_regime_feature_group_plan() -> None:
    candidate = _candidate()
    group = RegimeFeatureGroupPlan(
        group_id="returns-group",
        group=RegimeFeatureGroup.RETURNS,
        description="Returns candidates.",
        candidates=[candidate],
        required_evidence_kinds=[RegimeEvidenceKind.RETURNS],
    )

    assert group.computation_allowed is False
    assert group.classification_allowed is False


@pytest.mark.parametrize(
    "override",
    [
        {"group_id": " "},
        {"group": RegimeFeatureGroup.UNKNOWN},
        {"description": " "},
        {"candidates": []},
        {"required_evidence_kinds": []},
        {"required_evidence_kinds": [RegimeEvidenceKind.UNKNOWN]},
        {"computation_allowed": True},
        {"classification_allowed": True},
    ],
)
def test_group_plan_rejects_unsafe_or_invalid_fields(override: dict[str, object]) -> None:
    group = default_regime_feature_group_plans()[0]
    data = group.model_dump()
    data.update(override)
    with pytest.raises(ValidationError):
        RegimeFeatureGroupPlan(**data)
