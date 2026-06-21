from datetime import datetime, timedelta, timezone

from stark_terminal_core.domain.enums import DataProviderType, Exchange, MarketSegment, Timeframe
from stark_terminal_core.domain.identifiers import InstrumentId
from stark_terminal_data_platform.fixtures.synthetic_ohlcv import (
    SyntheticOHLCVConfig,
    generate_synthetic_market_data_batch,
    generate_synthetic_ohlcv_bars,
)


def _config(seed: int = 42, timeframe: Timeframe = Timeframe.DAILY) -> SyntheticOHLCVConfig:
    return SyntheticOHLCVConfig(
        instrument_id=InstrumentId(symbol="RELIANCE", exchange=Exchange.NSE, segment=MarketSegment.NSE_EQUITY),
        timeframe=timeframe,
        start_timestamp=datetime(2024, 1, 1, tzinfo=timezone.utc),
        bar_count=5,
        start_price=100.0,
        seed=seed,
    )


def test_same_seed_produces_identical_bars() -> None:
    first = generate_synthetic_ohlcv_bars(_config(seed=42))
    second = generate_synthetic_ohlcv_bars(_config(seed=42))

    assert [bar.model_dump() for bar in first] == [bar.model_dump() for bar in second]


def test_different_seed_produces_different_bars() -> None:
    first = generate_synthetic_ohlcv_bars(_config(seed=42))
    second = generate_synthetic_ohlcv_bars(_config(seed=43))

    assert [bar.close for bar in first] != [bar.close for bar in second]


def test_bar_count_and_ohlc_constraints_hold() -> None:
    bars = generate_synthetic_ohlcv_bars(_config())

    assert len(bars) == 5
    for bar in bars:
        assert bar.timestamp.tzinfo is not None
        assert bar.high >= max(bar.open, bar.close, bar.low)
        assert bar.low <= min(bar.open, bar.close, bar.high)
        assert min(bar.open, bar.high, bar.low, bar.close) > 0
        assert bar.volume is not None and bar.volume >= 0
        assert bar.provider is not None
        assert bar.provider.provider_type == DataProviderType.LOCAL_SAMPLE
        assert bar.source_data_reference == "synthetic-local-test-only"


def test_timestamps_increment_for_supported_timeframes() -> None:
    expectations = {
        Timeframe.DAILY: timedelta(days=1),
        Timeframe.FIFTEEN_MINUTE: timedelta(minutes=15),
        Timeframe.FIVE_MINUTE: timedelta(minutes=5),
    }

    for timeframe, expected_delta in expectations.items():
        bars = generate_synthetic_ohlcv_bars(_config(timeframe=timeframe))
        assert bars[1].timestamp - bars[0].timestamp == expected_delta


def test_generated_market_data_batch_is_valid() -> None:
    batch = generate_synthetic_market_data_batch(_config())

    assert len(batch.bars) == 5
    assert batch.provider is not None
    assert batch.provider.provider_type == DataProviderType.LOCAL_SAMPLE
