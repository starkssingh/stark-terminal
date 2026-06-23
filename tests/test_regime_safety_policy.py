import pytest

from stark_terminal_analytics.regime.contracts import default_regime_analytics_plan
from stark_terminal_analytics.regime.safety import (
    RegimeSafetyPolicy,
    default_regime_safety_policy,
    evaluate_regime_plan_safety,
    reject_regime_classification_output,
    reject_regime_signal_or_decision,
)


def test_default_regime_safety_policy_forbids_unsafe_capabilities() -> None:
    policy = default_regime_safety_policy()

    assert policy.allow_classification is False
    assert policy.allow_real_data is False
    assert policy.allow_trade_signals is False
    assert policy.allow_recommendations is False
    assert policy.allow_decision_objects is False
    assert policy.allow_execution is False
    assert policy.require_evidence is True
    assert policy.require_human_review is True


@pytest.mark.parametrize(
    "override",
    [
        {"allow_classification": True},
        {"allow_real_data": True},
        {"allow_trade_signals": True},
        {"allow_recommendations": True},
        {"allow_decision_objects": True},
        {"allow_execution": True},
        {"require_evidence": False},
        {"require_human_review": False},
    ],
)
def test_regime_safety_policy_rejects_unsafe_flags(override: dict[str, object]) -> None:
    data = {
        "policy_id": "policy",
        "name": "Policy",
    }
    data.update(override)

    with pytest.raises(ValueError):
        RegimeSafetyPolicy(**data)


def test_safe_planning_only_plan_passes_safety_policy() -> None:
    result = evaluate_regime_plan_safety(default_regime_analytics_plan(), default_regime_safety_policy())

    assert result.decision == "planning_allowed"
    assert result.reasons


def test_unsafe_plan_blocks() -> None:
    plan = default_regime_analytics_plan().model_copy(update={"classification_allowed": True})
    policy = default_regime_safety_policy()

    result = evaluate_regime_plan_safety(plan, policy)

    assert result.decision == "blocked"
    assert any("classification" in reason for reason in result.reasons)


def test_reject_helpers_block_classification_and_signal_outputs() -> None:
    classification = reject_regime_classification_output()
    signal = reject_regime_signal_or_decision()

    assert classification.decision == "blocked"
    assert signal.decision == "blocked"
    assert classification.reasons
    assert signal.reasons
