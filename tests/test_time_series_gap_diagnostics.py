from datetime import datetime, timedelta, timezone

from stark_terminal_analytics.diagnostics.calculations import calculate_time_series_diagnostics, find_timestamp_gaps
from stark_terminal_analytics.diagnostics.contracts import (
    TimeSeriesDiagnosticKind,
    create_time_series_diagnostics_request,
    create_timestamp_series,
)
from stark_terminal_analytics.numerical.contracts import create_synthetic_source_reference


def _source():
    return create_synthetic_source_reference(source_id="gap-diagnostics-source")


def test_no_gap_when_interval_equals_expected_interval() -> None:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    gaps = find_timestamp_gaps([start, start + timedelta(minutes=1)], expected_interval_seconds=60)

    assert gaps == []


def test_gap_when_interval_exceeds_expected_interval() -> None:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    gaps = find_timestamp_gaps([start, start + timedelta(minutes=3)], expected_interval_seconds=60)

    assert len(gaps) == 1
    assert gaps[0].missing_count_estimate == 2


def test_multiple_gaps_detected() -> None:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    timestamps = [
        start,
        start + timedelta(minutes=3),
        start + timedelta(minutes=4),
        start + timedelta(minutes=7),
    ]
    gaps = find_timestamp_gaps(timestamps, expected_interval_seconds=60)

    assert [gap.missing_count_estimate for gap in gaps] == [2, 2]


def test_gap_diagnostics_request_requires_expected_interval() -> None:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    series = create_timestamp_series(
        "gap-series",
        "Gap timestamps",
        [start, start + timedelta(minutes=3)],
        _source(),
    )
    request = create_time_series_diagnostics_request(
        request_id="gap-request",
        timestamp_series=series,
        diagnostics=[TimeSeriesDiagnosticKind.GAPS],
    )

    result = calculate_time_series_diagnostics(request)

    assert result.status == "failed"
    assert result.gap_count is None


def test_duplicate_timestamps_do_not_create_gap() -> None:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    gaps = find_timestamp_gaps([start, start, start + timedelta(minutes=1)], expected_interval_seconds=60)

    assert gaps == []

