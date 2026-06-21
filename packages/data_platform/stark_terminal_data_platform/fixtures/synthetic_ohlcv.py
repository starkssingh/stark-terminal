from __future__ import annotations

from datetime import datetime, timedelta, timezone
from random import Random

from pydantic import BaseModel, Field, field_validator

from stark_terminal_core.domain.enums import DataProviderType, DataQualityStatus, Timeframe
from stark_terminal_core.domain.identifiers import DataProviderId, InstrumentId
from stark_terminal_core.domain.market_data import MarketDataBar, MarketDataBatch
from stark_terminal_data_platform.fixtures.manifests import text_mentions_synthetic_local_test


def normalize_to_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def local_sample_provider() -> DataProviderId:
    return DataProviderId(name="local_sample", provider_type=DataProviderType.LOCAL_SAMPLE, version="synthetic-v1")


class SyntheticOHLCVConfig(BaseModel):
    instrument_id: InstrumentId
    timeframe: Timeframe
    start_timestamp: datetime
    bar_count: int = Field(gt=0)
    start_price: float = Field(gt=0)
    seed: int = 42
    provider: DataProviderId | None = None
    quality_status: DataQualityStatus = DataQualityStatus.RAW
    source_data_reference: str = "synthetic-local-test-only"

    @field_validator("start_timestamp")
    @classmethod
    def start_timestamp_must_be_utc(cls, value: datetime) -> datetime:
        return normalize_to_utc(value)

    @field_validator("source_data_reference")
    @classmethod
    def source_reference_must_be_synthetic(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("source_data_reference cannot be empty")
        if not text_mentions_synthetic_local_test(normalized):
            raise ValueError("source_data_reference must include synthetic, local, and test semantics")
        return normalized


def _timeframe_delta(timeframe: Timeframe) -> timedelta:
    if timeframe == Timeframe.DAILY:
        return timedelta(days=1)
    if timeframe == Timeframe.FIFTEEN_MINUTE:
        return timedelta(minutes=15)
    if timeframe == Timeframe.FIVE_MINUTE:
        return timedelta(minutes=5)
    raise ValueError("synthetic OHLCV fixtures support DAILY, FIFTEEN_MINUTE, and FIVE_MINUTE")


def deterministic_price_path(seed: int, bar_count: int, start_price: float) -> list[dict[str, float]]:
    if bar_count <= 0:
        raise ValueError("bar_count must be positive")
    if start_price <= 0:
        raise ValueError("start_price must be positive")

    rng = Random(seed)
    previous_close = float(start_price)
    rows: list[dict[str, float]] = []
    for _ in range(bar_count):
        open_price = max(0.01, previous_close)
        move = rng.uniform(-0.018, 0.018)
        close_price = max(0.01, open_price * (1.0 + move))
        spread = max(0.01, open_price * rng.uniform(0.001, 0.012))
        high_price = max(open_price, close_price) + spread
        low_price = max(0.01, min(open_price, close_price) - spread)
        volume = float(int(1_000 + rng.random() * 9_000))
        rows.append(
            {
                "open": round(open_price, 4),
                "high": round(high_price, 4),
                "low": round(low_price, 4),
                "close": round(close_price, 4),
                "volume": volume,
                "open_interest": 0.0,
            }
        )
        previous_close = close_price
    return rows


def generate_synthetic_ohlcv_bars(config: SyntheticOHLCVConfig) -> list[MarketDataBar]:
    step = _timeframe_delta(config.timeframe)
    provider = config.provider or local_sample_provider()
    rows = deterministic_price_path(config.seed, config.bar_count, config.start_price)
    return [
        MarketDataBar(
            instrument_id=config.instrument_id,
            timeframe=config.timeframe,
            timestamp=config.start_timestamp + (step * index),
            open=row["open"],
            high=row["high"],
            low=row["low"],
            close=row["close"],
            volume=row["volume"],
            open_interest=row["open_interest"],
            provider=provider,
            quality_status=config.quality_status,
            source_data_reference=config.source_data_reference,
        )
        for index, row in enumerate(rows)
    ]


def generate_synthetic_market_data_batch(config: SyntheticOHLCVConfig) -> MarketDataBatch:
    provider = config.provider or local_sample_provider()
    return MarketDataBatch(
        bars=generate_synthetic_ohlcv_bars(config),
        provider=provider,
        quality_status=config.quality_status,
    )
