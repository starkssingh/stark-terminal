from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from stark_terminal_core.domain.enums import DataLakeZone, DatasetFormat, DatasetKind
from stark_terminal_core.serialization.json import to_jsonable
from stark_terminal_data_platform.lake.zones import normalize_zone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _reject_traversal(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} cannot be empty")
    if Path(normalized).is_absolute() or ".." in Path(normalized).parts:
        raise ValueError(f"{field_name} cannot be absolute or contain traversal")
    return normalized


class DatasetPartition(BaseModel):
    key: str
    value: str

    @field_validator("key", "value", mode="before")
    @classmethod
    def partition_fields_must_be_non_empty(cls, value: str) -> str:
        return _reject_traversal(str(value), "partition")


class DatasetManifest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    dataset_id: str
    name: str
    kind: DatasetKind
    zone: DataLakeZone
    format: DatasetFormat = DatasetFormat.PARQUET
    version: str = "v1"
    path: str
    partitions: list[DatasetPartition] = Field(default_factory=list)
    row_count: int | None = Field(default=None, ge=0)
    schema_map: dict[str, str] = Field(default_factory=dict, alias="schema_json")
    source_data_reference: str | None = None
    created_at: datetime = Field(default_factory=utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("dataset_id", "name", "path", "version", mode="before")
    @classmethod
    def required_text_fields_must_be_safe(cls, value: str) -> str:
        return _reject_traversal(str(value), "manifest field")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @field_validator("schema_map")
    @classmethod
    def schema_values_must_be_strings(cls, value: dict[str, Any]) -> dict[str, str]:
        return {str(key): str(schema_value) for key, schema_value in value.items()}

    @property
    def schema_json(self) -> dict[str, str]:
        return self.schema_map


def manifest_to_jsonable(manifest: DatasetManifest) -> dict[str, Any]:
    return to_jsonable(manifest.model_dump(by_alias=True))


def create_dataset_manifest(
    dataset_id: str,
    name: str,
    kind: DatasetKind,
    zone: DataLakeZone | str,
    path: str | Path,
    *,
    format: DatasetFormat = DatasetFormat.PARQUET,
    version: str = "v1",
    partitions: list[DatasetPartition] | None = None,
    row_count: int | None = None,
    schema_json: dict[str, str] | None = None,
    source_data_reference: str | None = None,
    notes: list[str] | None = None,
) -> DatasetManifest:
    return DatasetManifest(
        dataset_id=dataset_id,
        name=name,
        kind=kind,
        zone=normalize_zone(zone),
        format=format,
        version=version,
        path=str(path),
        partitions=partitions or [],
        row_count=row_count,
        schema_json=schema_json or {},
        source_data_reference=source_data_reference,
        notes=notes or [],
    )


def manifest_from_path(
    path: str | Path,
    *,
    dataset_id: str,
    name: str,
    kind: DatasetKind = DatasetKind.UNKNOWN,
    zone: DataLakeZone | str = DataLakeZone.RAW,
    version: str = "v1",
) -> DatasetManifest:
    return create_dataset_manifest(
        dataset_id=dataset_id,
        name=name,
        kind=kind,
        zone=zone,
        path=path,
        version=version,
    )
