import pytest
from pydantic import ValidationError

from stark_terminal_core.config.settings import Settings


def test_data_quality_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.prompt_number == "54"
    assert settings.data_quality_enabled is True
    assert settings.data_quality_schema_version == "v1"
    assert settings.data_quality_default_fail_on_error is True
    assert settings.data_quality_default_fail_on_warning is False
    assert settings.data_quality_max_issues_per_report == 100
    assert settings.data_quality_require_source_reference is True
    assert settings.data_quality_require_timezone_aware_timestamps is True
    assert settings.data_quality_allow_synthetic_data is True
    assert settings.data_quality_external_validation_enabled is False


def test_data_quality_max_issues_validation_rejects_invalid_values() -> None:
    with pytest.raises(ValidationError):
        Settings(data_quality_max_issues_per_report=0)


def test_data_quality_schema_version_cannot_be_empty() -> None:
    with pytest.raises(ValidationError):
        Settings(data_quality_schema_version=" ")


def test_safe_snapshot_exposes_data_quality_fields_without_secrets() -> None:
    settings = Settings(
        database_url="postgresql://secret",
        redis_url="redis://secret",
        clickhouse_url="http://secret",
        kafka_bootstrap_servers="secret:9092",
        kafka_sasl_username="user",
        kafka_sasl_password="password",
    )

    snapshot = settings.safe_settings_snapshot()

    assert snapshot["data_quality_enabled"] is True
    assert snapshot["data_quality_schema_version"] == "v1"
    assert snapshot["data_quality_external_validation_enabled"] is False
    assert "database_url" not in snapshot
    assert "redis_url" not in snapshot
    assert "clickhouse_url" not in snapshot
    assert "kafka_bootstrap_servers" not in snapshot
    assert "kafka_sasl_username" not in snapshot
    assert "kafka_sasl_password" not in snapshot
