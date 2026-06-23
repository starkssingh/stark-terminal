from datetime import datetime, timedelta, timezone

from stark_terminal_analytics.diagnostics.calculations import (
    calculate_intervals_seconds,
    calculate_time_series_diagnostics,
    determine_timestamp_order,
    find_duplicate_timestamps,
    find_timestamp_gaps,
    summarize_intervals,
)
from stark_terminal_analytics.diagnostics.contracts import (
    TimeSeriesDiagnosticKind,
    TimestampOrderStatus,
    create_time_series_diagnostics_request,
    create_timestamp_series,
)
from stark_terminal_analytics.numerical.contracts import create_synthetic_source_reference


def _source():
    return create_synthetic_source_reference(source_id="diagnostics-calculation-source")


def _timestamps() -> list[datetime]:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    return [start, start + timedelta(minutes=1), start + timedelta(minutes=4)]


def test_determine_timestamp_order_statuses() -> None:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)

    assert determine_timestamp_order([start, start + timedelta(seconds=1)]) == TimestampOrderStatus.STRICTLY_INCREASING
    assert determine_timestamp_order([start, start]) == TimestampOrderStatus.NON_DECREASING
    assert determine_timestamp_order([start + timedelta(seconds=1), start]) == TimestampOrderStatus.NON_MONOTONIC


def test_find_duplicate_timestamps_returns_unique_duplicates() -> None:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    duplicates = find_duplicate_timestamps([start, start, start + timedelta(minutes=1), start])

    assert duplicates == [start]


def test_calculate_intervals_seconds_is_deterministic() -> None:
    assert calculate_intervals_seconds(_timestamps()) == [60.0, 180.0]


def test_find_timestamp_gaps_is_deterministic() -> None:
    gaps = find_timestamp_gaps(_timestamps(), expected_interval_seconds=60)

    assert len(gaps) == 1
    assert gaps[0].observed_interval_seconds == 180.0
    assert gaps[0].missing_count_estimate == 2


def test_summarize_intervals_is_deterministic() -> None:
    summary = summarize_intervals(_timestamps())

    assert summary == {
        "interval_count": 2,
        "min_interval_seconds": 60.0,
        "max_interval_seconds": 180.0,
        "mean_interval_seconds": 120.0,
    }


def test_calculate_time_series_diagnostics_success_result_is_descriptive() -> None:
    series = create_timestamp_series("series-calc", "Calculation timestamps", _timestamps(), _source())
    request = create_time_series_diagnostics_request(
        request_id="request-calc",
        timestamp_series=series,
        diagnostics=[
            TimeSeriesDiagnosticKind.MONOTONICITY,
            TimeSeriesDiagnosticKind.DUPLICATES,
            TimeSeriesDiagnosticKind.GAPS,
            TimeSeriesDiagnosticKind.IRREGULAR_INTERVALS,
            TimeSeriesDiagnosticKind.SPACING_SUMMARY,
        ],
        expected_interval_seconds=60,
    )

    result = calculate_time_series_diagnostics(request)

    assert result.status == "ok"
    assert result.order_status == TimestampOrderStatus.STRICTLY_INCREASING
    assert result.duplicate_count == 0
    assert result.gap_count == 1
    assert result.interval_count == 2
    assert result.descriptive_only is True
    assert result.trade_signal is False
    assert result.recommendation is False
    assert result.decision_object_generated is False
    assert "stationarity" not in result.model_dump()
    assert "regime" not in result.model_dump()


def test_non_monotonic_interval_diagnostics_fail_safely() -> None:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    series = create_timestamp_series(
        "series-non-monotonic",
        "Non-monotonic timestamps",
        [start + timedelta(minutes=1), start],
        _source(),
    )
    request = create_time_series_diagnostics_request(
        request_id="request-non-monotonic",
        timestamp_series=series,
        diagnostics=[TimeSeriesDiagnosticKind.GAPS, TimeSeriesDiagnosticKind.SPACING_SUMMARY],
        expected_interval_seconds=60,
    )

    result = calculate_time_series_diagnostics(request)

    assert result.status == "failed"
    assert result.order_status == TimestampOrderStatus.NON_MONOTONIC
    assert result.trade_signal is False
    assert result.recommendation is False
    assert result.decision_object_generated is False

