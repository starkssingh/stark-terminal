import math

import pytest

from stark_terminal_analytics.numerical.contracts import create_vector_contract
from stark_terminal_analytics.returns.calculations import calculate_log_returns, calculate_returns, calculate_simple_returns
from stark_terminal_analytics.returns.contracts import ReturnMethod, create_return_request


def test_simple_returns_are_deterministic() -> None:
    values = calculate_simple_returns([100.0, 110.0, 99.0])

    assert values == pytest.approx([0.1, -0.1])


def test_log_returns_are_deterministic() -> None:
    values = calculate_log_returns([100.0, 110.0, 99.0])

    assert values == pytest.approx([math.log(1.1), math.log(0.9)])


def test_calculate_returns_preserves_source_and_counts() -> None:
    vector = create_vector_contract("prices", "Prices", [100.0, 110.0, 99.0])
    request = create_return_request("returns", vector, ReturnMethod.SIMPLE)

    result = calculate_returns(request)

    assert result.status == "ok"
    assert result.input_count == 3
    assert result.output_count == 2
    assert result.source == vector.source
    assert result.descriptive_only is True
    assert result.trade_signal is False
    assert result.recommendation is False
    assert result.decision_object_generated is False


def test_log_returns_fail_safely_for_zero_or_negative_prices() -> None:
    vector = create_vector_contract("prices", "Prices", [100.0, 0.0, 101.0])
    request = create_return_request("returns", vector, ReturnMethod.LOG)

    result = calculate_returns(request)

    assert result.status == "failed"
    assert result.values == []
    assert result.output_count == 0


def test_invalid_inputs_fail_safely_and_do_not_emit_other_metrics() -> None:
    vector = create_vector_contract("prices", "Prices", [100.0])
    request = create_return_request("returns", vector, ReturnMethod.SIMPLE)

    result = calculate_returns(request)

    assert result.status == "failed"
    assert result.values == []
    assert not hasattr(result, "annualized_return")
    assert not hasattr(result, "volatility")
    assert not hasattr(result, "drawdown")
    assert not hasattr(result, "correlation")
