from datetime import datetime, timezone

from pydantic import ValidationError
import pytest

from stark_terminal_core.domain.enums import FixtureKind, Timeframe
from stark_terminal_data_platform.fixtures.manifests import (
    FixtureManifest,
    create_fixture_manifest,
    fixture_manifest_to_jsonable,
)


def test_valid_fixture_manifest_creation() -> None:
    manifest = create_fixture_manifest(
        "synthetic_ohlcv_reliance",
        "Synthetic OHLCV RELIANCE",
        FixtureKind.SYNTHETIC_OHLCV,
        instrument_key="NSE:RELIANCE:NSE_EQUITY",
        row_count=30,
        timeframe=Timeframe.DAILY,
        start_timestamp=datetime(2024, 1, 1, tzinfo=timezone.utc),
        end_timestamp=datetime(2024, 1, 31, tzinfo=timezone.utc),
        seed=42,
    )

    assert manifest.fixture_id == "synthetic_ohlcv_reliance"
    assert manifest.label == "synthetic-local-test-only"
    assert manifest.created_at.tzinfo is not None


@pytest.mark.parametrize("field", ["fixture_id", "name", "label", "schema_version"])
def test_fixture_manifest_empty_fields_rejected(field: str) -> None:
    payload = {
        "fixture_id": "fixture",
        "name": "Synthetic Fixture",
        "kind": FixtureKind.SYNTHETIC_OHLCV,
        "label": "synthetic-local-test-only",
        "schema_version": "v1",
    }
    payload[field] = ""

    with pytest.raises(ValidationError):
        FixtureManifest(**payload)


def test_fixture_manifest_rejects_negative_row_count() -> None:
    with pytest.raises(ValidationError):
        create_fixture_manifest("fixture", "Synthetic", FixtureKind.SYNTHETIC_OHLCV, row_count=-1)


def test_fixture_manifest_rejects_invalid_time_range() -> None:
    with pytest.raises(ValidationError):
        create_fixture_manifest(
            "fixture",
            "Synthetic",
            FixtureKind.SYNTHETIC_OHLCV,
            start_timestamp=datetime(2024, 1, 2, tzinfo=timezone.utc),
            end_timestamp=datetime(2024, 1, 1, tzinfo=timezone.utc),
        )


def test_fixture_manifest_label_requires_synthetic_local_test_semantics() -> None:
    with pytest.raises(ValidationError):
        create_fixture_manifest("fixture", "Synthetic", FixtureKind.SYNTHETIC_OHLCV, label="sample")


def test_fixture_manifest_source_reference_cannot_imply_live_provider_data() -> None:
    with pytest.raises(ValidationError):
        create_fixture_manifest(
            "fixture",
            "Synthetic",
            FixtureKind.SYNTHETIC_OHLCV,
            source_data_reference="live-provider-feed",
        )


def test_fixture_manifest_serialization() -> None:
    manifest = create_fixture_manifest("fixture", "Synthetic Fixture", FixtureKind.SYNTHETIC_OHLCV)

    serialized = fixture_manifest_to_jsonable(manifest)

    assert serialized["fixture_id"] == "fixture"
    assert serialized["kind"] == "SYNTHETIC_OHLCV"
