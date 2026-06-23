from __future__ import annotations

from stark_terminal_analytics.diagnostics.contracts import (
    TimeSeriesDiagnosticKind,
    TimeSeriesDiagnosticsRequest,
    TimeSeriesDiagnosticsResult,
    TimestampSeriesContract,
)
from stark_terminal_analytics.numerical.contracts import (
    NumericalComputationKind,
    NumericalComputationResult,
    create_safe_result,
)
from stark_terminal_analytics.numerical.validation import validate_no_signal_fields, validate_source_reference


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


def _timestamps_are_timezone_aware(series: TimestampSeriesContract) -> bool:
    return all(
        timestamp.tzinfo is not None and timestamp.tzinfo.utcoffset(timestamp) is not None
        for timestamp in series.timestamps
    )


def validate_timestamp_series(
    series: TimestampSeriesContract,
    max_observations: int | None = None,
) -> NumericalComputationResult:
    source_check = validate_source_reference(series.source)
    observation_count = len(series.timestamps)
    max_observations_ok = max_observations is None or observation_count <= max_observations
    timezone_ok = (not series.require_timezone_aware) or _timestamps_are_timezone_aware(series)
    passed = (
        observation_count > 0
        and source_check.status == "ok"
        and not series.source.real_market_data
        and max_observations_ok
        and timezone_ok
        and series.descriptive_only
    )
    return _validation_result(
        result_id=f"{series.series_id}_timestamp_series_validation",
        request_id=f"{series.series_id}_timestamp_series_validation_request",
        passed=passed,
        metrics={
            "observation_count": observation_count,
            "source_valid": source_check.status == "ok",
            "real_market_data": series.source.real_market_data,
            "timezone_aware": timezone_ok,
            "max_observations_ok": max_observations_ok,
        },
        source=series.source,
        error=None if passed else "timestamp series failed validation",
    )


def validate_time_series_diagnostics_request(
    request: TimeSeriesDiagnosticsRequest,
    max_observations: int | None = None,
) -> NumericalComputationResult:
    series_check = validate_timestamp_series(request.timestamp_series, max_observations=max_observations)
    no_signal_fields = validate_no_signal_fields(request)
    diagnostics_known = bool(request.diagnostics) and TimeSeriesDiagnosticKind.UNKNOWN not in request.diagnostics
    gap_interval_ok = (
        TimeSeriesDiagnosticKind.GAPS not in request.diagnostics
        or request.expected_interval_seconds is not None
    )
    expected_interval_ok = (
        request.expected_interval_seconds is None or request.expected_interval_seconds > 0
    )
    passed = (
        series_check.status == "ok"
        and no_signal_fields
        and diagnostics_known
        and gap_interval_ok
        and expected_interval_ok
        and request.require_source_reference
    )
    return _validation_result(
        result_id=f"{request.request_id}_time_series_diagnostics_request_validation",
        request_id=request.request_id,
        passed=passed,
        metrics={
            "observation_count": len(request.timestamp_series.timestamps),
            "diagnostic_count": len(request.diagnostics),
            "no_signal_fields": no_signal_fields,
            "diagnostics_known": diagnostics_known,
            "gap_interval_supplied": gap_interval_ok,
            "expected_interval_valid": expected_interval_ok,
        },
        source=request.timestamp_series.source,
        error=None if passed else "time-series diagnostics request failed validation",
    )


def validate_time_series_diagnostics_result(
    result: TimeSeriesDiagnosticsResult,
) -> NumericalComputationResult:
    source_check = validate_source_reference(result.source)
    no_signal_fields = validate_no_signal_fields(result)
    counts_valid = (
        result.observation_count >= 0
        and (result.duplicate_count is None or result.duplicate_count >= 0)
        and (result.gap_count is None or result.gap_count >= 0)
        and (result.interval_count is None or result.interval_count >= 0)
    )
    interval_values = [
        result.min_interval_seconds,
        result.max_interval_seconds,
        result.mean_interval_seconds,
    ]
    intervals_valid = all(value is None or value >= 0 for value in interval_values)
    passed = (
        source_check.status == "ok"
        and no_signal_fields
        and counts_valid
        and intervals_valid
        and result.descriptive_only
        and not result.source.real_market_data
    )
    return _validation_result(
        result_id=f"{result.result_id}_time_series_diagnostics_result_validation",
        request_id=result.request_id,
        passed=passed,
        metrics={
            "observation_count": result.observation_count,
            "counts_valid": counts_valid,
            "intervals_valid": intervals_valid,
            "no_signal_fields": no_signal_fields,
        },
        source=result.source,
        error=None if passed else "time-series diagnostics result failed validation",
    )

