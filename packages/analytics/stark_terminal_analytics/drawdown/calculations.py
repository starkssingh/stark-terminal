from __future__ import annotations

import math

from stark_terminal_analytics.drawdown.contracts import (
    DrawdownCalculationRequest,
    DrawdownResult,
    create_drawdown_result,
)
from stark_terminal_analytics.drawdown.validation import validate_drawdown_request


def _require_positive_values(values: list[float]) -> list[float]:
    if not values:
        raise ValueError("at least 1 value is required")
    if not all(math.isfinite(value) for value in values):
        raise ValueError("values must be finite")
    if not all(value > 0 for value in values):
        raise ValueError("values must be positive")
    return list(values)


def calculate_drawdown_series(values: list[float]) -> list[float]:
    checked = _require_positive_values(values)
    running_peak = checked[0]
    drawdowns: list[float] = []
    for value in checked:
        if value > running_peak:
            running_peak = value
        drawdowns.append((value / running_peak) - 1.0)
    return drawdowns


def calculate_max_drawdown(drawdown_values: list[float]) -> tuple[float, int]:
    if not drawdown_values:
        raise ValueError("drawdown values cannot be empty")
    if not all(math.isfinite(value) for value in drawdown_values):
        raise ValueError("drawdown values must be finite")
    if any(value > 0 for value in drawdown_values):
        raise ValueError("drawdown values must be zero or negative")
    max_drawdown = min(drawdown_values)
    return max_drawdown, drawdown_values.index(max_drawdown)


def calculate_longest_drawdown_duration(drawdown_values: list[float]) -> int:
    if not all(math.isfinite(value) for value in drawdown_values):
        raise ValueError("drawdown values must be finite")
    if any(value > 0 for value in drawdown_values):
        raise ValueError("drawdown values must be zero or negative")
    longest = 0
    current = 0
    for value in drawdown_values:
        if value < 0:
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return longest


def calculate_drawdown(request: DrawdownCalculationRequest) -> DrawdownResult:
    validation = validate_drawdown_request(request)
    if validation.status != "ok":
        return create_drawdown_result(
            result_id=f"{request.request_id}_drawdown",
            request_id=request.request_id,
            drawdown_values=[],
            max_drawdown=None,
            source=request.value_vector.source,
            input_count=len(request.value_vector.values),
            status="failed",
            error=validation.error or "drawdown request failed validation",
        )

    try:
        drawdown_values = calculate_drawdown_series(request.value_vector.values)
        max_drawdown, max_drawdown_index = calculate_max_drawdown(drawdown_values)
        longest_duration = calculate_longest_drawdown_duration(drawdown_values)
        return create_drawdown_result(
            result_id=f"{request.request_id}_drawdown",
            request_id=request.request_id,
            drawdown_values=drawdown_values,
            max_drawdown=max_drawdown,
            source=request.value_vector.source,
            input_count=len(request.value_vector.values),
            max_drawdown_index=max_drawdown_index,
            longest_drawdown_duration=longest_duration,
            status="ok",
        )
    except ValueError as exc:
        return create_drawdown_result(
            result_id=f"{request.request_id}_drawdown",
            request_id=request.request_id,
            drawdown_values=[],
            max_drawdown=None,
            source=request.value_vector.source,
            input_count=len(request.value_vector.values),
            status="failed",
            error=str(exc),
        )
