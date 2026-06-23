from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from stark_terminal_analytics.diagnostics.contracts import (
    TimeSeriesDiagnosticKind,
    TimeSeriesDiagnosticsRequest,
    TimeSeriesDiagnosticsResult,
    TimeSeriesDiagnosticSafetyLabel,
    TimestampGap,
    TimestampOrderStatus,
    TimestampSeriesContract,
    create_time_series_diagnostics_request,
    create_time_series_diagnostics_result,
    create_timestamp_series,
)
from stark_terminal_analytics.numerical.contracts import (
    NumericalSourceReference,
    create_synthetic_source_reference,
)


def _timestamps() -> list[datetime]:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    return [start, start + timedelta(minutes=1), start + timedelta(minutes=2)]


def _source():
    return create_synthetic_source_reference(source_id="diagnostics-source")


def test_valid_timestamp_series_contract() -> None:
    series = create_timestamp_series("series-1", "Synthetic timestamps", _timestamps(), _source())

    assert series.series_id == "series-1"
    assert series.descriptive_only is True
    assert series.safety_label == TimeSeriesDiagnosticSafetyLabel.DATA_QUALITY_ONLY
    assert all(timestamp.tzinfo is not None for timestamp in series.timestamps)


def test_timestamp_series_rejects_empty_timestamps() -> None:
    with pytest.raises(ValidationError):
        TimestampSeriesContract(series_id="series-1", name="Empty", timestamps=[], source=_source())


def test_timestamp_series_rejects_naive_timestamps_by_default() -> None:
    with pytest.raises(ValidationError):
        TimestampSeriesContract(
            series_id="series-1",
            name="Naive",
            timestamps=[datetime(2026, 1, 1)],
            source=_source(),
        )


def test_timestamp_series_rejects_real_market_data_source() -> None:
    real_source = NumericalSourceReference.model_construct(
        source_id="real-source",
        source_type="provider",
        source_data_reference="real-market",
        synthetic=False,
        real_market_data=True,
        schema_version="v1",
        created_at=datetime.now(timezone.utc),
    )

    with pytest.raises(ValidationError):
        TimestampSeriesContract(
            series_id="series-1",
            name="Real source",
            timestamps=_timestamps(),
            source=real_source,
        )


def test_valid_time_series_diagnostics_request() -> None:
    series = create_timestamp_series("series-1", "Synthetic timestamps", _timestamps(), _source())
    request = create_time_series_diagnostics_request(
        request_id="request-1",
        timestamp_series=series,
        diagnostics=[TimeSeriesDiagnosticKind.MONOTONICITY, TimeSeriesDiagnosticKind.GAPS],
        expected_interval_seconds=60,
    )

    assert request.request_id == "request-1"
    assert request.allow_real_data is False
    assert request.allow_trade_signal is False
    assert request.allow_recommendation is False
    assert request.allow_decision_object is False


@pytest.mark.parametrize(
    "override",
    [
        {"allow_real_data": True},
        {"allow_trade_signal": True},
        {"allow_recommendation": True},
        {"allow_decision_object": True},
        {"require_source_reference": False},
        {"expected_interval_seconds": 0},
        {"diagnostics": [TimeSeriesDiagnosticKind.UNKNOWN]},
    ],
)
def test_time_series_diagnostics_request_rejects_unsafe_fields(override: dict[str, object]) -> None:
    series = create_timestamp_series("series-1", "Synthetic timestamps", _timestamps(), _source())
    payload = {
        "request_id": "request-1",
        "timestamp_series": series,
        "diagnostics": [TimeSeriesDiagnosticKind.MONOTONICITY],
    }
    payload.update(override)

    with pytest.raises(ValidationError):
        TimeSeriesDiagnosticsRequest(**payload)


def test_timestamp_gap_contract_validates_gap_shape() -> None:
    start, end = _timestamps()[0], _timestamps()[2]
    gap = TimestampGap(
        start_timestamp=start,
        end_timestamp=end,
        observed_interval_seconds=120,
        expected_interval_seconds=60,
        missing_count_estimate=1,
    )

    assert gap.missing_count_estimate == 1


def test_time_series_diagnostics_result_preserves_source_reference() -> None:
    source = _source()
    result = create_time_series_diagnostics_result(
        result_id="result-1",
        request_id="request-1",
        source=source,
        observation_count=3,
        order_status=TimestampOrderStatus.STRICTLY_INCREASING,
        duplicate_count=0,
        gap_count=0,
        status="ok",
    )

    assert result.source.source_id == source.source_id
    assert result.descriptive_only is True
    assert result.trade_signal is False
    assert result.recommendation is False
    assert result.decision_object_generated is False


@pytest.mark.parametrize(
    "override",
    [
        {"trade_signal": True},
        {"recommendation": True},
        {"decision_object_generated": True},
        {"descriptive_only": False},
    ],
)
def test_time_series_diagnostics_result_rejects_unsafe_flags(override: dict[str, object]) -> None:
    payload = {
        "result_id": "result-1",
        "request_id": "request-1",
        "source": _source(),
        "observation_count": 3,
        "status": "ok",
    }
    payload.update(override)

    with pytest.raises(ValidationError):
        TimeSeriesDiagnosticsResult(**payload)

