from __future__ import annotations

import math

from stark_terminal_analytics.beta.contracts import BetaCalculationRequest, BetaMethod, BetaResult
from stark_terminal_analytics.correlation.calculations import calculate_sample_variance
from stark_terminal_analytics.numerical.contracts import (
    NumericalComputationKind,
    NumericalComputationResult,
    NumericalVectorContract,
    create_safe_result,
)
from stark_terminal_analytics.numerical.validation import validate_no_signal_fields, validate_source_reference


def _validation_result(
    result_id: str,
    request_id: str,
    passed: bool,
    metrics: dict[str, float | int | str | bool | None],
    source,
    error: str | None = None,
) -> NumericalComputationResult:
    return create_safe_result(
        result_id=result_id,
        request_id=request_id,
        computation_kind=NumericalComputationKind.VALIDATION,
        metrics=metrics if passed else {},
        source=source if passed else None,
        status="ok" if passed else "failed",
        error=error,
    )


def validate_paired_vectors_for_beta(
    asset_returns: NumericalVectorContract,
    benchmark_returns: NumericalVectorContract,
    min_observations: int = 2,
) -> NumericalComputationResult:
    asset_source_check = validate_source_reference(asset_returns.source)
    benchmark_source_check = validate_source_reference(benchmark_returns.source)
    equal_lengths = len(asset_returns.values) == len(benchmark_returns.values)
    enough_values = (
        len(asset_returns.values) >= min_observations
        and len(benchmark_returns.values) >= min_observations
        and min_observations >= 2
    )
    finite = all(math.isfinite(value) for value in asset_returns.values + benchmark_returns.values)
    benchmark_variance_positive = (
        equal_lengths
        and enough_values
        and finite
        and calculate_sample_variance(benchmark_returns.values) > 0
    )
    safe_sources = (
        asset_source_check.status == "ok"
        and benchmark_source_check.status == "ok"
        and not asset_returns.source.real_market_data
        and not benchmark_returns.source.real_market_data
    )
    passed = equal_lengths and enough_values and finite and benchmark_variance_positive and safe_sources
    return _validation_result(
        result_id=f"{asset_returns.vector_id}_{benchmark_returns.vector_id}_beta_pair_validation",
        request_id=f"{asset_returns.vector_id}_{benchmark_returns.vector_id}_beta_pair_validation_request",
        passed=passed,
        metrics={
            "observation_count": len(asset_returns.values),
            "equal_lengths": equal_lengths,
            "min_observations": min_observations,
            "finite": finite,
            "benchmark_variance_positive": benchmark_variance_positive,
            "sources_valid": safe_sources,
        },
        source=asset_returns.source,
        error=None
        if passed
        else "beta vectors must be equal length, finite, sufficiently long, non-constant benchmark, and source referenced",
    )


def validate_beta_request(request: BetaCalculationRequest) -> NumericalComputationResult:
    pair_check = validate_paired_vectors_for_beta(
        request.asset_returns,
        request.benchmark_returns,
        min_observations=request.min_observations,
    )
    no_signal_fields = validate_no_signal_fields(request)
    method_valid = request.method == BetaMethod.SAMPLE_COVARIANCE
    passed = pair_check.status == "ok" and no_signal_fields and method_valid
    return _validation_result(
        result_id=f"{request.request_id}_beta_request_validation",
        request_id=request.request_id,
        passed=passed,
        metrics={
            "observation_count": len(request.asset_returns.values),
            "method": request.method.value,
            "no_signal_fields": no_signal_fields,
            "method_valid": method_valid,
        },
        source=request.asset_returns.source,
        error=None if passed else "beta request failed validation",
    )


def validate_beta_result(result: BetaResult) -> NumericalComputationResult:
    asset_source_check = validate_source_reference(result.asset_source)
    benchmark_source_check = validate_source_reference(result.benchmark_source)
    no_signal_fields = validate_no_signal_fields(result)
    beta_valid = result.beta is None or math.isfinite(result.beta)
    covariance_valid = result.covariance is None or math.isfinite(result.covariance)
    variance_valid = result.benchmark_variance is None or (
        math.isfinite(result.benchmark_variance) and result.benchmark_variance > 0
    )
    success_value_consistent = result.status != "ok" or result.beta is not None
    passed = (
        asset_source_check.status == "ok"
        and benchmark_source_check.status == "ok"
        and no_signal_fields
        and beta_valid
        and covariance_valid
        and variance_valid
        and success_value_consistent
    )
    return _validation_result(
        result_id=f"{result.result_id}_beta_result_validation",
        request_id=result.request_id,
        passed=passed,
        metrics={
            "observation_count": result.observation_count,
            "beta_valid": beta_valid,
            "covariance_valid": covariance_valid,
            "variance_valid": variance_valid,
            "no_signal_fields": no_signal_fields,
        },
        source=result.asset_source,
        error=None if passed else "beta result failed validation",
    )
