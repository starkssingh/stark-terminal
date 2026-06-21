from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.domain.enums import DataQualityStatus, Timeframe
from stark_terminal_core.domain.identifiers import DataProviderId, InstrumentId


def normalize_datetime_to_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


class MarketDataBar(BaseModel):
    instrument_id: InstrumentId
    timeframe: Timeframe
    timestamp: datetime
    open: float = Field(gt=0)
    high: float = Field(gt=0)
    low: float = Field(gt=0)
    close: float = Field(gt=0)
    volume: float | None = Field(default=None, ge=0)
    open_interest: float | None = Field(default=None, ge=0)
    provider: DataProviderId | None = None
    quality_status: DataQualityStatus = DataQualityStatus.RAW
    source_data_reference: str | None = None

    @field_validator("timestamp")
    @classmethod
    def timestamp_must_be_utc(cls, value: datetime) -> datetime:
        return normalize_datetime_to_utc(value)

    @model_validator(mode="after")
    def validate_ohlc_relationships(self) -> MarketDataBar:
        if self.high < max(self.open, self.close, self.low):
            raise ValueError("high must be greater than or equal to open, close, and low")
        if self.low > min(self.open, self.close, self.high):
            raise ValueError("low must be less than or equal to open, close, and high")
        return self


class MarketDataBatch(BaseModel):
    bars: list[MarketDataBar]
    provider: DataProviderId | None = None
    quality_status: DataQualityStatus = DataQualityStatus.RAW

    @field_validator("bars")
    @classmethod
    def bars_cannot_be_empty(cls, value: list[MarketDataBar]) -> list[MarketDataBar]:
        if not value:
            raise ValueError("bars cannot be empty")
        return value
