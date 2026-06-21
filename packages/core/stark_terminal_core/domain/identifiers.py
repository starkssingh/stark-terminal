from __future__ import annotations

from uuid import uuid4

from pydantic import BaseModel, field_validator

from stark_terminal_core.domain.enums import DataProviderType, Exchange, MarketSegment


class InstrumentId(BaseModel):
    symbol: str
    exchange: Exchange
    segment: MarketSegment

    @field_validator("symbol", mode="before")
    @classmethod
    def normalize_symbol(cls, value: str) -> str:
        if not isinstance(value, str):
            raise TypeError("symbol must be a string")
        normalized = value.strip().upper()
        if not normalized:
            raise ValueError("symbol cannot be empty")
        return normalized

    def __str__(self) -> str:
        return f"{self.exchange.value}:{self.symbol}:{self.segment.value}"


class DataProviderId(BaseModel):
    name: str
    provider_type: DataProviderType
    version: str | None = None

    @field_validator("name", mode="before")
    @classmethod
    def name_must_be_non_empty(cls, value: str) -> str:
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        normalized = value.strip()
        if not normalized:
            raise ValueError("name cannot be empty")
        return normalized


class AuditId(BaseModel):
    value: str

    @field_validator("value", mode="before")
    @classmethod
    def value_must_be_non_empty(cls, value: str) -> str:
        if not isinstance(value, str):
            raise TypeError("audit id must be a string")
        normalized = value.strip()
        if not normalized:
            raise ValueError("audit id cannot be empty")
        return normalized

    @classmethod
    def new(cls) -> AuditId:
        return cls(value=f"audit_{uuid4().hex}")

    def __str__(self) -> str:
        return self.value
