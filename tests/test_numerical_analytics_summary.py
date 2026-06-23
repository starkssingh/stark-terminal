from math import inf

from stark_terminal_analytics.numerical.contracts import NumericalVectorContract, create_synthetic_source_reference, create_vector_contract
from stark_terminal_analytics.numerical.summary import (
    numeric_count,
    numeric_max,
    numeric_mean,
    numeric_min,
    safe_numeric_summary,
)


def test_numeric_summary_helpers_are_deterministic() -> None:
    values = [1.0, 2.0, 4.0]

    assert numeric_count(values) == 3
    assert numeric_min(values) == 1.0
    assert numeric_max(values) == 4.0
    assert numeric_mean(values) == 7.0 / 3.0
    assert values == [1.0, 2.0, 4.0]


def test_safe_numeric_summary_returns_descriptive_metrics_only() -> None:
    vector = create_vector_contract("vec", "Vector", [1.0, 2.0, 4.0])
    result = safe_numeric_summary(vector)

    assert result.status == "ok"
    assert set(result.metrics) == {"count", "min", "max", "mean"}
    assert result.metrics["count"] == 3
    assert result.descriptive_only is True
    assert result.trade_signal is False
    assert result.recommendation is False
    assert result.decision_object_generated is False
    assert "return" not in result.metrics
    assert "volatility" not in result.metrics
    assert "drawdown" not in result.metrics
    assert "correlation" not in result.metrics


def test_safe_numeric_summary_fails_safely_for_non_finite_values() -> None:
    source = create_synthetic_source_reference()
    vector = NumericalVectorContract(
        vector_id="vec",
        name="Vector",
        values=[1.0, inf],
        source=source,
        finite_required=False,
    )
    result = safe_numeric_summary(vector)

    assert result.status == "failed"
    assert result.metrics == {}
    assert result.trade_signal is False
    assert result.recommendation is False


def test_safe_numeric_summary_fails_safely_for_empty_constructed_vector() -> None:
    source = create_synthetic_source_reference()
    vector = NumericalVectorContract.model_construct(
        vector_id="vec",
        name="Vector",
        values=[],
        source=source,
        finite_required=True,
    )
    result = safe_numeric_summary(vector)

    assert result.status == "failed"
    assert result.metrics == {}
    assert result.decision_object_generated is False
