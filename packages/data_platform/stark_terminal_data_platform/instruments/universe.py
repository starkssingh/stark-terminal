from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.domain.enums import Exchange, MarketSegment
from stark_terminal_core.domain.instrument import Instrument
from stark_terminal_core.domain.market_data import normalize_datetime_to_utc
from stark_terminal_data_platform.instruments.normalization import (
    build_instrument_key,
    normalize_exchange,
    normalize_segment,
    normalize_symbol,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class InstrumentUniverseSnapshot(BaseModel):
    snapshot_id: str = Field(default_factory=lambda: f"universe_{uuid4().hex}")
    source: str
    instruments: list[Instrument]
    created_at: datetime = Field(default_factory=_utc_now)
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)

    @field_validator("snapshot_id", "source", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("snapshot_id, source, and schema_version cannot be empty")
        return normalized

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_utc(cls, value: datetime) -> datetime:
        return normalize_datetime_to_utc(value)

    @field_validator("instruments")
    @classmethod
    def instruments_cannot_be_empty(cls, value: list[Instrument]) -> list[Instrument]:
        if not value:
            raise ValueError("instrument universe cannot be empty")
        return value

    @model_validator(mode="after")
    def instrument_keys_must_be_unique(self) -> InstrumentUniverseSnapshot:
        keys = [str(instrument.instrument_id) for instrument in self.instruments]
        if len(keys) != len(set(keys)):
            raise ValueError("instrument universe cannot contain duplicate instrument keys")
        return self


def create_universe_snapshot(
    instruments: list[Instrument],
    source: str = "synthetic",
    schema_version: str = "v1",
) -> InstrumentUniverseSnapshot:
    return InstrumentUniverseSnapshot(
        source=source,
        instruments=instruments,
        schema_version=schema_version,
    )


def index_instruments_by_key(instruments: list[Instrument]) -> dict[str, Instrument]:
    indexed: dict[str, Instrument] = {}
    for instrument in instruments:
        key = str(instrument.instrument_id)
        if key in indexed:
            raise ValueError(f"duplicate instrument key: {key}")
        indexed[key] = instrument
    return indexed


def filter_by_exchange(instruments: list[Instrument], exchange: str | Exchange) -> list[Instrument]:
    normalized_exchange = normalize_exchange(exchange)
    return [
        instrument
        for instrument in instruments
        if instrument.instrument_id.exchange == normalized_exchange
    ]


def filter_by_segment(
    instruments: list[Instrument],
    segment: str | MarketSegment,
) -> list[Instrument]:
    normalized_segment = normalize_segment(segment)
    return [
        instrument
        for instrument in instruments
        if instrument.instrument_id.segment == normalized_segment
    ]


def find_instrument(
    instruments: list[Instrument],
    symbol: str,
    exchange: str | Exchange,
    segment: str | MarketSegment,
) -> Instrument | None:
    key = build_instrument_key(normalize_symbol(symbol), exchange, segment)
    return index_instruments_by_key(instruments).get(key)
