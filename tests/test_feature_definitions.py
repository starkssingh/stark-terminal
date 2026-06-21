from pydantic import ValidationError
import pytest

from stark_terminal_core.domain.enums import (
    FeatureEntityType,
    FeatureFrequency,
    FeatureValueType,
)
from stark_terminal_data_platform.features.definitions import (
    FeatureDefinition,
    FeatureDependency,
    create_feature_definition,
    feature_key,
)


def sample_feature(name: str = "close_return_1d") -> FeatureDefinition:
    return create_feature_definition(
        name=name,
        description="One-day close return placeholder.",
        value_type=FeatureValueType.FLOAT,
        entity_type=FeatureEntityType.INSTRUMENT_TIMEFRAME,
        frequency=FeatureFrequency.DAILY,
        owner="research",
        entity_keys=["instrument_id", "timeframe"],
        source_data_references=["synthetic:test"],
    )


def test_valid_feature_definition_creation() -> None:
    feature = sample_feature()

    assert feature.feature_id == "close_return_1d:v1"
    assert feature.name == "close_return_1d"
    assert feature.freshness_seconds == 86400
    assert feature.max_staleness_seconds == 604800
    assert feature.created_at.tzinfo is not None


def test_feature_key_helper() -> None:
    assert feature_key("volatility_20d", "v2") == "volatility_20d:v2"


@pytest.mark.parametrize(
    "field,value",
    [
        ("feature_id", ""),
        ("name", ""),
        ("version", ""),
        ("description", ""),
        ("owner", ""),
    ],
)
def test_feature_definition_rejects_empty_required_text(field: str, value: str) -> None:
    data = sample_feature().model_dump()
    data[field] = value
    with pytest.raises(ValidationError):
        FeatureDefinition(**data)


def test_feature_definition_rejects_empty_or_unsafe_entity_keys() -> None:
    with pytest.raises(ValidationError):
        FeatureDefinition(**{**sample_feature().model_dump(), "entity_keys": []})
    with pytest.raises(ValidationError):
        FeatureDefinition(**{**sample_feature().model_dump(), "entity_keys": ["instrument id"]})


def test_feature_definition_validates_freshness_and_staleness() -> None:
    with pytest.raises(ValidationError):
        FeatureDefinition(**{**sample_feature().model_dump(), "freshness_seconds": 0})
    with pytest.raises(ValidationError):
        FeatureDefinition(
            **{
                **sample_feature().model_dump(),
                "freshness_seconds": 100,
                "max_staleness_seconds": 99,
            }
        )


def test_feature_dependency_validation() -> None:
    dependency = FeatureDependency(name="source_feature", version="v1")
    assert dependency.name == "source_feature"
    with pytest.raises(ValidationError):
        FeatureDependency(name="")


@pytest.mark.parametrize("name", ["broker_signal", "order_placement_flag", "live_trading_trigger"])
def test_execution_broker_order_feature_names_are_rejected(name: str) -> None:
    with pytest.raises((ValueError, ValidationError)):
        sample_feature(name=name)

