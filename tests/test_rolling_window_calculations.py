import pytest

from stark_terminal_analytics.numerical.contracts import create_vector_contract
from stark_terminal_analytics.rolling.calculations import (
    calculate_rolling_metric,
    rolling_count,
    rolling_max,
    rolling_mean,
    rolling_min,
)
from stark_terminal_analytics.rolling.contracts import RollingMetric, RollingWindowRequest, create_rolling_request


def test_rolling_helpers_are_deterministic() -> None:
    values = [1.0, 3.0, 2.0, 6.0]

    assert rolling_count(values, 2) == [2, 2, 2]
    assert rolling_mean(values, 2) == pytest.approx([2.0, 2.5, 4.0])
    assert rolling_min(values, 2) == [1.0, 2.0, 2.0]
    assert rolling_max(values, 2) == [3.0, 3.0, 6.0]


def test_calculate_rolling_metric_preserves_source_and_counts() -> None:
    vector = create_vector_contract("values", "Values", [1.0, 3.0, 2.0, 6.0])
    request = create_rolling_request("rolling", vector, 2, RollingMetric.MEAN)

    result = calculate_rolling_metric(request)

    assert result.status == "ok"
    assert result.values == pytest.approx([2.0, 2.5, 4.0])
    assert result.input_count == 4
    assert result.output_count == 3
    assert result.source == vector.source
    assert result.descriptive_only is True
    assert result.trade_signal is False
    assert result.recommendation is False
    assert result.decision_object_generated is False


def test_invalid_rolling_window_fails_safely() -> None:
    vector = create_vector_contract("values", "Values", [1.0, 2.0])
    request = RollingWindowRequest.model_construct(
        request_id="rolling",
        vector=vector,
        window=0,
        metric=RollingMetric.MEAN,
        require_finite_values=True,
        require_source_reference=True,
        allow_real_data=False,
        allow_trade_signal=False,
        allow_recommendation=False,
        allow_decision_object=False,
    )

    result = calculate_rolling_metric(request)

    assert result.status == "failed"
    assert result.values == []
    assert result.output_count == 0


def test_rolling_result_has_no_other_market_metrics() -> None:
    vector = create_vector_contract("values", "Values", [1.0, 3.0, 2.0, 6.0])
    result = calculate_rolling_metric(create_rolling_request("rolling", vector, 2, RollingMetric.MAX))

    assert result.status == "ok"
    assert not hasattr(result, "trend_label")
    assert not hasattr(result, "volatility")
    assert not hasattr(result, "drawdown")
    assert not hasattr(result, "correlation")
