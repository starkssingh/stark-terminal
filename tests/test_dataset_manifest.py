from pathlib import Path

import pytest
from pydantic import ValidationError

from stark_terminal_core.domain.enums import DataLakeZone, DatasetFormat, DatasetKind
from stark_terminal_data_platform.lake.manifest import (
    DatasetManifest,
    DatasetPartition,
    create_dataset_manifest,
    manifest_from_path,
    manifest_to_jsonable,
)
from stark_terminal_data_platform.lake.registry import DatasetRegistry


def test_valid_manifest_creation() -> None:
    manifest = DatasetManifest(
        dataset_id="ds_ohlcv_v1",
        name="ohlcv_sample",
        kind=DatasetKind.OHLCV,
        zone=DataLakeZone.RAW,
        path="raw/ohlcv_sample/v1",
        row_count=2,
        schema_json={"symbol": "str"},
        partitions=[DatasetPartition(key="exchange", value="NSE")],
    )

    assert manifest.format == DatasetFormat.PARQUET
    assert manifest.created_at.tzinfo is not None


def test_manifest_rejects_negative_row_count() -> None:
    with pytest.raises(ValidationError):
        DatasetManifest(
            dataset_id="bad",
            name="bad",
            kind=DatasetKind.UNKNOWN,
            zone=DataLakeZone.RAW,
            path="raw/bad",
            row_count=-1,
        )


def test_manifest_rejects_traversal_path() -> None:
    with pytest.raises(ValidationError):
        DatasetManifest(
            dataset_id="bad",
            name="bad",
            kind=DatasetKind.UNKNOWN,
            zone=DataLakeZone.RAW,
            path="../bad",
        )


def test_manifest_serialization_and_helpers_work() -> None:
    manifest = create_dataset_manifest(
        dataset_id="ds_1",
        name="sample",
        kind=DatasetKind.FEATURE_SET,
        zone="feature_ready",
        path=Path("feature_ready/sample/v1"),
        row_count=10,
        schema_json={"feature": "float64"},
    )
    from_path = manifest_from_path(
        "raw/source/v1",
        dataset_id="ds_2",
        name="source",
        kind=DatasetKind.OHLCV,
    )

    payload = manifest_to_jsonable(manifest)

    assert payload["zone"] == "FEATURE_READY"
    assert payload["schema_json"] == {"feature": "float64"}
    assert from_path.name == "source"


def test_dataset_registry_placeholder_registers_and_lists() -> None:
    registry = DatasetRegistry()
    manifest = create_dataset_manifest(
        dataset_id="ds_registry",
        name="registry_sample",
        kind=DatasetKind.RESEARCH_ARTIFACT,
        zone=DataLakeZone.RESEARCH_ARTIFACTS,
        path="research_artifacts/registry_sample",
    )

    registry.register(manifest)

    assert registry.get("ds_registry") == manifest
    assert registry.list_manifests() == [manifest]
