from datetime import datetime

from pydantic import ValidationError
import pytest

from stark_terminal_core.domain.enums import Exchange, MarketSegment, Timeframe
from stark_terminal_core.domain.identifiers import InstrumentId
from stark_terminal_core.domain.market_data import MarketDataBar, MarketDataBatch


def instrument_id() -> InstrumentId:
    return InstrumentId(
        symbol="NIFTY",
        exchange=Exchange.NSE,
        segment=MarketSegment.INDEX,
    )


def valid_bar(**overrides: object) -> MarketDataBar:
    payload = {
        "instrument_id": instrument_id(),
        "timeframe": Timeframe.DAILY,
        "timestamp": datetime(2026, 1, 1, 9, 15),
        "open": 100.0,
        "high": 110.0,
        "low": 95.0,
        "close": 105.0,
        "volume": 1000.0,
    }
    payload.update(overrides)
    return MarketDataBar(**payload)


def test_valid_ohlc_bar_creation() -> None:
    bar = valid_bar()

    assert bar.high == 110.0
    assert bar.timestamp.tzinfo is not None


def test_high_validation_rejects_invalid_bar() -> None:
    with pytest.raises(ValidationError):
        valid_bar(high=99.0)


def test_low_validation_rejects_invalid_bar() -> None:
    with pytest.raises(ValidationError):
        valid_bar(low=106.0)


def test_negative_volume_rejected() -> None:
    with pytest.raises(ValidationError):
        valid_bar(volume=-1.0)


def test_market_data_batch_rejects_empty_bars() -> None:
    with pytest.raises(ValidationError):
        MarketDataBatch(bars=[])
