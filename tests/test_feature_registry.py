from pydantic import ValidationError
import pytest

from stark_terminal_core.domain.enums import FeatureEntityType, FeatureFrequency, FeatureQualityStatus, FeatureValueType
from stark_terminal_data_platform.features.definitions import create_feature_definition
from stark_terminal_data_platform.features.feature_sets import create_feature_set
from stark_terminal_data_platform.features.lineage import FeatureLineageRecord
from stark_terminal_data_platform.features.quality import create_quality_report
from stark_terminal_data_platform.features.registry import FeatureRegistryError, StarkFeatureRegistry


def make_feature(name: str = "close_return_1d"):
    return create_feature_definition(
        name=name,
        description="Feature placeholder.",
        value_type=FeatureValueType.FLOAT,
        entity_type=FeatureEntityType.INSTRUMENT,
        frequency=FeatureFrequency.DAILY,
        owner="research",
        entity_keys=["instrument_id"],
    )


def test_register_get_list_feature() -> None:
    registry = StarkFeatureRegistry()
    feature = make_feature()

    registry.register_feature(feature)

    assert registry.get_feature("close_return_1d") == feature
    assert registry.list_features() == [feature]


def test_duplicate_feature_rejected_unless_replace() -> None:
    registry = StarkFeatureRegistry()
    feature = make_feature()
    registry.register_feature(feature)

    with pytest.raises(FeatureRegistryError):
        registry.register_feature(feature)

    replacement = make_feature()
    registry.register_feature(replacement, replace=True)
    assert registry.get_feature("close_return_1d") == replacement


def test_register_feature_set_quality_lineage_and_clear() -> None:
    registry = StarkFeatureRegistry()
    feature = make_feature()
    feature_set = create_feature_set(
        name="instrument_daily_features",
        description="Daily features.",
        features=[feature],
        entity_type=FeatureEntityType.INSTRUMENT,
        owner="research",
    )
    quality = create_quality_report(
        report_id="quality-1",
        feature_set_name="instrument_daily_features",
        status=FeatureQualityStatus.WARN,
    )
    lineage = FeatureLineageRecord(
        lineage_id="lineage-1",
        feature_name="close_return_1d",
        upstream_sources=["normalized://bars"],
        transformation_description="Derived from bars.",
    )

    registry.register_feature_set(feature_set)
    registry.register_quality_report(quality)
    registry.register_lineage(lineage)

    assert registry.get_feature_set("instrument_daily_features") == feature_set
    assert registry.list_quality_reports() == [quality]
    assert registry.list_lineage() == [lineage]

    registry.clear()
    assert registry.list_feature_sets() == []
    assert registry.list_quality_reports() == []
    assert registry.list_lineage() == []


def test_registry_instances_do_not_share_state() -> None:
    first = StarkFeatureRegistry()
    second = StarkFeatureRegistry()

    first.register_feature(make_feature())

    assert second.list_features() == []


def test_forbidden_execution_feature_names_rejected() -> None:
    with pytest.raises((ValueError, ValidationError)):
        make_feature("broker_order_signal")
