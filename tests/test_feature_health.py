from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import FeatureEntityType, FeatureFrequency, FeatureValueType
from stark_terminal_data_platform.features.definitions import create_feature_definition
from stark_terminal_data_platform.features.feature_sets import create_feature_set
from stark_terminal_data_platform.features.health import check_feature_registry_health
from stark_terminal_data_platform.features.registry import StarkFeatureRegistry


def test_default_feature_registry_health_does_not_crash() -> None:
    status = check_feature_registry_health(Settings())

    assert status.enabled is False
    assert status.backend == "memory"
    assert status.feature_store_mode == "custom"
    assert status.status == "disabled"
    assert status.registered_features == 0
    assert status.error is None


def test_registry_health_reports_counts() -> None:
    registry = StarkFeatureRegistry()
    feature = create_feature_definition(
        name="close_return_1d",
        description="Feature placeholder.",
        value_type=FeatureValueType.FLOAT,
        entity_type=FeatureEntityType.INSTRUMENT,
        frequency=FeatureFrequency.DAILY,
        owner="research",
        entity_keys=["instrument_id"],
    )
    registry.register_feature(feature)
    registry.register_feature_set(
        create_feature_set(
            name="instrument_daily_features",
            description="Daily features.",
            features=[feature],
            entity_type=FeatureEntityType.INSTRUMENT,
            owner="research",
        )
    )

    status = check_feature_registry_health(Settings(feature_registry_enabled=True), registry)

    assert status.status == "healthy"
    assert status.registered_features == 1
    assert status.registered_feature_sets == 1


def test_external_backend_allowed_reports_caution() -> None:
    status = check_feature_registry_health(Settings(feature_registry_allow_external_backend=True))

    assert status.status == "caution_external_backend_allowed"
    assert "secret" not in status.model_dump()

