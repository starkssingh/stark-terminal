from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.domain.enums import OptionType
from stark_terminal_core.domain.identifiers import DataProviderId, InstrumentId
from stark_terminal_core.domain.market_data import normalize_datetime_to_utc


class OptionContract(BaseModel):
    underlying: InstrumentId
    contract_symbol: str
    expiry: date
    strike: float = Field(gt=0)
    option_type: OptionType
    lot_size: int = Field(gt=0)
    tick_size: float | None = Field(default=None, gt=0)
    provider: DataProviderId | None = None
    metadata: dict[str, str] = Field(default_factory=dict)

    @field_validator("contract_symbol", mode="before")
    @classmethod
    def contract_symbol_must_be_non_empty(cls, value: str) -> str:
        if not isinstance(value, str):
            raise TypeError("contract_symbol must be a string")
        normalized = value.strip().upper()
        if not normalized:
            raise ValueError("contract_symbol cannot be empty")
        return normalized


class OptionsChainSnapshot(BaseModel):
    underlying: InstrumentId
    timestamp: datetime
    expiry: date
    contracts: list[OptionContract]
    provider: DataProviderId | None = None
    source_data_reference: str | None = None

    @field_validator("timestamp")
    @classmethod
    def timestamp_must_be_utc(cls, value: datetime) -> datetime:
        return normalize_datetime_to_utc(value)

    @field_validator("contracts")
    @classmethod
    def contracts_cannot_be_empty(
        cls, value: list[OptionContract]
    ) -> list[OptionContract]:
        if not value:
            raise ValueError("contracts cannot be empty")
        return value

    @model_validator(mode="after")
    def contracts_must_match_snapshot(self) -> OptionsChainSnapshot:
        for contract in self.contracts:
            if contract.underlying != self.underlying:
                raise ValueError("all contracts must share the same underlying")
            if contract.expiry != self.expiry:
                raise ValueError("all contracts must share the same expiry")
        return self
