from __future__ import annotations

import math

from stark_terminal_analytics.returns.contracts import (
    ReturnCalculationRequest,
    ReturnMethod,
    ReturnSeriesResult,
    create_return_result,
)
from stark_terminal_analytics.returns.validation import validate_return_request


def _require_prices(values: list[float], require_positive: bool = False) -> list[float]:
    if len(values) < 2:
        raise ValueError("at least 2 prices are required")
    if not all(math.isfinite(value) for value in values):
        raise ValueError("prices must be finite")
    if require_positive and not all(value > 0 for value in values):
        raise ValueError("prices must be positive")
    return list(values)


def calculate_simple_returns(prices: list[float]) -> list[float]:
    checked = _require_prices(prices, require_positive=False)
    returns: list[float] = []
    for previous, current in zip(checked, checked[1:]):
        if previous == 0:
            raise ValueError("previous price cannot be zero")
        returns.append((current / previous) - 1.0)
    return returns


def calculate_log_returns(prices: list[float]) -> list[float]:
    checked = _require_prices(prices, require_positive=True)
    return [math.log(current / previous) for previous, current in zip(checked, checked[1:])]


def calculate_returns(request: ReturnCalculationRequest) -> ReturnSeriesResult:
    validation = validate_return_request(request)
    if validation.status != "ok":
        return create_return_result(
            result_id=f"{request.request_id}_returns",
            request_id=request.request_id,
            method=request.method,
            values=[],
            source=request.price_vector.source,
            input_count=len(request.price_vector.values),
            status="failed",
            error=validation.error or "return request failed validation",
        )

    try:
        if request.method == ReturnMethod.SIMPLE:
            values = calculate_simple_returns(request.price_vector.values)
        elif request.method == ReturnMethod.LOG:
            values = calculate_log_returns(request.price_vector.values)
        else:
            raise ValueError("unsupported return method")
        return create_return_result(
            result_id=f"{request.request_id}_returns",
            request_id=request.request_id,
            method=request.method,
            values=values,
            source=request.price_vector.source,
            input_count=len(request.price_vector.values),
            status="ok",
        )
    except ValueError as exc:
        return create_return_result(
            result_id=f"{request.request_id}_returns",
            request_id=request.request_id,
            method=request.method,
            values=[],
            source=request.price_vector.source,
            input_count=len(request.price_vector.values),
            status="failed",
            error=str(exc),
        )
