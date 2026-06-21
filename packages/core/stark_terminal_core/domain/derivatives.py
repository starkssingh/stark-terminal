from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field, field_validator

from stark_terminal_core.domain.identifiers import DataProviderId, InstrumentId


class FuturesContract(BaseModel):
    underlying: InstrumentId
    contract_symbol: str
    expiry: date
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
