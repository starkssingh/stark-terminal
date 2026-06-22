from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from stark_terminal_core.domain.enums import DataLakeZone, Exchange, MarketSegment, Timeframe
from stark_terminal_core.domain.identifiers import InstrumentId
from stark_terminal_data_platform.exports.synthetic_ohlcv import (
    SyntheticOHLCVExportRequest,
    SyntheticOHLCVExportResult,
    build_synthetic_ohlcv_dataset_name,
    create_synthetic_ohlcv_export_request,
)


def _instrument_id() -> InstrumentId:
    return InstrumentId(symbol="RELIANCE", exchange=Exchange.NSE, segment=MarketSegment.NSE_EQUITY)


def test_valid_export_request_and_dataset_name_helper_are_stable() -> None:
    instrument_id = _instrument_id()
    dataset_name = build_synthetic_ohlcv_dataset_name(instrument_id, Timeframe.DAILY)

    request = create_synthetic_ohlcv_export_request(
        export_id="synthetic_ohlcv_export_reliance_daily",
        instrument_id=instrument_id,
        timeframe=Timeframe.DAILY,
        dataset_name=dataset_name,
        source_data_reference="synthetic-local-test-only",
        start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        end=datetime(2026, 1, 2, tzinfo=timezone.utc),
    )

    assert dataset_name == "synthetic_ohlcv_nse_reliance_nse_equity_daily_v1"
    assert request.synthetic is True
    assert request.zone == DataLakeZone.RESEARCH_ARTIFACTS
    assert request.created_at.tzinfo is not None


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("export_id", ""),
        ("dataset_name", ""),
        ("dataset_name", "../escape"),
        ("dataset_name", "unsafe/name"),
        ("version", ""),
        ("schema_version", ""),
    ],
)
def test_export_request_rejects_unsafe_text_fields(field: str, value: str) -> None:
    payload = {
        "export_id": "synthetic_ohlcv_export_reliance_daily",
        "instrument_id": _instrument_id(),
        "timeframe": Timeframe.DAILY,
        "dataset_name": "synthetic_ohlcv_reliance_daily",
        "source_data_reference": "synthetic-local-test-only",
    }
    payload[field] = value

    with pytest.raises(ValidationError):
        SyntheticOHLCVExportRequest(**payload)


def test_export_request_rejects_non_synthetic_or_unordered_ranges() -> None:
    with pytest.raises(ValidationError):
        SyntheticOHLCVExportRequest(
            export_id="synthetic_ohlcv_export_reliance_daily",
            instrument_id=_instrument_id(),
            timeframe=Timeframe.DAILY,
            dataset_name="synthetic_ohlcv_reliance_daily",
            synthetic=False,
            source_data_reference="synthetic-local-test-only",
        )
    with pytest.raises(ValidationError):
        SyntheticOHLCVExportRequest(
            export_id="synthetic_ohlcv_export_reliance_daily",
            instrument_id=_instrument_id(),
            timeframe=Timeframe.DAILY,
            dataset_name="synthetic_ohlcv_reliance_daily",
            source_data_reference="real-provider-live-data",
        )
    with pytest.raises(ValidationError):
        SyntheticOHLCVExportRequest(
            export_id="synthetic_ohlcv_export_reliance_daily",
            instrument_id=_instrument_id(),
            timeframe=Timeframe.DAILY,
            dataset_name="synthetic_ohlcv_reliance_daily",
            source_data_reference="synthetic-local-test-only",
            start=datetime(2026, 1, 2, tzinfo=timezone.utc),
            end=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )


def test_export_result_enforces_synthetic_boundary_and_sanitizes_errors() -> None:
    result = SyntheticOHLCVExportResult(
        export_id="synthetic_ohlcv_export_reliance_daily",
        exported=False,
        row_count=0,
        status="failed",
        error="postgresql://user:secret@localhost/db",
    )

    assert result.synthetic is True
    assert result.real_market_data is False
    assert result.error == "SyntheticOHLCVExportError"
    with pytest.raises(ValidationError):
        SyntheticOHLCVExportResult(
            export_id="synthetic_ohlcv_export_reliance_daily",
            exported=True,
            synthetic=False,
            row_count=1,
            status="exported",
        )
    with pytest.raises(ValidationError):
        SyntheticOHLCVExportResult(
            export_id="synthetic_ohlcv_export_reliance_daily",
            exported=True,
            real_market_data=True,
            row_count=1,
            status="exported",
        )
