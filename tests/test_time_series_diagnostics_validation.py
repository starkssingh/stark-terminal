from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from stark_terminal_analytics.diagnostics.contracts import (
    TimeSeriesDiagnosticKind,
    TimeSeriesDiagnosticsRequest,
    create_time_series_diagnostics_request,
    create_timestamp_series,
)
from stark_terminal_analytics.diagnostics.validation import (
    validate_time_series_diagnostics_request,
    validate_time_series_diagnostics_result,
    validate_timestamp_series,
)
from stark_terminal_analytics.numerical.contracts import (
    NumericalSourceReference,
    create_synthetic_source_reference,
)


def _source():
    return create_synthetic_source_reference(source_id="diagnostics-validation-source")


def _timestamps(count: int = 3) -> list[datetime]:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    return [start + timedelta(minutes=index) for index in range(count)]


def _series(count: int = 3):
    return create_timestamp_series("series-validation", "Validation timestamps", _timestamps(count), _source())


def test_timestamp_series_validation_passes() -> None:
    result = validate_timestamp_series(_series())

    assert result.status == "ok"
    assert result.metrics["observation_count"] == 3


def test_timestamp_series_validation_enforces_max_observations() -> None:
    result = validate_timestamp_series(_series(3), max_observations=2)

    assert result.status == "failed"


def test_timestamp_series_validation_rejects_real_market_data_source() -> None:
    source = NumericalSourceReference.model_construct(
        source_id="real-source",
        source_type="provider",
        source_data_reference="real-market",
        synthetic=False,
        real_market_data=True,
        schema_version="v1",
        created_at=datetime.now(timezone.utc),
    )
    with pytest.raises(ValidationError):
        create_timestamp_series("series-real", "Real timestamps", _timestamps(), source)


def test_timestamp_series_validation_enforces_timezone_awareness() -> None:
    with pytest.raises(ValidationError):
        create_timestamp_series("series-naive", "Naive timestamps", [datetime(2026, 1, 1)], _source())


def test_diagnostics_request_requires_expected_interval_for_gaps() -> None:
    request = create_time_series_diagnostics_request(
        request_id="request-gap-missing-interval",
        timestamp_series=_series(),
        diagnostics=[TimeSeriesDiagnosticKind.GAPS],
    )

    result = validate_time_series_diagnostics_request(request)

    assert result.status == "failed"


def test_diagnostics_request_unknown_diagnostic_is_rejected() -> None:
    with pytest.raises(ValidationError):
        TimeSeriesDiagnosticsRequest(
            request_id="request-unknown",
            timestamp_series=_series(),
            diagnostics=[TimeSeriesDiagnosticKind.UNKNOWN],
        )


def test_diagnostics_request_unsafe_flags_fail_validation_when_bypassed() -> None:
    request = create_time_series_diagnostics_request(
        request_id="request-unsafe",
        timestamp_series=_series(),
        diagnostics=[TimeSeriesDiagnosticKind.MONOTONICITY],
    ).model_copy(update={"allow_trade_signal": True})

    result = validate_time_series_diagnostics_request(request)

    assert result.status == "failed"


def test_diagnostics_result_validation_rejects_unsafe_flags_when_bypassed() -> None:
    from stark_terminal_analytics.diagnostics.contracts import create_time_series_diagnostics_result

    result = create_time_series_diagnostics_result(
        result_id="result-unsafe",
        request_id="request-unsafe",
        source=_source(),
        observation_count=3,
        status="ok",
    ).model_copy(update={"decision_object_generated": True})

    validation = validate_time_series_diagnostics_result(result)

    assert validation.status == "failed"

