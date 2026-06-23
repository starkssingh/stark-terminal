from pydantic import ValidationError
import pytest

from stark_terminal_analytics.beta.contracts import (
    BetaCalculationRequest,
    BetaMethod,
    BetaResult,
    create_beta_request,
    create_beta_result,
)
from stark_terminal_analytics.numerical.contracts import create_vector_contract


def _vectors():
    return (
        create_vector_contract("asset", "Asset Returns", [0.01, 0.02, 0.03]),
        create_vector_contract("benchmark", "Benchmark Returns", [0.02, 0.04, 0.06]),
    )


def test_valid_beta_request() -> None:
    asset, benchmark = _vectors()

    request = create_beta_request("beta", asset, benchmark)

    assert request.request_id == "beta"
    assert request.method == BetaMethod.SAMPLE_COVARIANCE
    assert request.asset_returns.source == asset.source
    assert request.benchmark_returns.source == benchmark.source


@pytest.mark.parametrize(
    "field",
    ["allow_real_data", "allow_trade_signal", "allow_recommendation", "allow_decision_object"],
)
def test_beta_request_rejects_unsafe_flags(field: str) -> None:
    asset, benchmark = _vectors()

    with pytest.raises(ValidationError):
        BetaCalculationRequest(request_id="beta", asset_returns=asset, benchmark_returns=benchmark, **{field: True})


def test_beta_request_rejects_unequal_lengths() -> None:
    asset = create_vector_contract("asset", "Asset Returns", [0.01, 0.02])
    benchmark = create_vector_contract("benchmark", "Benchmark Returns", [0.02, 0.04, 0.06])

    with pytest.raises(ValidationError):
        BetaCalculationRequest(request_id="beta", asset_returns=asset, benchmark_returns=benchmark)


def test_beta_request_rejects_low_min_observations() -> None:
    asset, benchmark = _vectors()

    with pytest.raises(ValidationError):
        BetaCalculationRequest(request_id="beta", asset_returns=asset, benchmark_returns=benchmark, min_observations=1)


def test_beta_result_preserves_sources() -> None:
    asset, benchmark = _vectors()

    result = create_beta_result(
        "beta_result",
        "beta",
        BetaMethod.SAMPLE_COVARIANCE,
        beta=0.5,
        covariance=0.01,
        benchmark_variance=0.02,
        asset_source=asset.source,
        benchmark_source=benchmark.source,
        observation_count=3,
    )

    assert result.asset_source == asset.source
    assert result.benchmark_source == benchmark.source
    assert result.beta == 0.5
    assert result.descriptive_only is True
    assert result.trade_signal is False
    assert result.recommendation is False
    assert result.decision_object_generated is False


@pytest.mark.parametrize(
    "field",
    ["trade_signal", "recommendation", "decision_object_generated"],
)
def test_beta_result_rejects_unsafe_flags(field: str) -> None:
    asset, benchmark = _vectors()

    with pytest.raises(ValidationError):
        BetaResult(
            result_id="beta_result",
            request_id="beta",
            method=BetaMethod.SAMPLE_COVARIANCE,
            beta=0.5,
            covariance=0.01,
            benchmark_variance=0.02,
            asset_source=asset.source,
            benchmark_source=benchmark.source,
            observation_count=3,
            status="ok",
            **{field: True},
        )

