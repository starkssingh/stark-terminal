"""Descriptive returns analytics v0 for Stark Terminal."""

from stark_terminal_analytics.returns.calculations import calculate_log_returns, calculate_returns, calculate_simple_returns
from stark_terminal_analytics.returns.contracts import (
    ReturnCalculationRequest,
    ReturnMethod,
    ReturnSeriesResult,
    ReturnSeriesSafetyLabel,
)

__all__ = [
    "ReturnCalculationRequest",
    "ReturnMethod",
    "ReturnSeriesResult",
    "ReturnSeriesSafetyLabel",
    "calculate_log_returns",
    "calculate_returns",
    "calculate_simple_returns",
]
