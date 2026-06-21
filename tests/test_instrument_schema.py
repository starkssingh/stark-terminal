from pydantic import ValidationError
import pytest

from stark_terminal_core.domain.enums import AssetClass, Exchange, MarketSegment
from stark_terminal_core.domain.identifiers import InstrumentId
from stark_terminal_core.domain.instrument import Instrument


def instrument_id() -> InstrumentId:
    return InstrumentId(
        symbol="RELIANCE",
        exchange=Exchange.NSE,
        segment=MarketSegment.NSE_EQUITY,
    )


def test_valid_instrument_creation() -> None:
    instrument = Instrument(
        instrument_id=instrument_id(),
        display_name="Reliance Industries",
        asset_class=AssetClass.EQUITY,
        lot_size=1,
        tick_size=0.05,
    )

    assert instrument.display_name == "Reliance Industries"
    assert instrument.metadata == {}


def test_invalid_lot_size_rejected() -> None:
    with pytest.raises(ValidationError):
        Instrument(
            instrument_id=instrument_id(),
            display_name="Reliance Industries",
            asset_class=AssetClass.EQUITY,
            lot_size=0,
        )


def test_invalid_tick_size_rejected() -> None:
    with pytest.raises(ValidationError):
        Instrument(
            instrument_id=instrument_id(),
            display_name="Reliance Industries",
            asset_class=AssetClass.EQUITY,
            tick_size=-0.05,
        )
