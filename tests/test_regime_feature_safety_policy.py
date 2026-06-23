import pytest
from pydantic import ValidationError

from stark_terminal_analytics.regime_features.contracts import (
    RegimeFeatureCandidate,
    default_regime_feature_candidates,
    default_regime_feature_group_plans,
)
from stark_terminal_analytics.regime_features.safety import (
    RegimeFeatureSafetyPolicy,
    default_regime_feature_safety_policy,
    evaluate_regime_feature_candidate_safety,
    evaluate_regime_feature_plan_safety,
    reject_feature_computation_output,
    reject_feature_signal_or_decision,
)


def test_default_policy_forbids_unsafe_outputs() -> None:
    policy = default_regime_feature_safety_policy()

    assert policy.allow_real_data is False
    assert policy.allow_feature_computation is False
    assert policy.allow_feature_registry_writes is False
    assert policy.allow_classification is False
    assert policy.allow_trade_signals is False
    assert policy.allow_recommendations is False
    assert policy.allow_decision_objects is False
    assert policy.allow_execution is False
    assert policy.require_provenance is True
    assert policy.require_evidence_mapping is True


@pytest.mark.parametrize(
    "override",
    [
        {"policy_id": " "},
        {"name": " "},
        {"allow_real_data": True},
        {"allow_feature_computation": True},
        {"allow_feature_registry_writes": True},
        {"allow_classification": True},
        {"allow_trade_signals": True},
        {"allow_recommendations": True},
        {"allow_decision_objects": True},
        {"allow_execution": True},
        {"require_provenance": False},
        {"require_evidence_mapping": False},
        {"schema_version": " "},
    ],
)
def test_policy_rejects_unsafe_fields(override: dict[str, object]) -> None:
    data = default_regime_feature_safety_policy().model_dump()
    data.update(override)
    with pytest.raises(ValidationError):
        RegimeFeatureSafetyPolicy(**data)


def test_safe_preparation_only_candidate_passes_with_warning_reason() -> None:
    candidate = default_regime_feature_candidates()[0]
    result = evaluate_regime_feature_candidate_safety(candidate, default_regime_feature_safety_policy())

    assert result.decision == "preparation_allowed"
    assert result.reasons


def test_unsafe_candidate_blocks() -> None:
    data = default_regime_feature_candidates()[0].model_dump()
    data["computation_allowed"] = True

    with pytest.raises(ValidationError):
        RegimeFeatureCandidate(**data)


def test_safe_plan_passes_and_missing_plan_blocks() -> None:
    policy = default_regime_feature_safety_policy()

    safe_result = evaluate_regime_feature_plan_safety(
        default_regime_feature_candidates(),
        default_regime_feature_group_plans(),
        policy,
    )
    missing_result = evaluate_regime_feature_plan_safety([], [], policy)

    assert safe_result.decision == "preparation_allowed"
    assert missing_result.decision == "blocked"
    assert "regime feature candidates are missing" in missing_result.reasons


def test_reject_helpers_block_computation_and_signals() -> None:
    assert reject_feature_computation_output().decision == "blocked"
    assert reject_feature_signal_or_decision().decision == "blocked"

