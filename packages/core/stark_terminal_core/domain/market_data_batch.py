from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.domain.enums import DataQualityStatus, Timeframe
from stark_terminal_core.domain.identifiers import DataProviderId, InstrumentId
from stark_terminal_core.domain.market_data import MarketDataBatch, normalize_datetime_to_utc


SECRET_TEXT_PARTS = (
    "password",
    "secret",
    "token",
    "api_key",
    "database_url",
    "redis_url",
    "clickhouse_url",
    "kafka_bootstrap",
    "broker",
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _text_has_sensitive_content(value: str) -> bool:
    lowered = value.lower()
    return any(part in lowered for part in SECRET_TEXT_PARTS) or "://" in lowered


def _is_synthetic_local_test_reference(value: str) -> bool:
    lowered = value.lower()
    return "synthetic" in lowered and "local" in lowered and ("test" in lowered or "dev" in lowered)


def _sanitize_error(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    if not normalized:
        return None
    if _text_has_sensitive_content(normalized):
        return "sanitized_error"
    return normalized[:500]


class MarketDataBatchMetadata(BaseModel):
    batch_id: str
    instrument_id: InstrumentId
    timeframe: Timeframe
    provider: DataProviderId | None = None
    quality_status: DataQualityStatus
    row_count: int = Field(gt=0)
    start_timestamp: datetime
    end_timestamp: datetime
    source_data_reference: str
    synthetic: bool = False
    fixture_id: str | None = None
    dataset_manifest_id: str | None = None
    validation_report_id: str | None = None
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator(
        "batch_id",
        "source_data_reference",
        "schema_version",
        "fixture_id",
        "dataset_manifest_id",
        "validation_report_id",
        mode="before",
    )
    @classmethod
    def text_fields_must_be_safe(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str):
            raise TypeError("market data batch metadata text fields must be strings")
        normalized = value.strip()
        if not normalized:
            raise ValueError("market data batch metadata text fields cannot be empty")
        if _text_has_sensitive_content(normalized):
            raise ValueError("market data batch metadata text fields cannot contain secrets or raw URLs")
        return normalized

    @field_validator("start_timestamp", "end_timestamp", "created_at")
    @classmethod
    def timestamps_must_be_utc(cls, value: datetime) -> datetime:
        return normalize_datetime_to_utc(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_safe(cls, value: list[str]) -> list[str]:
        cleaned: list[str] = []
        for note in value:
            normalized = note.strip()
            if not normalized:
                continue
            if _text_has_sensitive_content(normalized):
                raise ValueError("market data batch metadata notes cannot contain secrets or raw URLs")
            cleaned.append(normalized[:500])
        return cleaned

    @model_validator(mode="after")
    def timestamps_and_synthetic_reference_must_be_consistent(self) -> MarketDataBatchMetadata:
        if self.start_timestamp > self.end_timestamp:
            raise ValueError("start_timestamp must be before or equal to end_timestamp")
        if self.synthetic and not _is_synthetic_local_test_reference(self.source_data_reference):
            raise ValueError("synthetic batch metadata requires synthetic/local/test source reference")
        return self


class MarketDataBatchPersistenceResult(BaseModel):
    batch_id: str
    persisted: bool
    status: str
    validation_status: str | None = None
    row_count: int | None = None
    error: str | None = None
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("batch_id", "status", "validation_status", mode="before")
    @classmethod
    def result_text_fields_must_be_safe(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str):
            raise TypeError("market data batch persistence result text fields must be strings")
        normalized = value.strip()
        if not normalized:
            raise ValueError("market data batch persistence result text fields cannot be empty")
        if _text_has_sensitive_content(normalized):
            raise ValueError("market data batch persistence result text fields cannot contain secrets or raw URLs")
        return normalized

    @field_validator("error", mode="before")
    @classmethod
    def error_must_be_sanitized(cls, value: str | None) -> str | None:
        return _sanitize_error(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_utc(cls, value: datetime) -> datetime:
        return normalize_datetime_to_utc(value)


def batch_metadata_key(metadata: MarketDataBatchMetadata) -> str:
    return (
        f"{metadata.instrument_id}:{metadata.timeframe.value}:"
        f"{metadata.start_timestamp.isoformat()}:{metadata.end_timestamp.isoformat()}:"
        f"{metadata.row_count}:{metadata.source_data_reference}"
    )


def validate_batch_metadata_identity(metadata: MarketDataBatchMetadata) -> MarketDataBatchMetadata:
    if not metadata.batch_id.strip():
        raise ValueError("batch_id cannot be empty")
    if metadata.row_count <= 0:
        raise ValueError("row_count must be positive")
    if metadata.start_timestamp > metadata.end_timestamp:
        raise ValueError("start_timestamp must be before or equal to end_timestamp")
    return metadata


def _stable_batch_id(parts: dict[str, Any]) -> str:
    payload = "|".join(str(parts[key]) for key in sorted(parts))
    return f"batch_{sha256(payload.encode('utf-8')).hexdigest()[:32]}"


def metadata_from_batch(
    batch: MarketDataBatch,
    batch_id: str | None = None,
    synthetic: bool = False,
    fixture_id: str | None = None,
    dataset_manifest_id: str | None = None,
    validation_report_id: str | None = None,
    schema_version: str = "v1",
) -> MarketDataBatchMetadata:
    bars = sorted(batch.bars, key=lambda item: item.timestamp)
    first = bars[0]
    instrument_id = first.instrument_id
    timeframe = first.timeframe
    if any(bar.instrument_id != instrument_id for bar in bars):
        raise ValueError("market data batch metadata requires one instrument per batch")
    if any(bar.timeframe != timeframe for bar in bars):
        raise ValueError("market data batch metadata requires one timeframe per batch")
    source_data_reference = first.source_data_reference or ""
    if not source_data_reference:
        raise ValueError("source_data_reference cannot be empty")

    start_timestamp = bars[0].timestamp
    end_timestamp = bars[-1].timestamp
    provider = batch.provider or first.provider
    parts = {
        "instrument": str(instrument_id),
        "timeframe": timeframe.value,
        "start": start_timestamp.isoformat(),
        "end": end_timestamp.isoformat(),
        "row_count": len(bars),
        "source": source_data_reference,
        "fixture": fixture_id or "",
    }
    return MarketDataBatchMetadata(
        batch_id=batch_id or _stable_batch_id(parts),
        instrument_id=instrument_id,
        timeframe=timeframe,
        provider=provider,
        quality_status=batch.quality_status,
        row_count=len(bars),
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        source_data_reference=source_data_reference,
        synthetic=synthetic,
        fixture_id=fixture_id,
        dataset_manifest_id=dataset_manifest_id,
        validation_report_id=validation_report_id,
        schema_version=schema_version,
    )
