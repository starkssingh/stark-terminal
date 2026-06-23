import pytest

from stark_terminal_analytics.correlation.calculations import (
    calculate_correlation,
    calculate_pearson_correlation,
    calculate_sample_covariance,
    calculate_sample_variance,
)
from stark_terminal_analytics.correlation.contracts import create_correlation_request
from stark_terminal_analytics.numerical.contracts import create_vector_contract


def test_sample_covariance_is_deterministic() -> None:
    assert calculate_sample_covariance([1.0, 2.0, 3.0], [2.0, 4.0, 6.0]) == pytest.approx(2.0)


def test_sample_variance_is_deterministic() -> None:
    assert calculate_sample_variance([1.0, 2.0, 3.0]) == pytest.approx(1.0)


def test_pearson_correlation_perfect_positive() -> None:
    assert calculate_pearson_correlation([1.0, 2.0, 3.0], [2.0, 4.0, 6.0]) == pytest.approx(1.0)


def test_pearson_correlation_perfect_negative() -> None:
    assert calculate_pearson_correlation([1.0, 2.0, 3.0], [6.0, 4.0, 2.0]) == pytest.approx(-1.0)


def test_zero_variance_correlation_fails_safely() -> None:
    x_vector = create_vector_contract("x", "X", [1.0, 1.0, 1.0])
    y_vector = create_vector_contract("y", "Y", [1.0, 2.0, 3.0])
    request = create_correlation_request("corr", x_vector, y_vector)

    result = calculate_correlation(request)

    assert result.status == "failed"
    assert result.correlation is None
    assert result.covariance is None


def test_calculate_correlation_result_is_descriptive_only() -> None:
    x_vector = create_vector_contract("x", "X", [1.0, 2.0, 3.0])
    y_vector = create_vector_contract("y", "Y", [2.0, 4.0, 6.0])
    result = calculate_correlation(create_correlation_request("corr", x_vector, y_vector))

    assert result.status == "ok"
    assert result.correlation == pytest.approx(1.0)
    assert result.x_source == x_vector.source
    assert result.y_source == y_vector.source
    assert result.descriptive_only is True
    assert result.trade_signal is False
    assert result.recommendation is False
    assert result.decision_object_generated is False
    assert not hasattr(result, "beta")
    assert not hasattr(result, "backtest")
    assert not hasattr(result, "indicator")

