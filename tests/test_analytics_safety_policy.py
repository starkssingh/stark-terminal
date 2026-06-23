from pydantic import ValidationError
import pytest

from stark_terminal_analytics.foundation.contracts import (
    AnalyticsOutputContract,
    AnalyticsOutputKind,
    AnalyticsSafetyLevel,
    create_default_descriptive_output_contract,
)
from stark_terminal_analytics.foundation.safety import (
    AnalyticsSafetyPolicy,
    default_analytics_safety_policy,
    evaluate_analytics_output_contract,
    reject_signal_or_recommendation_contract,
)


def test_default_analytics_safety_policy_forbids_trade_actionable_outputs() -> None:
    policy = default_analytics_safety_policy()

    assert policy.allow_real_data is False
    assert policy.allow_trade_signals is False
    assert policy.allow_recommendations is False
    assert policy.allow_execution is False
    assert policy.require_validated_inputs is True
    assert policy.require_source_reference is True


@pytest.mark.parametrize(
    "overrides",
    [
        {"allow_real_data": True},
        {"allow_trade_signals": True},
        {"allow_recommendations": True},
        {"allow_execution": True},
        {"require_validated_inputs": False},
        {"require_source_reference": False},
    ],
)
def test_analytics_safety_policy_rejects_unsafe_flags(overrides: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        AnalyticsSafetyPolicy(policy_id="policy", name="Unsafe policy", **overrides)


def test_evaluate_descriptive_output_allows_safely() -> None:
    output = create_default_descriptive_output_contract("output", "Output")
    result = evaluate_analytics_output_contract(output, default_analytics_safety_policy())

    assert result.decision == "ALLOW"
    assert "descriptive/research-only" in result.reasons[0]


@pytest.mark.parametrize(
    "unsafe_flag",
    ["trade_signal", "recommendation", "execution_ready"],
)
def test_evaluate_unsafe_output_blocks(unsafe_flag: str) -> None:
    unsafe_output = AnalyticsOutputContract.model_construct(
        contract_id="unsafe",
        name="Unsafe",
        output_kind=AnalyticsOutputKind.TIME_SERIES_METRIC,
        safety_level=AnalyticsSafetyLevel.RESEARCH_ONLY,
        descriptive_only=True,
        trade_signal=unsafe_flag == "trade_signal",
        recommendation=unsafe_flag == "recommendation",
        execution_ready=unsafe_flag == "execution_ready",
        requires_interpretation=True,
        schema_version="v1",
        notes=[],
    )

    reasons = reject_signal_or_recommendation_contract(unsafe_output)
    result = evaluate_analytics_output_contract(unsafe_output, default_analytics_safety_policy())

    assert reasons
    assert result.decision == "BLOCK"

def test_analytics_notes_are_sanitized() -> None:
    output = AnalyticsOutputContract(
        contract_id="safe",
        name="Safe",
        output_kind=AnalyticsOutputKind.DESCRIPTIVE_STATISTIC,
        safety_level=AnalyticsSafetyLevel.RESEARCH_ONLY,
        notes=["contains token secret"],
    )

    assert output.notes == ["[redacted]"]

