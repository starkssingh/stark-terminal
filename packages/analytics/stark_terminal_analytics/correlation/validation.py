from __future__ import annotations

import math

from stark_terminal_analytics.correlation.contracts import (
    CorrelationCalculationRequest,
    CorrelationMethod,
    CorrelationResult,
)
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


def _sample_variance(values: list[float]) -> float:
    mean = math.fsum(values) / len(values)
    return math.fsum((value - mean) ** 2 for value in values) / (len(values) - 1)


def validate_paired_vectors_for_correlation(
    x_vector: NumericalVectorContract,
    y_vector: NumericalVectorContract,
    min_observations: int = 2,
) -> NumericalComputationResult:
    x_source_check = validate_source_reference(x_vector.source)
    y_source_check = validate_source_reference(y_vector.source)
    equal_lengths = len(x_vector.values) == len(y_vector.values)
    enough_values = (
        len(x_vector.values) >= min_observations
        and len(y_vector.values) >= min_observations
        and min_observations >= 2
    )
    finite = all(math.isfinite(value) for value in x_vector.values + y_vector.values)
    variance_safe = equal_lengths and enough_values and finite
    x_variance_positive = variance_safe and _sample_variance(x_vector.values) > 0
    y_variance_positive = variance_safe and _sample_variance(y_vector.values) > 0
    safe_sources = (
        x_source_check.status == "ok"
        and y_source_check.status == "ok"
        and not x_vector.source.real_market_data
        and not y_vector.source.real_market_data
    )
    passed = equal_lengths and enough_values and finite and x_variance_positive and y_variance_positive and safe_sources
    return _validation_result(
        result_id=f"{x_vector.vector_id}_{y_vector.vector_id}_correlation_pair_validation",
        request_id=f"{x_vector.vector_id}_{y_vector.vector_id}_correlation_pair_validation_request",
        passed=passed,
        metrics={
            "observation_count": len(x_vector.values),
            "equal_lengths": equal_lengths,
            "min_observations": min_observations,
            "finite": finite,
            "x_variance_positive": x_variance_positive,
            "y_variance_positive": y_variance_positive,
            "sources_valid": safe_sources,
        },
        source=x_vector.source,
        error=None
        if passed
        else "correlation vectors must be equal length, finite, sufficiently long, non-constant, and source referenced",
    )


def validate_correlation_request(request: CorrelationCalculationRequest) -> NumericalComputationResult:
    pair_check = validate_paired_vectors_for_correlation(
        request.x_vector,
        request.y_vector,
        min_observations=request.min_observations,
    )
    no_signal_fields = validate_no_signal_fields(request)
    method_valid = request.method == CorrelationMethod.PEARSON
    passed = pair_check.status == "ok" and no_signal_fields and method_valid
    return _validation_result(
        result_id=f"{request.request_id}_correlation_request_validation",
        request_id=request.request_id,
        passed=passed,
        metrics={
            "observation_count": len(request.x_vector.values),
            "method": request.method.value,
            "no_signal_fields": no_signal_fields,
            "method_valid": method_valid,
        },
        source=request.x_vector.source,
        error=None if passed else "correlation request failed validation",
    )


def validate_correlation_result(result: CorrelationResult) -> NumericalComputationResult:
    x_source_check = validate_source_reference(result.x_source)
    y_source_check = validate_source_reference(result.y_source)
    no_signal_fields = validate_no_signal_fields(result)
    correlation_valid = (
        result.correlation is None
        or (
            math.isfinite(result.correlation)
            and -1.000000000001 <= result.correlation <= 1.000000000001
        )
    )
    covariance_valid = result.covariance is None or math.isfinite(result.covariance)
    success_value_consistent = result.status != "ok" or result.correlation is not None
    passed = (
        x_source_check.status == "ok"
        and y_source_check.status == "ok"
        and no_signal_fields
        and correlation_valid
        and covariance_valid
        and success_value_consistent
    )
    return _validation_result(
        result_id=f"{result.result_id}_correlation_result_validation",
        request_id=result.request_id,
        passed=passed,
        metrics={
            "observation_count": result.observation_count,
            "correlation_valid": correlation_valid,
            "covariance_valid": covariance_valid,
            "no_signal_fields": no_signal_fields,
        },
        source=result.x_source,
        error=None if passed else "correlation result failed validation",
    )
