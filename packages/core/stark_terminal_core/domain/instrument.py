from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from stark_terminal_core.domain.enums import AssetClass, InstrumentStatus
from stark_terminal_core.domain.identifiers import InstrumentId


class Instrument(BaseModel):
    instrument_id: InstrumentId
    display_name: str
    asset_class: AssetClass
    status: InstrumentStatus = InstrumentStatus.UNKNOWN
    lot_size: int | None = Field(default=None, gt=0)
    tick_size: float | None = Field(default=None, gt=0)
    isin: str | None = None
    sector: str | None = None
    industry: str | None = None
    metadata: dict[str, str] = Field(default_factory=dict)

    @field_validator("display_name", mode="before")
    @classmethod
    def display_name_must_be_non_empty(cls, value: str) -> str:
        if not isinstance(value, str):
            raise TypeError("display_name must be a string")
        normalized = value.strip()
        if not normalized:
            raise ValueError("display_name cannot be empty")
        return normalized
