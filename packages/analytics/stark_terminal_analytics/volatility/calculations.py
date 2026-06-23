from __future__ import annotations

import math

from stark_terminal_analytics.volatility.contracts import (
    VolatilityCalculationRequest,
    VolatilityMethod,
    VolatilityResult,
    create_volatility_result,
)
from stark_terminal_analytics.volatility.validation import validate_volatility_request


def _require_finite_values(values: list[float], minimum_count: int) -> list[float]:
    if len(values) < minimum_count:
        raise ValueError(f"at least {minimum_count} finite values are required")
    if not all(math.isfinite(value) for value in values):
        raise ValueError("values must be finite")
    return list(values)


def calculate_population_stddev(values: list[float]) -> float:
    checked = _require_finite_values(values, minimum_count=1)
    mean = math.fsum(checked) / len(checked)
    variance = math.fsum((value - mean) ** 2 for value in checked) / len(checked)
    return math.sqrt(variance)


def calculate_sample_stddev(values: list[float]) -> float:
    checked = _require_finite_values(values, minimum_count=2)
    mean = math.fsum(checked) / len(checked)
    variance = math.fsum((value - mean) ** 2 for value in checked) / (len(checked) - 1)
    return math.sqrt(variance)


def calculate_volatility(request: VolatilityCalculationRequest) -> VolatilityResult:
    validation = validate_volatility_request(request)
    if validation.status != "ok":
        return create_volatility_result(
            result_id=f"{request.request_id}_volatility",
            request_id=request.request_id,
            method=request.method,
            volatility=None,
            source=request.return_vector.source,
            input_count=len(request.return_vector.values),
            annualize=request.annualize,
            periods_per_year=request.periods_per_year,
            status="failed",
            error=validation.error or "volatility request failed validation",
        )

    try:
        if request.method == VolatilityMethod.SAMPLE_STDDEV:
            volatility = calculate_sample_stddev(request.return_vector.values)
        elif request.method == VolatilityMethod.POPULATION_STDDEV:
            volatility = calculate_population_stddev(request.return_vector.values)
        else:
            raise ValueError("unsupported volatility method")

        annualized = None
        if request.annualize:
            if request.periods_per_year is None or request.periods_per_year <= 0:
                raise ValueError("annualization requires positive periods_per_year")
            annualized = volatility * math.sqrt(request.periods_per_year)

        return create_volatility_result(
            result_id=f"{request.request_id}_volatility",
            request_id=request.request_id,
            method=request.method,
            volatility=volatility,
            source=request.return_vector.source,
            input_count=len(request.return_vector.values),
            annualize=request.annualize,
            periods_per_year=request.periods_per_year,
            annualized_volatility=annualized,
            status="ok",
        )
    except ValueError as exc:
        return create_volatility_result(
            result_id=f"{request.request_id}_volatility",
            request_id=request.request_id,
            method=request.method,
            volatility=None,
            source=request.return_vector.source,
            input_count=len(request.return_vector.values),
            annualize=request.annualize,
            periods_per_year=request.periods_per_year,
            status="failed",
            error=str(exc),
        )
