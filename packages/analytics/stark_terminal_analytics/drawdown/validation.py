from __future__ import annotations

import math

from stark_terminal_analytics.drawdown.contracts import DrawdownCalculationRequest, DrawdownResult
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


def validate_value_vector_for_drawdown(
    vector: NumericalVectorContract,
    require_positive: bool = True,
) -> NumericalComputationResult:
    source_check = validate_source_reference(vector.source)
    finite = all(math.isfinite(value) for value in vector.values)
    enough_values = len(vector.values) >= 1
    positive = all(value > 0 for value in vector.values)
    passed = (
        enough_values
        and finite
        and (positive or not require_positive)
        and source_check.status == "ok"
        and not vector.source.real_market_data
    )
    return _validation_result(
        result_id=f"{vector.vector_id}_drawdown_value_validation",
        request_id=f"{vector.vector_id}_drawdown_value_validation_request",
        passed=passed,
        metrics={
            "input_count": len(vector.values),
            "finite": finite,
            "positive": positive,
            "source_valid": source_check.status == "ok",
            "real_market_data": vector.source.real_market_data,
        },
        source=vector.source,
        error=None if passed else "drawdown value vector must have finite positive values and a safe source reference",
    )


def validate_drawdown_request(request: DrawdownCalculationRequest) -> NumericalComputationResult:
    value_check = validate_value_vector_for_drawdown(
        request.value_vector,
        require_positive=request.require_positive_values,
    )
    no_signal_fields = validate_no_signal_fields(request)
    passed = value_check.status == "ok" and no_signal_fields
    return _validation_result(
        result_id=f"{request.request_id}_drawdown_request_validation",
        request_id=request.request_id,
        passed=passed,
        metrics={
            "input_count": len(request.value_vector.values),
            "require_positive_values": request.require_positive_values,
            "no_signal_fields": no_signal_fields,
        },
        source=request.value_vector.source,
        error=None if passed else "drawdown request failed validation",
    )


def validate_drawdown_result(result: DrawdownResult) -> NumericalComputationResult:
    source_check = validate_source_reference(result.source)
    no_signal_fields = validate_no_signal_fields(result)
    output_count_matches = result.output_count == len(result.drawdown_values)
    finite = all(math.isfinite(value) for value in result.drawdown_values)
    non_positive = all(value <= 0 for value in result.drawdown_values)
    max_valid = result.max_drawdown is None or result.max_drawdown <= 0
    passed = (
        source_check.status == "ok"
        and no_signal_fields
        and output_count_matches
        and finite
        and non_positive
        and max_valid
    )
    return _validation_result(
        result_id=f"{result.result_id}_drawdown_result_validation",
        request_id=result.request_id,
        passed=passed,
        metrics={
            "input_count": result.input_count,
            "output_count": result.output_count,
            "output_count_matches": output_count_matches,
            "finite": finite,
            "non_positive": non_positive,
            "max_valid": max_valid,
            "no_signal_fields": no_signal_fields,
        },
        source=result.source,
        error=None if passed else "drawdown result failed validation",
    )
