from __future__ import annotations

import math

from stark_terminal_analytics.rolling.contracts import (
    RollingMetric,
    RollingWindowRequest,
    RollingWindowResult,
    create_rolling_result,
)
from stark_terminal_analytics.rolling.validation import validate_rolling_request


def _windows(values: list[float], window: int) -> list[list[float]]:
    if window <= 0:
        raise ValueError("rolling window must be positive")
    if window > len(values):
        raise ValueError("rolling window cannot exceed vector length")
    if not all(math.isfinite(value) for value in values):
        raise ValueError("rolling values must be finite")
    return [list(values[index : index + window]) for index in range(0, len(values) - window + 1)]


def rolling_count(values: list[float], window: int) -> list[int]:
    return [len(item) for item in _windows(values, window)]


def rolling_mean(values: list[float], window: int) -> list[float]:
    return [math.fsum(item) / len(item) for item in _windows(values, window)]


def rolling_min(values: list[float], window: int) -> list[float]:
    return [min(item) for item in _windows(values, window)]


def rolling_max(values: list[float], window: int) -> list[float]:
    return [max(item) for item in _windows(values, window)]


def calculate_rolling_metric(request: RollingWindowRequest) -> RollingWindowResult:
    validation = validate_rolling_request(request)
    if validation.status != "ok":
        return create_rolling_result(
            result_id=f"{request.request_id}_rolling",
            request_id=request.request_id,
            metric=request.metric,
            window=max(1, request.window),
            values=[],
            source=request.vector.source,
            input_count=len(request.vector.values),
            status="failed",
            error=validation.error or "rolling request failed validation",
        )

    try:
        if request.metric == RollingMetric.COUNT:
            values = rolling_count(request.vector.values, request.window)
        elif request.metric == RollingMetric.MEAN:
            values = rolling_mean(request.vector.values, request.window)
        elif request.metric == RollingMetric.MIN:
            values = rolling_min(request.vector.values, request.window)
        elif request.metric == RollingMetric.MAX:
            values = rolling_max(request.vector.values, request.window)
        else:
            raise ValueError("unsupported rolling metric")
        return create_rolling_result(
            result_id=f"{request.request_id}_rolling",
            request_id=request.request_id,
            metric=request.metric,
            window=request.window,
            values=values,
            source=request.vector.source,
            input_count=len(request.vector.values),
            status="ok",
        )
    except ValueError as exc:
        return create_rolling_result(
            result_id=f"{request.request_id}_rolling",
            request_id=request.request_id,
            metric=request.metric,
            window=request.window,
            values=[],
            source=request.vector.source,
            input_count=len(request.vector.values),
            status="failed",
            error=str(exc),
        )
