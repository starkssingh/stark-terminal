from pydantic import ValidationError
import pytest

from stark_terminal_core.domain.enums import FeatureEntityType, FeatureFrequency, FeatureValueType
from stark_terminal_data_platform.features.definitions import create_feature_definition
from stark_terminal_data_platform.features.feature_sets import (
    FeatureSet,
    create_feature_set,
    feature_set_key,
)


def make_feature(name: str, entity_type: FeatureEntityType = FeatureEntityType.INSTRUMENT) :
    return create_feature_definition(
        name=name,
        description=f"{name} placeholder.",
        value_type=FeatureValueType.FLOAT,
        entity_type=entity_type,
        frequency=FeatureFrequency.DAILY,
        owner="research",
        entity_keys=["instrument_id"],
    )


def test_valid_feature_set_creation() -> None:
    feature_set = create_feature_set(
        name="instrument_daily_features",
        description="Daily instrument features.",
        features=[make_feature("close_return_1d")],
        entity_type=FeatureEntityType.INSTRUMENT,
        owner="research",
    )

    assert feature_set.feature_set_id == "instrument_daily_features:v1"
    assert feature_set.created_at.tzinfo is not None


def test_feature_set_key_helper() -> None:
    assert feature_set_key("instrument_daily_features", "v2") == "instrument_daily_features:v2"


def test_feature_set_rejects_empty_features() -> None:
    with pytest.raises(ValidationError):
        FeatureSet(
            feature_set_id="empty:v1",
            name="empty",
            description="empty",
            features=[],
            entity_type=FeatureEntityType.INSTRUMENT,
            owner="research",
        )


def test_feature_set_rejects_duplicate_features() -> None:
    feature = make_feature("close_return_1d")
    with pytest.raises(ValidationError):
        create_feature_set(
            name="dupes",
            description="duplicate set",
            features=[feature, feature],
            entity_type=FeatureEntityType.INSTRUMENT,
            owner="research",
        )


def test_feature_set_rejects_incompatible_entity_types() -> None:
    with pytest.raises(ValidationError):
        create_feature_set(
            name="mixed",
            description="mixed set",
            features=[
                make_feature("instrument_feature", FeatureEntityType.INSTRUMENT),
                make_feature("sector_feature", FeatureEntityType.SECTOR),
            ],
            entity_type=FeatureEntityType.INSTRUMENT,
            owner="research",
        )

