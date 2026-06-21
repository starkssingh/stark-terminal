from __future__ import annotations

from stark_terminal_core.domain.enums import AssetClass, Exchange, InstrumentStatus, MarketSegment
from stark_terminal_core.domain.identifiers import InstrumentId
from stark_terminal_core.domain.instrument import Instrument


def _instrument(
    symbol: str,
    exchange: Exchange,
    segment: MarketSegment,
    display_name: str,
    asset_class: AssetClass,
    lot_size: int | None = 1,
    tick_size: float | None = 0.05,
    sector: str | None = None,
) -> Instrument:
    return Instrument(
        instrument_id=InstrumentId(symbol=symbol, exchange=exchange, segment=segment),
        display_name=display_name,
        asset_class=asset_class,
        status=InstrumentStatus.ACTIVE,
        lot_size=lot_size,
        tick_size=tick_size,
        sector=sector,
        metadata={"fixture": "synthetic", "scope": "local_test_only"},
    )


def create_sample_instruments() -> list[Instrument]:
    """Return tiny synthetic/local fixtures; these are not live market data."""

    return [
        _instrument(
            "RELIANCE",
            Exchange.NSE,
            MarketSegment.NSE_EQUITY,
            "Reliance Industries Synthetic",
            AssetClass.EQUITY,
            sector="Energy",
        ),
        _instrument(
            "HDFCBANK",
            Exchange.NSE,
            MarketSegment.NSE_EQUITY,
            "HDFC Bank Synthetic",
            AssetClass.EQUITY,
            sector="Financials",
        ),
        _instrument(
            "TCS",
            Exchange.NSE,
            MarketSegment.NSE_EQUITY,
            "Tata Consultancy Services Synthetic",
            AssetClass.EQUITY,
            sector="Information Technology",
        ),
        _instrument(
            "NIFTY",
            Exchange.NSE,
            MarketSegment.INDEX,
            "NIFTY 50 Synthetic Index",
            AssetClass.INDEX,
            lot_size=None,
            tick_size=None,
        ),
        _instrument(
            "BANKNIFTY",
            Exchange.NSE,
            MarketSegment.INDEX,
            "NIFTY Bank Synthetic Index",
            AssetClass.INDEX,
            lot_size=None,
            tick_size=None,
        ),
        _instrument(
            "SENSEX",
            Exchange.BSE,
            MarketSegment.INDEX,
            "SENSEX Synthetic Index",
            AssetClass.INDEX,
            lot_size=None,
            tick_size=None,
        ),
    ]
