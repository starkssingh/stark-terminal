from datetime import datetime, timedelta, timezone
from pathlib import Path

import polars as pl

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import (
    DataProviderType,
    DatasetFormat,
    MarketDataRequestKind,
    ProviderCapability,
    Timeframe,
)
from stark_terminal_core.domain.identifiers import InstrumentId
from stark_terminal_core.domain.market_data_contracts import create_market_data_request
from stark_terminal_core.serialization.json import to_jsonable
from stark_terminal_data_platform.providers.local_file import (
    LOCAL_FILE_SOURCE_REFERENCE,
    LocalFileProviderAdapter,
    LocalFileSource,
)


def _settings(root: Path, **overrides) -> Settings:
    return Settings(local_file_provider_allowed_root=str(root), **overrides)


def _instrument_id() -> InstrumentId:
    return InstrumentId(symbol="ABC", exchange="NSE", segment="NSE_EQUITY")


def _instrument_rows() -> list[dict[str, object]]:
    return [
        {
            "symbol": "ABC",
            "exchange": "NSE",
            "segment": "NSE_EQUITY",
            "display_name": "ABC Local File Test",
            "asset_class": "EQUITY",
            "status": "ACTIVE",
            "lot_size": 1,
            "tick_size": 0.05,
        }
    ]


def _ohlcv_rows() -> list[dict[str, object]]:
    start = datetime(2024, 1, 1, tzinfo=timezone.utc)
    return [
        {
            "symbol": "ABC",
            "exchange": "NSE",
            "segment": "NSE_EQUITY",
            "timeframe": "DAILY",
            "timestamp": (start + timedelta(days=index)).isoformat(),
            "open": 100.0 + index,
            "high": 102.0 + index,
            "low": 99.0 + index,
            "close": 101.0 + index,
            "volume": 1000.0 + index,
            "open_interest": 10.0 + index,
        }
        for index in range(2)
    ]


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    pl.DataFrame(rows).write_csv(path)


def _write_parquet(path: Path, rows: list[dict[str, object]]) -> None:
    pl.DataFrame(rows).write_parquet(path)


def _source(path: Path, file_format: DatasetFormat) -> LocalFileSource:
    return LocalFileSource(
        source_id=f"source_{path.suffix[1:]}",
        path=str(path),
        file_format=file_format,
    )


def _historical_request() -> object:
    start = datetime(2024, 1, 1, tzinfo=timezone.utc)
    return create_market_data_request(
        MarketDataRequestKind.HISTORICAL_BARS,
        instrument_id=_instrument_id(),
        timeframe=Timeframe.DAILY,
        start=start,
        end=start + timedelta(days=2),
    )


def test_local_file_provider_identity_capabilities_and_health(tmp_path: Path) -> None:
    provider = LocalFileProviderAdapter(settings=_settings(tmp_path))

    report = provider.capabilities()
    health = provider.health_check()

    assert provider.provider_id.name == "local_file"
    assert provider.provider_id.provider_type == DataProviderType.MANUAL
    assert provider.provider_id.version == "v0"
    assert ProviderCapability.INSTRUMENT_MASTER in report.capabilities
    assert ProviderCapability.HISTORICAL_BARS in report.capabilities
    assert ProviderCapability.HEALTH_CHECK in report.capabilities
    assert ProviderCapability.LATEST_BAR not in report.capabilities
    assert report.network_calls_allowed is False
    assert health.synthetic_or_local_only is True
    assert health.real_data_claims_allowed is False
    assert health.network_allowed is False
    assert health.credentials_required is False
    assert health.status == "HEALTHY"


def test_missing_source_returns_safe_errors(tmp_path: Path) -> None:
    provider = LocalFileProviderAdapter(settings=_settings(tmp_path))
    request = create_market_data_request(MarketDataRequestKind.INSTRUMENT_MASTER)

    response = provider.get_instrument_master(request)

    assert response.errors
    assert response.source_data_reference == LOCAL_FILE_SOURCE_REFERENCE
    assert "secret" not in str(response.model_dump()).lower()


def test_instrument_master_csv_and_parquet_files_return_local_file_response(tmp_path: Path) -> None:
    csv_path = tmp_path / "instruments.csv"
    parquet_path = tmp_path / "instruments.parquet"
    _write_csv(csv_path, _instrument_rows())
    _write_parquet(parquet_path, _instrument_rows())

    for path, file_format in [(csv_path, DatasetFormat.CSV), (parquet_path, DatasetFormat.PARQUET)]:
        provider = LocalFileProviderAdapter(settings=_settings(tmp_path), source=_source(path, file_format))
        request = create_market_data_request(MarketDataRequestKind.INSTRUMENT_MASTER)

        response = provider.get_instrument_master(request)

        assert response.provider == provider.provider_id
        assert response.source_data_reference == LOCAL_FILE_SOURCE_REFERENCE
        assert response.errors == []
        assert len(response.instruments) == 1
        assert response.instruments[0].display_name == "ABC Local File Test"
        assert response.instruments[0].metadata["source"] == LOCAL_FILE_SOURCE_REFERENCE


def test_historical_bars_csv_and_parquet_files_return_valid_bars(tmp_path: Path) -> None:
    csv_path = tmp_path / "ohlcv.csv"
    parquet_path = tmp_path / "ohlcv.parquet"
    _write_csv(csv_path, _ohlcv_rows())
    _write_parquet(parquet_path, _ohlcv_rows())
    request = _historical_request()

    for path, file_format in [(csv_path, DatasetFormat.CSV), (parquet_path, DatasetFormat.PARQUET)]:
        provider = LocalFileProviderAdapter(settings=_settings(tmp_path), source=_source(path, file_format))

        response = provider.get_historical_bars(request)

        assert response.errors == []
        assert len(response.bars) == 2
        for bar in response.bars:
            assert bar.provider == provider.provider_id
            assert bar.source_data_reference == LOCAL_FILE_SOURCE_REFERENCE
            assert bar.timestamp.tzinfo is not None
            assert bar.high >= max(bar.open, bar.close, bar.low)
            assert bar.low <= min(bar.open, bar.close, bar.high)


def test_historical_bars_are_deterministic_for_same_file(tmp_path: Path) -> None:
    path = tmp_path / "ohlcv.csv"
    _write_csv(path, _ohlcv_rows())
    provider = LocalFileProviderAdapter(settings=_settings(tmp_path), source=_source(path, DatasetFormat.CSV))
    request = _historical_request()

    first = provider.get_historical_bars(request)
    second = provider.get_historical_bars(request)

    assert first.errors == []
    assert to_jsonable(first.bars) == to_jsonable(second.bars)


def test_max_rows_is_enforced(tmp_path: Path) -> None:
    path = tmp_path / "ohlcv.csv"
    _write_csv(path, _ohlcv_rows())
    provider = LocalFileProviderAdapter(
        settings=_settings(tmp_path, local_file_provider_max_rows=1),
        source=_source(path, DatasetFormat.CSV),
    )

    response = provider.get_historical_bars(_historical_request())

    assert response.errors
    assert "max_rows" in response.errors[0]


def test_unsupported_capabilities_return_safe_errors(tmp_path: Path) -> None:
    provider = LocalFileProviderAdapter(settings=_settings(tmp_path))
    latest = create_market_data_request(MarketDataRequestKind.LATEST_BAR)
    options = create_market_data_request(MarketDataRequestKind.OPTIONS_CHAIN)
    futures = create_market_data_request(MarketDataRequestKind.FUTURES_CHAIN)

    latest_response = provider.get_latest_bar(latest)
    options_response = provider.get_options_chain(options)
    futures_response = provider.get_futures_chain(futures)

    assert latest_response.errors
    assert options_response.errors
    assert futures_response.errors
    assert "execution" not in str(latest_response.model_dump()).lower()
