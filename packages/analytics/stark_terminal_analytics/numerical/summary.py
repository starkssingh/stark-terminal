from __future__ import annotations

import math

from stark_terminal_analytics.numerical.contracts import (
    NumericalComputationKind,
    NumericalComputationRequest,
    NumericalComputationResult,
    NumericalVectorContract,
    create_safe_result,
    create_summary_request,
)


def _require_non_empty_finite(values: list[float]) -> list[float]:
    if not values:
        raise ValueError("values cannot be empty")
    if not all(math.isfinite(value) for value in values):
        raise ValueError("values must be finite")
    return list(values)


def numeric_count(values: list[float]) -> int:
    _require_non_empty_finite(values)
    return len(values)


def numeric_min(values: list[float]) -> float:
    return min(_require_non_empty_finite(values))


def numeric_max(values: list[float]) -> float:
    return max(_require_non_empty_finite(values))


def numeric_mean(values: list[float]) -> float:
    checked = _require_non_empty_finite(values)
    return math.fsum(checked) / len(checked)


def safe_numeric_summary(
    vector: NumericalVectorContract,
    request: NumericalComputationRequest | None = None,
) -> NumericalComputationResult:
    resolved_request = request or create_summary_request(
        request_id=f"{vector.vector_id}_summary_request",
        input_ids=[vector.vector_id],
        source=vector.source,
    )
    try:
        if resolved_request.require_finite_values:
            _require_non_empty_finite(vector.values)
        metrics = {
            "count": numeric_count(vector.values),
            "min": numeric_min(vector.values),
            "max": numeric_max(vector.values),
            "mean": numeric_mean(vector.values),
        }
        return create_safe_result(
            result_id=f"{vector.vector_id}_summary",
            request_id=resolved_request.request_id,
            computation_kind=NumericalComputationKind.SUMMARY,
            metrics=metrics,
            source=vector.source,
            status="ok",
        )
    except ValueError as exc:
        return create_safe_result(
            result_id=f"{vector.vector_id}_summary",
            request_id=resolved_request.request_id,
            computation_kind=NumericalComputationKind.SUMMARY,
            metrics={},
            source=vector.source,
            status="failed",
            error=str(exc),
        )
