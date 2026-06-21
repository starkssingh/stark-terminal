from datetime import datetime, timezone

from pydantic import ValidationError
import pytest

from stark_terminal_core.domain.enums import (
    FeatureComputationMode,
    FeatureEntityType,
    FeatureValueType,
)
from stark_terminal_core.serialization.json import to_jsonable
from stark_terminal_data_platform.features.values import FeatureEntity, FeatureSnapshot, FeatureValue


def entity(entity_type: FeatureEntityType = FeatureEntityType.INSTRUMENT) -> FeatureEntity:
    return FeatureEntity(entity_type=entity_type, keys={"instrument_id": "NSE:RELIANCE:NSE_EQUITY"})


def feature_value(value: object, value_type: FeatureValueType) -> FeatureValue:
    return FeatureValue(
        feature_name="close_return_1d",
        entity=entity(),
        value=value,
        value_type=value_type,
        event_timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
        source_data_reference="synthetic:test",
    )


def test_valid_feature_entity() -> None:
    item = entity()
    assert item.keys["instrument_id"] == "NSE:RELIANCE:NSE_EQUITY"


def test_feature_entity_rejects_secret_like_keys() -> None:
    with pytest.raises(ValidationError):
        FeatureEntity(entity_type=FeatureEntityType.INSTRUMENT, keys={"api_key": "secret"})


@pytest.mark.parametrize(
    "value,value_type",
    [
        (1.2, FeatureValueType.FLOAT),
        (1, FeatureValueType.INTEGER),
        (True, FeatureValueType.BOOLEAN),
        ("abc", FeatureValueType.STRING),
        ("sector", FeatureValueType.CATEGORY),
        ("2026-01-01T00:00:00Z", FeatureValueType.TIMESTAMP),
        ({"x": [1, 2]}, FeatureValueType.JSON),
    ],
)
def test_feature_value_type_validation_accepts_valid_values(value: object, value_type: FeatureValueType) -> None:
    item = feature_value(value, value_type)
    assert item.value == value
    assert item.created_at.tzinfo is not None


@pytest.mark.parametrize(
    "value,value_type",
    [
        (True, FeatureValueType.INTEGER),
        ("1.2", FeatureValueType.FLOAT),
        (1, FeatureValueType.BOOLEAN),
        (123, FeatureValueType.STRING),
        (object(), FeatureValueType.JSON),
    ],
)
def test_feature_value_type_validation_rejects_invalid_values(value: object, value_type: FeatureValueType) -> None:
    with pytest.raises(ValidationError):
        feature_value(value, value_type)


def test_feature_snapshot_requires_values_and_serializes() -> None:
    value = feature_value(1.2, FeatureValueType.FLOAT)
    snapshot = FeatureSnapshot(
        snapshot_id="snapshot-1",
        feature_set_name="instrument_daily_features",
        values=[value],
        computation_mode=FeatureComputationMode.BATCH,
    )

    assert snapshot.computed_at.tzinfo is not None
    assert to_jsonable(snapshot)["snapshot_id"] == "snapshot-1"

    with pytest.raises(ValidationError):
        FeatureSnapshot(snapshot_id="empty", feature_set_name="instrument_daily_features", values=[])


def test_feature_snapshot_rejects_mixed_entity_types() -> None:
    value_a = feature_value(1.2, FeatureValueType.FLOAT)
    value_b = FeatureValue(
        feature_name="sector_score",
        entity=entity(FeatureEntityType.SECTOR),
        value=1.0,
        value_type=FeatureValueType.FLOAT,
        event_timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    with pytest.raises(ValidationError):
        FeatureSnapshot(snapshot_id="mixed", feature_set_name="mixed", values=[value_a, value_b])

