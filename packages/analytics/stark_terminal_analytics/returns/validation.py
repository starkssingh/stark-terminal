from __future__ import annotations

import math

from stark_terminal_analytics.numerical.contracts import (
    NumericalComputationKind,
    NumericalComputationResult,
    NumericalVectorContract,
    create_safe_result,
)
from stark_terminal_analytics.numerical.validation import validate_no_signal_fields, validate_source_reference
from stark_terminal_analytics.returns.contracts import ReturnCalculationRequest, ReturnMethod, ReturnSeriesResult


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


def validate_price_vector_for_returns(
    vector: NumericalVectorContract,
    require_positive: bool = True,
) -> NumericalComputationResult:
    source_check = validate_source_reference(vector.source)
    finite = all(math.isfinite(value) for value in vector.values)
    enough_prices = len(vector.values) >= 2
    positive = all(value > 0 for value in vector.values)
    passed = enough_prices and finite and (positive or not require_positive) and source_check.status == "ok"
    return _validation_result(
        result_id=f"{vector.vector_id}_returns_price_validation",
        request_id=f"{vector.vector_id}_returns_price_validation_request",
        passed=passed,
        metrics={
            "input_count": len(vector.values),
            "finite": finite,
            "positive": positive,
            "source_valid": source_check.status == "ok",
        },
        source=vector.source,
        error=None if passed else "price vector must have at least 2 finite positive values and a safe source reference",
    )


def validate_return_request(request: ReturnCalculationRequest) -> NumericalComputationResult:
    require_positive = request.require_positive_prices or request.method == ReturnMethod.LOG
    price_check = validate_price_vector_for_returns(request.price_vector, require_positive=require_positive)
    no_signal_fields = validate_no_signal_fields(request)
    passed = price_check.status == "ok" and no_signal_fields and not request.price_vector.source.real_market_data
    return _validation_result(
        result_id=f"{request.request_id}_return_request_validation",
        request_id=request.request_id,
        passed=passed,
        metrics={
            "input_count": len(request.price_vector.values),
            "method": request.method.value,
            "require_positive_prices": require_positive,
            "no_signal_fields": no_signal_fields,
        },
        source=request.price_vector.source,
        error=None if passed else "return request failed validation",
    )


def validate_return_result(result: ReturnSeriesResult) -> NumericalComputationResult:
    source_check = validate_source_reference(result.source)
    no_signal_fields = validate_no_signal_fields(result)
    output_count_matches = result.output_count == len(result.values)
    finite = all(math.isfinite(value) for value in result.values)
    passed = source_check.status == "ok" and no_signal_fields and output_count_matches and finite
    return _validation_result(
        result_id=f"{result.result_id}_return_result_validation",
        request_id=result.request_id,
        passed=passed,
        metrics={
            "input_count": result.input_count,
            "output_count": result.output_count,
            "output_count_matches": output_count_matches,
            "finite": finite,
            "no_signal_fields": no_signal_fields,
        },
        source=result.source,
        error=None if passed else "return result failed validation",
    )
