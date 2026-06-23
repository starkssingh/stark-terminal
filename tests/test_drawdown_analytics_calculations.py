import pytest

from stark_terminal_analytics.drawdown.calculations import (
    calculate_drawdown,
    calculate_drawdown_series,
    calculate_longest_drawdown_duration,
    calculate_max_drawdown,
)
from stark_terminal_analytics.drawdown.contracts import create_drawdown_request
from stark_terminal_analytics.numerical.contracts import create_vector_contract


def test_drawdown_series_is_deterministic() -> None:
    values = [100.0, 110.0, 105.0, 120.0, 90.0, 95.0, 130.0]

    drawdowns = calculate_drawdown_series(values)

    assert drawdowns == pytest.approx([0.0, 0.0, -0.0454545455, 0.0, -0.25, -0.2083333333, 0.0])
    assert all(value <= 0 for value in drawdowns)


def test_max_drawdown_is_deterministic() -> None:
    drawdowns = [0.0, 0.0, -0.0454545455, 0.0, -0.25, -0.2083333333, 0.0]

    max_drawdown, index = calculate_max_drawdown(drawdowns)

    assert max_drawdown == pytest.approx(-0.25)
    assert index == 4


def test_longest_drawdown_duration_is_deterministic() -> None:
    drawdowns = [0.0, -0.1, -0.05, 0.0, -0.2, -0.1, -0.05]

    assert calculate_longest_drawdown_duration(drawdowns) == 3


def test_calculate_drawdown_preserves_source_and_counts() -> None:
    vector = create_vector_contract("values", "Values", [100.0, 110.0, 90.0])
    request = create_drawdown_request("drawdown", vector)

    result = calculate_drawdown(request)

    assert result.status == "ok"
    assert result.input_count == 3
    assert result.output_count == 3
    assert result.max_drawdown == pytest.approx(-0.1818181818)
    assert result.max_drawdown_index == 2
    assert result.longest_drawdown_duration == 1
    assert result.source == vector.source
    assert result.descriptive_only is True
    assert result.trade_signal is False
    assert result.recommendation is False
    assert result.decision_object_generated is False


def test_invalid_drawdown_input_fails_safely() -> None:
    vector = create_vector_contract("values", "Values", [100.0, 0.0])
    request = create_drawdown_request("drawdown", vector)

    result = calculate_drawdown(request)

    assert result.status == "failed"
    assert result.drawdown_values == []
    assert result.max_drawdown is None


def test_drawdown_result_has_no_other_risk_or_strategy_metrics() -> None:
    vector = create_vector_contract("values", "Values", [100.0, 110.0, 90.0])
    result = calculate_drawdown(create_drawdown_request("drawdown", vector))

    assert result.status == "ok"
    assert not hasattr(result, "volatility")
    assert not hasattr(result, "correlation")
    assert not hasattr(result, "beta")
    assert not hasattr(result, "regime")
