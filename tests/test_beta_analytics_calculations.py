import pytest

from stark_terminal_analytics.beta.calculations import calculate_beta, calculate_beta_from_request
from stark_terminal_analytics.beta.contracts import create_beta_request
from stark_terminal_analytics.correlation.calculations import calculate_sample_covariance, calculate_sample_variance
from stark_terminal_analytics.numerical.contracts import create_vector_contract


def test_beta_is_deterministic() -> None:
    assert calculate_beta([1.0, 2.0, 3.0], [2.0, 4.0, 6.0]) == pytest.approx(0.5)


def test_beta_equals_covariance_over_benchmark_variance() -> None:
    asset = [0.01, 0.02, 0.03]
    benchmark = [0.02, 0.04, 0.06]
    expected = calculate_sample_covariance(asset, benchmark) / calculate_sample_variance(benchmark)

    assert calculate_beta(asset, benchmark) == pytest.approx(expected)


def test_zero_benchmark_variance_fails_safely() -> None:
    asset = create_vector_contract("asset", "Asset Returns", [0.01, 0.02, 0.03])
    benchmark = create_vector_contract("benchmark", "Benchmark Returns", [0.02, 0.02, 0.02])

    result = calculate_beta_from_request(create_beta_request("beta", asset, benchmark))

    assert result.status == "failed"
    assert result.beta is None
    assert result.benchmark_variance is None


def test_calculate_beta_result_is_descriptive_only() -> None:
    asset = create_vector_contract("asset", "Asset Returns", [0.01, 0.02, 0.03])
    benchmark = create_vector_contract("benchmark", "Benchmark Returns", [0.02, 0.04, 0.06])
    result = calculate_beta_from_request(create_beta_request("beta", asset, benchmark))

    assert result.status == "ok"
    assert result.beta == pytest.approx(0.5)
    assert result.asset_source == asset.source
    assert result.benchmark_source == benchmark.source
    assert result.descriptive_only is True
    assert result.trade_signal is False
    assert result.recommendation is False
    assert result.decision_object_generated is False
    assert not hasattr(result, "correlation")
    assert not hasattr(result, "backtest")
    assert not hasattr(result, "indicator")

