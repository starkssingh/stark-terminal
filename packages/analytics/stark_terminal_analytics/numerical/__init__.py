"""Numerical analytics core contracts for Stark Terminal.

Prompt 27 allows only descriptive contract validation and tiny stdlib summaries.
It implements no returns, volatility, drawdown, correlation, signals,
recommendations, DecisionObject generation, backtests, or execution APIs.
"""

from stark_terminal_analytics.numerical.contracts import (
    NumericalComputationKind,
    NumericalComputationRequest,
    NumericalComputationResult,
    NumericalDataKind,
    NumericalSafetyLabel,
    NumericalSourceReference,
    NumericalTableColumn,
    NumericalTableContract,
    NumericalValueType,
    NumericalVectorContract,
)

__all__ = [
    "NumericalComputationKind",
    "NumericalComputationRequest",
    "NumericalComputationResult",
    "NumericalDataKind",
    "NumericalSafetyLabel",
    "NumericalSourceReference",
    "NumericalTableColumn",
    "NumericalTableContract",
    "NumericalValueType",
    "NumericalVectorContract",
]
