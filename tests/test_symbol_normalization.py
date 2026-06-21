import pytest

from stark_terminal_core.domain.enums import Exchange, MarketSegment
from stark_terminal_data_platform.instruments.normalization import (
    build_instrument_key,
    normalize_exchange,
    normalize_segment,
    normalize_symbol,
    parse_instrument_key,
)


def test_normalize_symbol_uppercases_and_trims() -> None:
    assert normalize_symbol(" reliance ") == "RELIANCE"
    assert normalize_symbol("m-m") == "M-M"
    assert normalize_symbol("a.b") == "A.B"


@pytest.mark.parametrize("symbol", ["", "   ", "REL\nIANCE", "../RELIANCE", "A/B", "http://x"])
def test_normalize_symbol_rejects_unsafe_values(symbol: str) -> None:
    with pytest.raises(ValueError):
        normalize_symbol(symbol)


def test_normalize_exchange_and_segment() -> None:
    assert normalize_exchange("nse") == Exchange.NSE
    assert normalize_exchange(Exchange.BSE) == Exchange.BSE
    assert normalize_segment("nse_equity") == MarketSegment.NSE_EQUITY
    assert normalize_segment(MarketSegment.INDEX) == MarketSegment.INDEX


def test_build_and_parse_instrument_key_roundtrip() -> None:
    key = build_instrument_key("reliance", "nse", "nse_equity")

    assert key == "NSE:RELIANCE:NSE_EQUITY"
    parsed = parse_instrument_key(key)
    assert str(parsed) == key
