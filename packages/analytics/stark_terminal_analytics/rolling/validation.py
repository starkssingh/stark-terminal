from __future__ import annotations

import math

from stark_terminal_analytics.numerical.contracts import NumericalComputationKind, NumericalComputationResult, create_safe_result
from stark_terminal_analytics.numerical.validation import validate_no_signal_fields, validate_source_reference
from stark_terminal_analytics.rolling.contracts import RollingMetric, RollingWindowRequest, RollingWindowResult


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


def validate_rolling_request(
    request: RollingWindowRequest,
    max_window: int | None = None,
) -> NumericalComputationResult:
    source_check = validate_source_reference(request.vector.source)
    finite = all(math.isfinite(value) for value in request.vector.values)
    positive_window = request.window > 0
    within_max = max_window is None or request.window <= max_window
    within_length = request.window <= len(request.vector.values)
    no_signal_fields = validate_no_signal_fields(request)
    metric_known = request.metric != RollingMetric.UNKNOWN
    passed = (
        finite
        and positive_window
        and within_max
        and within_length
        and no_signal_fields
        and metric_known
        and source_check.status == "ok"
        and not request.vector.source.real_market_data
    )
    return _validation_result(
        result_id=f"{request.request_id}_rolling_request_validation",
        request_id=request.request_id,
        passed=passed,
        metrics={
            "input_count": len(request.vector.values),
            "window": request.window,
            "max_window": max_window,
            "positive_window": positive_window,
            "finite": finite,
            "within_max": within_max,
            "within_length": within_length,
            "no_signal_fields": no_signal_fields,
        },
        source=request.vector.source,
        error=None if passed else "rolling request failed validation",
    )


def validate_rolling_result(result: RollingWindowResult) -> NumericalComputationResult:
    source_check = validate_source_reference(result.source)
    no_signal_fields = validate_no_signal_fields(result)
    output_count_matches = result.output_count == len(result.values)
    finite = all(value is None or math.isfinite(float(value)) for value in result.values)
    passed = source_check.status == "ok" and no_signal_fields and output_count_matches and finite
    return _validation_result(
        result_id=f"{result.result_id}_rolling_result_validation",
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
        error=None if passed else "rolling result failed validation",
    )
