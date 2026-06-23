from __future__ import annotations

import math
from datetime import datetime

from stark_terminal_analytics.diagnostics.contracts import (
    TimeSeriesDiagnosticKind,
    TimeSeriesDiagnosticsRequest,
    TimeSeriesDiagnosticsResult,
    TimestampGap,
    TimestampOrderStatus,
    create_time_series_diagnostics_result,
)
from stark_terminal_analytics.diagnostics.validation import validate_time_series_diagnostics_request


def determine_timestamp_order(timestamps: list[datetime]) -> TimestampOrderStatus:
    if len(timestamps) < 2:
        return TimestampOrderStatus.STRICTLY_INCREASING
    strictly_increasing = all(current < following for current, following in zip(timestamps, timestamps[1:]))
    if strictly_increasing:
        return TimestampOrderStatus.STRICTLY_INCREASING
    non_decreasing = all(current <= following for current, following in zip(timestamps, timestamps[1:]))
    if non_decreasing:
        return TimestampOrderStatus.NON_DECREASING
    return TimestampOrderStatus.NON_MONOTONIC


def find_duplicate_timestamps(timestamps: list[datetime]) -> list[datetime]:
    seen: set[datetime] = set()
    duplicates: list[datetime] = []
    duplicate_seen: set[datetime] = set()
    for timestamp in timestamps:
        if timestamp in seen and timestamp not in duplicate_seen:
            duplicates.append(timestamp)
            duplicate_seen.add(timestamp)
        seen.add(timestamp)
    return duplicates


def calculate_intervals_seconds(timestamps: list[datetime]) -> list[float]:
    return [
        (following - current).total_seconds()
        for current, following in zip(timestamps, timestamps[1:])
    ]


def find_timestamp_gaps(timestamps: list[datetime], expected_interval_seconds: int) -> list[TimestampGap]:
    if expected_interval_seconds <= 0:
        raise ValueError("expected_interval_seconds must be positive")
    gaps: list[TimestampGap] = []
    for current, following in zip(timestamps, timestamps[1:]):
        observed = (following - current).total_seconds()
        if observed > expected_interval_seconds:
            missing_count = max(math.floor(observed / expected_interval_seconds) - 1, 0)
            gaps.append(
                TimestampGap(
                    start_timestamp=current,
                    end_timestamp=following,
                    observed_interval_seconds=observed,
                    expected_interval_seconds=expected_interval_seconds,
                    missing_count_estimate=missing_count,
                )
            )
    return gaps


def summarize_intervals(timestamps: list[datetime]) -> dict[str, float | int | None]:
    intervals = calculate_intervals_seconds(timestamps)
    if not intervals:
        return {
            "interval_count": 0,
            "min_interval_seconds": None,
            "max_interval_seconds": None,
            "mean_interval_seconds": None,
        }
    return {
        "interval_count": len(intervals),
        "min_interval_seconds": min(intervals),
        "max_interval_seconds": max(intervals),
        "mean_interval_seconds": math.fsum(intervals) / len(intervals),
    }


def calculate_time_series_diagnostics(
    request: TimeSeriesDiagnosticsRequest,
) -> TimeSeriesDiagnosticsResult:
    validation = validate_time_series_diagnostics_request(request)
    series = request.timestamp_series
    timestamps = list(series.timestamps)
    order_status = determine_timestamp_order(timestamps)
    duplicates = find_duplicate_timestamps(timestamps)

    if validation.status != "ok":
        return create_time_series_diagnostics_result(
            result_id=f"{request.request_id}_time_series_diagnostics",
            request_id=request.request_id,
            source=series.source,
            observation_count=len(timestamps),
            status="failed",
            error=validation.error or "time-series diagnostics request failed validation",
            order_status=order_status,
            duplicate_count=len(duplicates),
            duplicate_timestamps=duplicates,
        )

    needs_interval_diagnostics = any(
        diagnostic in request.diagnostics
        for diagnostic in (
            TimeSeriesDiagnosticKind.GAPS,
            TimeSeriesDiagnosticKind.IRREGULAR_INTERVALS,
            TimeSeriesDiagnosticKind.SPACING_SUMMARY,
        )
    )
    if needs_interval_diagnostics and order_status == TimestampOrderStatus.NON_MONOTONIC:
        return create_time_series_diagnostics_result(
            result_id=f"{request.request_id}_time_series_diagnostics",
            request_id=request.request_id,
            source=series.source,
            observation_count=len(timestamps),
            status="failed",
            error="interval diagnostics require monotonic timestamps in provided order",
            order_status=order_status,
            duplicate_count=len(duplicates),
            duplicate_timestamps=duplicates,
        )

    summary = summarize_intervals(timestamps) if needs_interval_diagnostics else {}
    gaps: list[TimestampGap] = []
    if TimeSeriesDiagnosticKind.GAPS in request.diagnostics and request.expected_interval_seconds is not None:
        gaps = find_timestamp_gaps(timestamps, request.expected_interval_seconds)

    return create_time_series_diagnostics_result(
        result_id=f"{request.request_id}_time_series_diagnostics",
        request_id=request.request_id,
        source=series.source,
        observation_count=len(timestamps),
        status="ok",
        order_status=order_status if TimeSeriesDiagnosticKind.MONOTONICITY in request.diagnostics else None,
        duplicate_count=len(duplicates) if TimeSeriesDiagnosticKind.DUPLICATES in request.diagnostics else None,
        duplicate_timestamps=duplicates if TimeSeriesDiagnosticKind.DUPLICATES in request.diagnostics else [],
        gap_count=len(gaps) if TimeSeriesDiagnosticKind.GAPS in request.diagnostics else None,
        gaps=gaps if TimeSeriesDiagnosticKind.GAPS in request.diagnostics else [],
        interval_count=summary.get("interval_count") if needs_interval_diagnostics else None,
        min_interval_seconds=summary.get("min_interval_seconds") if needs_interval_diagnostics else None,
        max_interval_seconds=summary.get("max_interval_seconds") if needs_interval_diagnostics else None,
        mean_interval_seconds=summary.get("mean_interval_seconds") if needs_interval_diagnostics else None,
    )

