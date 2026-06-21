from datetime import datetime, timezone

import pytest

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import Exchange, MarketSegment, Timeframe
from stark_terminal_core.domain.identifiers import InstrumentId
from stark_terminal_data_platform.fixtures.parquet import (
    bars_to_polars_frame,
    read_fixture_bars_from_parquet,
    write_fixture_bars_to_parquet,
)
from stark_terminal_data_platform.fixtures.synthetic_ohlcv import SyntheticOHLCVConfig, generate_synthetic_ohlcv_bars


def _bars():
    config = SyntheticOHLCVConfig(
        instrument_id=InstrumentId(symbol="RELIANCE", exchange=Exchange.NSE, segment=MarketSegment.NSE_EQUITY),
        timeframe=Timeframe.DAILY,
        start_timestamp=datetime(2024, 1, 1, tzinfo=timezone.utc),
        bar_count=3,
        start_price=100.0,
    )
    return generate_synthetic_ohlcv_bars(config)


def test_bars_to_polars_frame() -> None:
    frame = bars_to_polars_frame(_bars())

    assert frame.height == 3
    assert "instrument_id" in frame.columns
    assert "close" in frame.columns


def test_write_and_read_tiny_fixture_parquet_tmp_path(tmp_path) -> None:
    target = tmp_path / "fixture.parquet"

    written = write_fixture_bars_to_parquet(_bars(), target)
    frame = read_fixture_bars_from_parquet(written)

    assert written == target
    assert frame.height == 3
    assert tmp_path in written.parents


def test_configured_output_root_write_rejected_when_disabled(tmp_path) -> None:
    settings = Settings(synthetic_fixture_output_root=str(tmp_path / "configured_root"))
    target = tmp_path / "configured_root" / "fixture.parquet"

    with pytest.raises(ValueError):
        write_fixture_bars_to_parquet(_bars(), target, settings=settings)
