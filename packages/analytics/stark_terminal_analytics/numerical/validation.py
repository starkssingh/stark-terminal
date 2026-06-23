from __future__ import annotations

import math
from typing import Any

from stark_terminal_analytics.numerical.contracts import (
    NumericalComputationKind,
    NumericalComputationResult,
    NumericalSourceReference,
    NumericalTableContract,
    NumericalVectorContract,
    create_safe_result,
    create_synthetic_source_reference,
)


def _validation_source() -> NumericalSourceReference:
    return create_synthetic_source_reference(
        source_id="numerical-validation",
        source_type="validation_contract",
        source_data_reference="synthetic-local-test-only:numerical-validation",
        provider_name=None,
    )


def _validation_result(
    result_id: str,
    request_id: str,
    computation_kind: NumericalComputationKind,
    passed: bool,
    metrics: dict[str, float | int | str | bool | None],
    error: str | None = None,
    source: NumericalSourceReference | None = None,
) -> NumericalComputationResult:
    return create_safe_result(
        result_id=result_id,
        request_id=request_id,
        computation_kind=computation_kind,
        metrics=metrics if passed else {},
        source=source or _validation_source(),
        status="ok" if passed else "failed",
        error=error,
    )


def validate_finite_values(values: list[float]) -> NumericalComputationResult:
    finite = bool(values) and all(math.isfinite(value) for value in values)
    return _validation_result(
        result_id="finite_values_validation",
        request_id="finite_values_validation_request",
        computation_kind=NumericalComputationKind.FINITE_CHECK,
        passed=finite,
        metrics={"count": len(values), "finite": finite},
        error=None if finite else "values must be non-empty and finite",
    )


def validate_vector_shape(
    vector: NumericalVectorContract,
    max_length: int | None = None,
) -> NumericalComputationResult:
    count = len(vector.values)
    too_long = max_length is not None and count > max_length
    passed = count > 0 and not too_long
    return _validation_result(
        result_id=f"{vector.vector_id}_shape_validation",
        request_id=f"{vector.vector_id}_shape_validation_request",
        computation_kind=NumericalComputationKind.SHAPE_CHECK,
        passed=passed,
        metrics={"count": count, "max_length": max_length, "within_limit": not too_long},
        error=None if passed else "vector shape is invalid or exceeds max length",
        source=vector.source,
    )


def validate_table_contract(table: NumericalTableContract) -> NumericalComputationResult:
    passed = bool(table.columns) and table.row_count >= 0 and table.descriptive_only
    return _validation_result(
        result_id=f"{table.table_id}_table_validation",
        request_id=f"{table.table_id}_table_validation_request",
        computation_kind=NumericalComputationKind.VALIDATION,
        passed=passed,
        metrics={
            "row_count": table.row_count,
            "column_count": len(table.columns),
            "descriptive_only": table.descriptive_only,
        },
        error=None if passed else "table contract is invalid",
        source=table.source,
    )


def validate_source_reference(source: NumericalSourceReference) -> NumericalComputationResult:
    passed = bool(source.source_id and source.source_type and source.source_data_reference) and not source.real_market_data
    return _validation_result(
        result_id=f"{source.source_id}_source_validation",
        request_id=f"{source.source_id}_source_validation_request",
        computation_kind=NumericalComputationKind.SOURCE_CHECK,
        passed=passed,
        metrics={
            "synthetic": source.synthetic,
            "real_market_data": source.real_market_data,
            "has_source_reference": bool(source.source_data_reference),
        },
        error=None if passed else "source reference is missing or claims real market data",
        source=source if passed else None,
    )


def validate_no_signal_fields(result_or_contract: Any) -> bool:
    unsafe_flags = [
        "trade_signal",
        "recommendation",
        "decision_object_generated",
        "execution_ready",
        "allow_trade_signal",
        "allow_recommendation",
        "allow_decision_object",
    ]
    for field in unsafe_flags:
        if getattr(result_or_contract, field, False):
            return False
    if getattr(result_or_contract, "descriptive_only", True) is False:
        return False
    return True
