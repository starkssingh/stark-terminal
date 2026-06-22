from datetime import datetime, timedelta, timezone
from pathlib import Path

import polars as pl

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import DatasetFormat, MarketDataRequestKind, Timeframe
from stark_terminal_core.domain.identifiers import InstrumentId
from stark_terminal_core.domain.market_data_contracts import create_market_data_request
from stark_terminal_data_platform.quality.builtins import MarketDataResponseValidator
from stark_terminal_data_platform.quality.enums import ValidationStatus
from stark_terminal_data_platform.providers.local_file import (
    LocalFileProviderAdapter,
    LocalFileSource,
)


def _settings(root: Path, **overrides) -> Settings:
    return Settings(local_file_provider_allowed_root=str(root), **overrides)


def _source(path: Path, file_format: DatasetFormat = DatasetFormat.CSV) -> LocalFileSource:
    return LocalFileSource(source_id="source", path=str(path), file_format=file_format)


def _request() -> object:
    start = datetime(2024, 1, 1, tzinfo=timezone.utc)
    return create_market_data_request(
        MarketDataRequestKind.HISTORICAL_BARS,
        instrument_id=InstrumentId(symbol="ABC", exchange="NSE", segment="NSE_EQUITY"),
        timeframe=Timeframe.DAILY,
        start=start,
        end=start + timedelta(days=2),
    )


def test_valid_local_file_bars_pass_data_quality_validation(tmp_path: Path) -> None:
    path = tmp_path / "ohlcv.csv"
    pl.DataFrame(
        [
            {
                "symbol": "ABC",
                "exchange": "NSE",
                "segment": "NSE_EQUITY",
                "timeframe": "DAILY",
                "timestamp": "2024-01-01T00:00:00+00:00",
                "open": 100.0,
                "high": 102.0,
                "low": 99.0,
                "close": 101.0,
                "volume": 1000.0,
                "open_interest": 10.0,
            }
        ]
    ).write_csv(path)
    settings = _settings(tmp_path)
    response = LocalFileProviderAdapter(settings=settings, source=_source(path)).get_historical_bars(_request())

    report = MarketDataResponseValidator(settings=settings).validate(response)

    assert response.errors == []
    assert report.status == ValidationStatus.PASS


def test_invalid_ohlc_rows_return_rejected_response(tmp_path: Path) -> None:
    path = tmp_path / "bad_ohlc.csv"
    pl.DataFrame(
        [
            {
                "symbol": "ABC",
                "exchange": "NSE",
                "segment": "NSE_EQUITY",
                "timeframe": "DAILY",
                "timestamp": "2024-01-01T00:00:00+00:00",
                "open": 100.0,
                "high": 98.0,
                "low": 99.0,
                "close": 101.0,
                "volume": 1000.0,
            }
        ]
    ).write_csv(path)

    response = LocalFileProviderAdapter(settings=_settings(tmp_path), source=_source(path)).get_historical_bars(_request())

    assert response.errors
    assert response.bars == []
    assert "validation" in response.errors[0].lower() or "high" in response.errors[0].lower()


def test_invalid_instrument_rows_return_sanitized_errors(tmp_path: Path) -> None:
    path = tmp_path / "bad_instruments.csv"
    pl.DataFrame([{"symbol": "ABC", "exchange": "NSE"}]).write_csv(path)
    provider = LocalFileProviderAdapter(settings=_settings(tmp_path), source=_source(path))
    request = create_market_data_request(MarketDataRequestKind.INSTRUMENT_MASTER)

    response = provider.get_instrument_master(request)

    assert response.errors
    assert response.instruments == []
    assert "secret" not in str(response.model_dump()).lower()


def test_invalid_request_kind_returns_safe_error(tmp_path: Path) -> None:
    path = tmp_path / "ohlcv.csv"
    pl.DataFrame(
        [
            {
                "symbol": "ABC",
                "exchange": "NSE",
                "segment": "NSE_EQUITY",
                "timeframe": "DAILY",
                "timestamp": "2024-01-01T00:00:00+00:00",
                "open": 100.0,
                "high": 102.0,
                "low": 99.0,
                "close": 101.0,
            }
        ]
    ).write_csv(path)
    provider = LocalFileProviderAdapter(settings=_settings(tmp_path), source=_source(path))
    request = create_market_data_request(MarketDataRequestKind.HEALTH_CHECK)

    response = provider.get_historical_bars(request)

    assert response.errors
    assert "HISTORICAL_BARS" in response.errors[0]
