"""Descriptive drawdown analytics v0."""

from stark_terminal_analytics.drawdown.calculations import (
    calculate_drawdown,
    calculate_drawdown_series,
    calculate_longest_drawdown_duration,
    calculate_max_drawdown,
)
from stark_terminal_analytics.drawdown.contracts import (
    DrawdownCalculationRequest,
    DrawdownMetric,
    DrawdownResult,
    create_drawdown_request,
    create_drawdown_result,
)
from stark_terminal_analytics.drawdown.validation import (
    validate_drawdown_request,
    validate_drawdown_result,
    validate_value_vector_for_drawdown,
)

__all__ = [
    "DrawdownCalculationRequest",
    "DrawdownMetric",
    "DrawdownResult",
    "calculate_drawdown",
    "calculate_drawdown_series",
    "calculate_longest_drawdown_duration",
    "calculate_max_drawdown",
    "create_drawdown_request",
    "create_drawdown_result",
    "validate_drawdown_request",
    "validate_drawdown_result",
    "validate_value_vector_for_drawdown",
]
