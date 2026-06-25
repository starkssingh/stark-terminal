from pydantic import ValidationError
import pytest

from stark_terminal_core.config.settings import Settings


def test_feature_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.prompt_number == "67"
    assert settings.feature_store_mode == "custom"
    assert settings.feature_registry_enabled is False
    assert settings.feature_registry_backend == "memory"
    assert settings.feature_registry_schema_version == "v1"
    assert settings.feature_registry_allow_external_backend is False
    assert settings.feature_registry_require_lineage is True
    assert settings.feature_registry_require_quality_report is True
    assert settings.feature_default_freshness_seconds == 86400
    assert settings.feature_max_allowed_staleness_seconds == 604800


def test_feature_settings_safe_snapshot_includes_feature_registry_fields() -> None:
    snapshot = Settings().safe_settings_snapshot()

    assert snapshot["feature_store_mode"] == "custom"
    assert snapshot["feature_registry_enabled"] is False
    assert snapshot["feature_registry_backend"] == "memory"
    assert snapshot["feature_registry_schema_version"] == "v1"
    assert snapshot["feature_registry_allow_external_backend"] is False
    assert snapshot["feature_registry_require_lineage"] is True
    assert snapshot["feature_registry_require_quality_report"] is True
    assert snapshot["feature_default_freshness_seconds"] == 86400
    assert snapshot["feature_max_allowed_staleness_seconds"] == 604800


@pytest.mark.parametrize(
    "field,value",
    [
        ("feature_store_mode", "feast"),
        ("feature_registry_backend", "external"),
        ("feature_registry_schema_version", ""),
        ("feature_default_freshness_seconds", 0),
        ("feature_max_allowed_staleness_seconds", 0),
    ],
)
def test_feature_setting_validation_rejects_invalid_values(field: str, value: str | int) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field: value})


def test_feature_staleness_must_cover_freshness() -> None:
    with pytest.raises(ValidationError):
        Settings(feature_default_freshness_seconds=100, feature_max_allowed_staleness_seconds=99)


def test_feature_store_mode_supports_custom_feast_planned_and_disabled() -> None:
    assert Settings(feature_store_mode="custom").feature_store_mode == "custom"
    assert Settings(feature_store_mode="feast_planned").feature_store_mode == "feast_planned"
    assert Settings(feature_store_mode="disabled").feature_store_mode == "disabled"
