from __future__ import annotations

import math

from stark_terminal_analytics.correlation.contracts import (
    CorrelationCalculationRequest,
    CorrelationMethod,
    CorrelationResult,
    create_correlation_result,
)
from stark_terminal_analytics.correlation.validation import validate_correlation_request


def _require_paired_values(
    x_values: list[float],
    y_values: list[float],
    minimum_count: int = 2,
) -> tuple[list[float], list[float]]:
    if len(x_values) != len(y_values):
        raise ValueError("paired vectors must have equal length")
    if len(x_values) < minimum_count:
        raise ValueError(f"at least {minimum_count} paired observations are required")
    if not all(math.isfinite(value) for value in x_values + y_values):
        raise ValueError("paired vector values must be finite")
    return list(x_values), list(y_values)


def calculate_sample_covariance(x_values: list[float], y_values: list[float]) -> float:
    x_checked, y_checked = _require_paired_values(x_values, y_values)
    x_mean = math.fsum(x_checked) / len(x_checked)
    y_mean = math.fsum(y_checked) / len(y_checked)
    return math.fsum((x - x_mean) * (y - y_mean) for x, y in zip(x_checked, y_checked)) / (
        len(x_checked) - 1
    )


def calculate_sample_variance(values: list[float]) -> float:
    checked, _ = _require_paired_values(values, values)
    mean = math.fsum(checked) / len(checked)
    return math.fsum((value - mean) ** 2 for value in checked) / (len(checked) - 1)


def calculate_pearson_correlation(x_values: list[float], y_values: list[float]) -> float:
    covariance = calculate_sample_covariance(x_values, y_values)
    x_variance = calculate_sample_variance(x_values)
    y_variance = calculate_sample_variance(y_values)
    if x_variance <= 0 or y_variance <= 0:
        raise ValueError("Pearson correlation is undefined for zero-variance vectors")
    return covariance / math.sqrt(x_variance * y_variance)


def calculate_correlation(request: CorrelationCalculationRequest) -> CorrelationResult:
    validation = validate_correlation_request(request)
    observation_count = len(request.x_vector.values)
    if validation.status != "ok":
        return create_correlation_result(
            result_id=f"{request.request_id}_correlation",
            request_id=request.request_id,
            method=request.method,
            correlation=None,
            covariance=None,
            x_source=request.x_vector.source,
            y_source=request.y_vector.source,
            observation_count=observation_count,
            status="failed",
            error=validation.error or "correlation request failed validation",
        )

    try:
        if request.method != CorrelationMethod.PEARSON:
            raise ValueError("unsupported correlation method")
        covariance = calculate_sample_covariance(request.x_vector.values, request.y_vector.values)
        correlation = calculate_pearson_correlation(request.x_vector.values, request.y_vector.values)
        return create_correlation_result(
            result_id=f"{request.request_id}_correlation",
            request_id=request.request_id,
            method=request.method,
            correlation=correlation,
            covariance=covariance,
            x_source=request.x_vector.source,
            y_source=request.y_vector.source,
            observation_count=observation_count,
            status="ok",
        )
    except ValueError as exc:
        return create_correlation_result(
            result_id=f"{request.request_id}_correlation",
            request_id=request.request_id,
            method=request.method,
            correlation=None,
            covariance=None,
            x_source=request.x_vector.source,
            y_source=request.y_vector.source,
            observation_count=observation_count,
            status="failed",
            error=str(exc),
        )

