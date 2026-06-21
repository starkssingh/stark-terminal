from pydantic import ValidationError
import pytest

from stark_terminal_core.domain.enums import Exchange, MarketSegment
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.instruments.universe import (
    InstrumentUniverseSnapshot,
    create_universe_snapshot,
    filter_by_exchange,
    filter_by_segment,
    find_instrument,
    index_instruments_by_key,
)


def test_valid_universe_snapshot_creation() -> None:
    snapshot = create_universe_snapshot(create_sample_instruments())

    assert snapshot.snapshot_id
    assert snapshot.source == "synthetic"
    assert len(snapshot.instruments) == 6
    assert snapshot.created_at.tzinfo is not None


def test_universe_rejects_empty_and_duplicate_instruments() -> None:
    instruments = create_sample_instruments()
    with pytest.raises(ValidationError):
        InstrumentUniverseSnapshot(source="synthetic", instruments=[])
    with pytest.raises(ValidationError):
        InstrumentUniverseSnapshot(source="synthetic", instruments=[instruments[0], instruments[0]])


def test_universe_index_filter_and_find_helpers() -> None:
    instruments = create_sample_instruments()
    indexed = index_instruments_by_key(instruments)

    assert "NSE:RELIANCE:NSE_EQUITY" in indexed
    assert all(item.instrument_id.exchange == Exchange.NSE for item in filter_by_exchange(instruments, "NSE"))
    assert all(item.instrument_id.segment == MarketSegment.INDEX for item in filter_by_segment(instruments, "INDEX"))
    assert find_instrument(instruments, "reliance", "NSE", "NSE_EQUITY") is not None
    assert find_instrument(instruments, "MISSING", "NSE", "NSE_EQUITY") is None
