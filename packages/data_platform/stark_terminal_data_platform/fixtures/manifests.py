from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.domain.enums import FixtureKind, FixtureStatus, Timeframe
from stark_terminal_core.serialization.json import to_jsonable


SYNTHETIC_LABEL_PARTS = ("synthetic", "local", "test")
REAL_DATA_MARKERS = ("live", "real", "vendor", "broker", "nse-feed", "bse-feed", "provider-feed")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def normalize_to_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def text_mentions_synthetic_local_test(value: str) -> bool:
    lowered = value.lower()
    return all(part in lowered for part in SYNTHETIC_LABEL_PARTS)


def text_implies_real_market_data(value: str | None) -> bool:
    if value is None:
        return False
    lowered = value.lower()
    return any(marker in lowered for marker in REAL_DATA_MARKERS)


class FixtureManifest(BaseModel):
    fixture_id: str
    name: str
    kind: FixtureKind
    status: FixtureStatus = FixtureStatus.AVAILABLE
    label: str
    schema_version: str
    instrument_key: str | None = None
    provider_name: str = "local_sample"
    row_count: int | None = Field(default=None, ge=0)
    timeframe: Timeframe | None = None
    start_timestamp: datetime | None = None
    end_timestamp: datetime | None = None
    seed: int | None = None
    source_data_reference: str | None = None
    notes: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("fixture_id", "name", "label", "schema_version", "provider_name", mode="before")
    @classmethod
    def required_text_must_be_non_empty(cls, value: str) -> str:
        if not isinstance(value, str):
            raise TypeError("fixture manifest text fields must be strings")
        normalized = value.strip()
        if not normalized:
            raise ValueError("fixture manifest text fields cannot be empty")
        return normalized

    @field_validator("instrument_key", "source_data_reference")
    @classmethod
    def optional_text_must_be_non_empty(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        if not normalized:
            raise ValueError("fixture manifest optional text fields cannot be empty")
        return normalized

    @field_validator("start_timestamp", "end_timestamp", "created_at")
    @classmethod
    def timestamps_must_be_utc(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None
        return normalize_to_utc(value)

    @model_validator(mode="after")
    def manifest_must_remain_synthetic(self) -> FixtureManifest:
        if not text_mentions_synthetic_local_test(self.label):
            raise ValueError("fixture label must include synthetic, local, and test semantics")
        if self.source_data_reference is not None:
            if text_implies_real_market_data(self.source_data_reference):
                raise ValueError("fixture source reference must not imply live or real provider data")
            if not text_mentions_synthetic_local_test(self.source_data_reference):
                raise ValueError("fixture source reference must include synthetic, local, and test semantics")
        if self.start_timestamp and self.end_timestamp and self.start_timestamp >= self.end_timestamp:
            raise ValueError("fixture start_timestamp must be before end_timestamp")
        return self


def create_fixture_manifest(
    fixture_id: str,
    name: str,
    kind: FixtureKind,
    *,
    label: str = "synthetic-local-test-only",
    schema_version: str = "v1",
    status: FixtureStatus = FixtureStatus.AVAILABLE,
    instrument_key: str | None = None,
    provider_name: str = "local_sample",
    row_count: int | None = None,
    timeframe: Timeframe | None = None,
    start_timestamp: datetime | None = None,
    end_timestamp: datetime | None = None,
    seed: int | None = None,
    source_data_reference: str | None = "synthetic-local-test-only",
    notes: list[str] | None = None,
) -> FixtureManifest:
    return FixtureManifest(
        fixture_id=fixture_id,
        name=name,
        kind=kind,
        status=status,
        label=label,
        schema_version=schema_version,
        instrument_key=instrument_key,
        provider_name=provider_name,
        row_count=row_count,
        timeframe=timeframe,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        seed=seed,
        source_data_reference=source_data_reference,
        notes=notes or [],
    )


def fixture_manifest_to_jsonable(manifest: FixtureManifest) -> dict[str, Any]:
    return to_jsonable(manifest.model_dump())
