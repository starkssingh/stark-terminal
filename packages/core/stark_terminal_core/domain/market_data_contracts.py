from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.domain.enums import (
    AdjustmentMode,
    DataQualityStatus,
    MarketDataRequestKind,
    Timeframe,
)
from stark_terminal_core.domain.identifiers import DataProviderId, InstrumentId
from stark_terminal_core.domain.instrument import Instrument
from stark_terminal_core.domain.market_data import MarketDataBar, normalize_datetime_to_utc


FORBIDDEN_PROVIDER_TEXT = (
    "password",
    "secret",
    "token",
    "api_key",
    "database_url",
    "redis_url",
    "broker_token",
    "broker_secret",
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _text_has_secret(value: str | None) -> bool:
    if value is None:
        return False
    normalized = value.lower()
    return any(part in normalized for part in FORBIDDEN_PROVIDER_TEXT)


def _provider_must_be_safe(provider: DataProviderId | None) -> None:
    if provider is None:
        return
    if _text_has_secret(provider.name) or _text_has_secret(provider.version):
        raise ValueError("provider identity must not contain credentials or secret-like values")


def sanitize_market_data_error(error: str) -> str:
    if _text_has_secret(error):
        return "SanitizedMarketDataError"
    return error.strip()


class MarketDataRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: f"mdreq_{uuid4().hex}")
    kind: MarketDataRequestKind
    instrument_id: InstrumentId | None = None
    timeframe: Timeframe | None = None
    start: datetime | None = None
    end: datetime | None = None
    provider: DataProviderId | None = None
    adjustment_mode: AdjustmentMode = AdjustmentMode.RAW
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("request_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("request_id and schema_version cannot be empty")
        return normalized

    @field_validator("start", "end", "created_at")
    @classmethod
    def datetimes_must_be_utc(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None
        return normalize_datetime_to_utc(value)

    @field_validator("provider")
    @classmethod
    def provider_must_not_include_secret_text(
        cls, value: DataProviderId | None
    ) -> DataProviderId | None:
        _provider_must_be_safe(value)
        return value

    @model_validator(mode="after")
    def validate_request_shape(self) -> MarketDataRequest:
        if self.start and self.end and self.start >= self.end:
            raise ValueError("start must be before end")
        if self.kind == MarketDataRequestKind.HISTORICAL_BARS:
            missing = [
                name
                for name, value in {
                    "instrument_id": self.instrument_id,
                    "timeframe": self.timeframe,
                    "start": self.start,
                    "end": self.end,
                }.items()
                if value is None
            ]
            if missing:
                raise ValueError(f"historical bars requests require: {', '.join(missing)}")
        return self


class MarketDataResponse(BaseModel):
    request_id: str
    kind: MarketDataRequestKind
    provider: DataProviderId | None = None
    bars: list[MarketDataBar] = Field(default_factory=list)
    instruments: list[Instrument] = Field(default_factory=list)
    quality_status: DataQualityStatus = DataQualityStatus.UNKNOWN
    source_data_reference: str | None = None
    received_at: datetime = Field(default_factory=_utc_now)
    errors: list[str] = Field(default_factory=list)

    @field_validator("request_id")
    @classmethod
    def request_id_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("request_id cannot be empty")
        return normalized

    @field_validator("received_at")
    @classmethod
    def received_at_must_be_utc(cls, value: datetime) -> datetime:
        return normalize_datetime_to_utc(value)

    @field_validator("provider")
    @classmethod
    def provider_must_be_safe(cls, value: DataProviderId | None) -> DataProviderId | None:
        _provider_must_be_safe(value)
        return value

    @field_validator("errors")
    @classmethod
    def errors_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return [sanitize_market_data_error(item) for item in value]

    @model_validator(mode="after")
    def response_must_have_content_or_error(self) -> MarketDataResponse:
        if not self.bars and not self.instruments and not self.errors:
            raise ValueError("market data response must contain bars, instruments, or errors")
        return self


def create_market_data_request(
    kind: MarketDataRequestKind,
    instrument_id: InstrumentId | None = None,
    timeframe: Timeframe | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
    provider: DataProviderId | None = None,
    adjustment_mode: AdjustmentMode = AdjustmentMode.RAW,
    schema_version: str = "v1",
    **extra: Any,
) -> MarketDataRequest:
    return MarketDataRequest(
        kind=kind,
        instrument_id=instrument_id,
        timeframe=timeframe,
        start=start,
        end=end,
        provider=provider,
        adjustment_mode=adjustment_mode,
        schema_version=schema_version,
        **extra,
    )
