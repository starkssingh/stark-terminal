from __future__ import annotations

from abc import ABC, abstractmethod

from stark_terminal_core.domain.enums import Exchange, MarketSegment
from stark_terminal_core.domain.instrument import Instrument
from stark_terminal_data_platform.instruments.normalization import (
    build_instrument_key,
    normalize_symbol,
)
from stark_terminal_data_platform.instruments.universe import (
    InstrumentUniverseSnapshot,
    create_universe_snapshot,
    find_instrument,
    index_instruments_by_key,
)


class InstrumentMaster(ABC):
    @abstractmethod
    def list_instruments(self) -> list[Instrument]:
        raise NotImplementedError

    @abstractmethod
    def get_instrument(
        self,
        symbol: str,
        exchange: str | Exchange,
        segment: str | MarketSegment,
    ) -> Instrument | None:
        raise NotImplementedError

    @abstractmethod
    def search(self, query: str, limit: int = 20) -> list[Instrument]:
        raise NotImplementedError

    @abstractmethod
    def snapshot(self) -> InstrumentUniverseSnapshot:
        raise NotImplementedError


class LocalInstrumentMaster(InstrumentMaster):
    def __init__(
        self,
        instruments: list[Instrument],
        source: str = "synthetic",
        schema_version: str = "v1",
    ) -> None:
        self._instruments = list(instruments)
        self._index = index_instruments_by_key(self._instruments)
        self.source = source
        self.schema_version = schema_version

    def list_instruments(self) -> list[Instrument]:
        return list(self._instruments)

    def get_instrument(
        self,
        symbol: str,
        exchange: str | Exchange,
        segment: str | MarketSegment,
    ) -> Instrument | None:
        key = build_instrument_key(symbol, exchange, segment)
        return self._index.get(key)

    def search(self, query: str, limit: int = 20) -> list[Instrument]:
        if limit <= 0:
            raise ValueError("search limit must be positive")
        normalized_query = normalize_symbol(query)
        results = [
            instrument
            for instrument in self._instruments
            if normalized_query in instrument.instrument_id.symbol
            or normalized_query in instrument.display_name.upper()
        ]
        return results[:limit]

    def snapshot(self) -> InstrumentUniverseSnapshot:
        return create_universe_snapshot(
            self.list_instruments(),
            source=self.source,
            schema_version=self.schema_version,
        )

    def find(
        self,
        symbol: str,
        exchange: str | Exchange,
        segment: str | MarketSegment,
    ) -> Instrument | None:
        return find_instrument(self._instruments, symbol, exchange, segment)
