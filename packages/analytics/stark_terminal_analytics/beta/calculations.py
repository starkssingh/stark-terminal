from __future__ import annotations

from stark_terminal_analytics.beta.contracts import (
    BetaCalculationRequest,
    BetaMethod,
    BetaResult,
    create_beta_result,
)
from stark_terminal_analytics.beta.validation import validate_beta_request
from stark_terminal_analytics.correlation.calculations import (
    calculate_sample_covariance,
    calculate_sample_variance,
)


def calculate_beta(asset_returns: list[float], benchmark_returns: list[float]) -> float:
    covariance = calculate_sample_covariance(asset_returns, benchmark_returns)
    benchmark_variance = calculate_sample_variance(benchmark_returns)
    if benchmark_variance <= 0:
        raise ValueError("beta is undefined when benchmark variance is zero")
    return covariance / benchmark_variance


def calculate_beta_from_request(request: BetaCalculationRequest) -> BetaResult:
    validation = validate_beta_request(request)
    observation_count = len(request.asset_returns.values)
    if validation.status != "ok":
        return create_beta_result(
            result_id=f"{request.request_id}_beta",
            request_id=request.request_id,
            method=request.method,
            beta=None,
            covariance=None,
            benchmark_variance=None,
            asset_source=request.asset_returns.source,
            benchmark_source=request.benchmark_returns.source,
            observation_count=observation_count,
            status="failed",
            error=validation.error or "beta request failed validation",
        )

    try:
        if request.method != BetaMethod.SAMPLE_COVARIANCE:
            raise ValueError("unsupported beta method")
        covariance = calculate_sample_covariance(request.asset_returns.values, request.benchmark_returns.values)
        benchmark_variance = calculate_sample_variance(request.benchmark_returns.values)
        if benchmark_variance <= 0:
            raise ValueError("beta is undefined when benchmark variance is zero")
        beta = covariance / benchmark_variance
        return create_beta_result(
            result_id=f"{request.request_id}_beta",
            request_id=request.request_id,
            method=request.method,
            beta=beta,
            covariance=covariance,
            benchmark_variance=benchmark_variance,
            asset_source=request.asset_returns.source,
            benchmark_source=request.benchmark_returns.source,
            observation_count=observation_count,
            status="ok",
        )
    except ValueError as exc:
        return create_beta_result(
            result_id=f"{request.request_id}_beta",
            request_id=request.request_id,
            method=request.method,
            beta=None,
            covariance=None,
            benchmark_variance=None,
            asset_source=request.asset_returns.source,
            benchmark_source=request.benchmark_returns.source,
            observation_count=observation_count,
            status="failed",
            error=str(exc),
        )

