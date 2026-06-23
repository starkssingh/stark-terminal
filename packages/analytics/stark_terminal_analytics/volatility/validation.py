from __future__ import annotations

import math

from stark_terminal_analytics.numerical.contracts import (
    NumericalComputationKind,
    NumericalComputationResult,
    NumericalVectorContract,
    create_safe_result,
)
from stark_terminal_analytics.numerical.validation import validate_no_signal_fields, validate_source_reference
from stark_terminal_analytics.volatility.contracts import (
    VolatilityCalculationRequest,
    VolatilityMethod,
    VolatilityResult,
)


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


def validate_return_vector_for_volatility(vector: NumericalVectorContract) -> NumericalComputationResult:
    source_check = validate_source_reference(vector.source)
    finite = all(math.isfinite(value) for value in vector.values)
    enough_values = len(vector.values) >= 2
    passed = enough_values and finite and source_check.status == "ok" and not vector.source.real_market_data
    return _validation_result(
        result_id=f"{vector.vector_id}_volatility_return_validation",
        request_id=f"{vector.vector_id}_volatility_return_validation_request",
        passed=passed,
        metrics={
            "input_count": len(vector.values),
            "finite": finite,
            "source_valid": source_check.status == "ok",
            "real_market_data": vector.source.real_market_data,
        },
        source=vector.source,
        error=None if passed else "return vector must have at least 2 finite values and a safe source reference",
    )


def validate_volatility_request(request: VolatilityCalculationRequest) -> NumericalComputationResult:
    vector_check = validate_return_vector_for_volatility(request.return_vector)
    no_signal_fields = validate_no_signal_fields(request)
    annualization_valid = not request.annualize or (
        request.periods_per_year is not None and request.periods_per_year > 0
    )
    method_valid = request.method in {VolatilityMethod.SAMPLE_STDDEV, VolatilityMethod.POPULATION_STDDEV}
    passed = vector_check.status == "ok" and no_signal_fields and annualization_valid and method_valid
    return _validation_result(
        result_id=f"{request.request_id}_volatility_request_validation",
        request_id=request.request_id,
        passed=passed,
        metrics={
            "input_count": len(request.return_vector.values),
            "method": request.method.value,
            "annualize": request.annualize,
            "annualization_valid": annualization_valid,
            "no_signal_fields": no_signal_fields,
        },
        source=request.return_vector.source,
        error=None if passed else "volatility request failed validation",
    )


def validate_volatility_result(result: VolatilityResult) -> NumericalComputationResult:
    source_check = validate_source_reference(result.source)
    no_signal_fields = validate_no_signal_fields(result)
    volatility_valid = result.volatility is None or math.isfinite(result.volatility)
    annualized_valid = result.annualized_volatility is None or math.isfinite(result.annualized_volatility)
    annualization_consistent = (
        (not result.annualize and result.annualized_volatility is None)
        or (
            result.annualize
            and result.status == "ok"
            and result.annualized_volatility is not None
            and result.periods_per_year is not None
            and result.periods_per_year > 0
        )
        or result.status != "ok"
    )
    passed = (
        source_check.status == "ok"
        and no_signal_fields
        and volatility_valid
        and annualized_valid
        and annualization_consistent
    )
    return _validation_result(
        result_id=f"{result.result_id}_volatility_result_validation",
        request_id=result.request_id,
        passed=passed,
        metrics={
            "input_count": result.input_count,
            "volatility_valid": volatility_valid,
            "annualized_valid": annualized_valid,
            "annualization_consistent": annualization_consistent,
            "no_signal_fields": no_signal_fields,
        },
        source=result.source,
        error=None if passed else "volatility result failed validation",
    )
