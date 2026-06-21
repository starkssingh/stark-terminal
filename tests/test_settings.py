from pydantic import ValidationError
import pytest

from stark_terminal_core.config.settings import Settings


def test_settings_defaults_load() -> None:
    settings = Settings()

    assert settings.app_name == "Stark Terminal"
    assert settings.app_version == "0.1.0"
    assert settings.prompt_number == "16"
    assert settings.api_port == 8000
    assert settings.feature_store_mode == "custom"
    assert settings.market_data_batch_persistence_enabled is True
    assert settings.market_data_batch_persistence_require_validation is True
    assert settings.market_data_batch_persistence_allow_synthetic is True
    assert settings.market_data_batch_persistence_schema_version == "v1"


def test_execution_flags_default_false() -> None:
    settings = Settings()

    assert settings.execution_apis_enabled is False
    assert settings.broker_integrations_enabled is False
    assert settings.live_trading_enabled is False


def test_safe_snapshot_does_not_expose_raw_urls() -> None:
    settings = Settings(
        database_url="postgresql://user:secret@localhost/stark",
        redis_url="redis://localhost:6379",
        clickhouse_url="http://localhost:8123",
        kafka_bootstrap_servers="localhost:9092",
        kafka_sasl_username="user-secret",
        kafka_sasl_password="password-secret",
    )

    snapshot = settings.safe_settings_snapshot()

    assert "database_url" not in snapshot
    assert "redis_url" not in snapshot
    assert "clickhouse_url" not in snapshot
    assert "kafka_bootstrap_servers" not in snapshot
    assert "kafka_sasl_username" not in snapshot
    assert "kafka_sasl_password" not in snapshot
    assert snapshot["database_configured"] is True
    assert snapshot["redis_configured"] is True
    assert snapshot["redis_enabled"] is False
    assert snapshot["cache_key_prefix"] == "stark"
    assert snapshot["cache_environment_namespace"] == "development"
    assert snapshot["cache_use_memory_fallback"] is True
    assert snapshot["redis_streams_enabled"] is False
    assert snapshot["redis_streams_use_memory_fallback"] is True
    assert snapshot["stream_key_prefix"] == "stark"
    assert snapshot["stream_environment_namespace"] == "development"
    assert snapshot["workers_enabled"] is False
    assert snapshot["worker_harness_mode"] == "in_process"
    assert snapshot["worker_allow_background_threads"] is False
    assert snapshot["worker_allow_infinite_loops"] is False
    assert snapshot["instrument_master_mode"] == "local"
    assert snapshot["instrument_master_source"] == "synthetic"
    assert snapshot["allow_external_market_data_calls"] is False
    assert snapshot["allow_provider_network_calls"] is False
    assert snapshot["market_data_contract_schema_version"] == "v1"
    assert snapshot["default_market_data_provider"] == "local_sample"
    assert snapshot["clickhouse_configured"] is True
    assert snapshot["clickhouse_enabled"] is False
    assert snapshot["clickhouse_host"] == "localhost"
    assert snapshot["clickhouse_port"] == 8123
    assert snapshot["clickhouse_database"] == "stark_terminal"
    assert snapshot["clickhouse_use_memory_fallback"] is True
    assert snapshot["warehouse_schema_version"] == "v1"
    assert snapshot["feature_registry_enabled"] is False
    assert snapshot["feature_registry_backend"] == "memory"
    assert snapshot["feature_registry_schema_version"] == "v1"
    assert snapshot["feature_registry_allow_external_backend"] is False
    assert snapshot["feature_registry_require_lineage"] is True
    assert snapshot["feature_registry_require_quality_report"] is True
    assert snapshot["feature_default_freshness_seconds"] == 86400
    assert snapshot["feature_max_allowed_staleness_seconds"] == 604800
    assert snapshot["event_backbone_mode"] == "memory"
    assert snapshot["kafka_enabled"] is False
    assert snapshot["kafka_configured"] is True
    assert snapshot["kafka_client_id"] == "stark-terminal"
    assert snapshot["kafka_security_protocol"] == "PLAINTEXT"
    assert snapshot["kafka_default_partitions"] == 3
    assert snapshot["kafka_replication_factor"] == 1
    assert snapshot["kafka_request_timeout_seconds"] == 5
    assert snapshot["kafka_topic_prefix"] == "stark"
    assert snapshot["kafka_environment_namespace"] == "development"
    assert snapshot["kafka_use_memory_fallback"] is True
    assert snapshot["durable_event_schema_version"] == "v1"
    assert snapshot["data_quality_enabled"] is True
    assert snapshot["data_quality_schema_version"] == "v1"
    assert snapshot["data_quality_default_fail_on_error"] is True
    assert snapshot["data_quality_default_fail_on_warning"] is False
    assert snapshot["data_quality_max_issues_per_report"] == 100
    assert snapshot["data_quality_require_source_reference"] is True
    assert snapshot["data_quality_require_timezone_aware_timestamps"] is True
    assert snapshot["data_quality_allow_synthetic_data"] is True
    assert snapshot["data_quality_external_validation_enabled"] is False
    assert snapshot["synthetic_fixtures_enabled"] is True
    assert snapshot["synthetic_fixture_schema_version"] == "v1"
    assert snapshot["synthetic_fixture_default_seed"] == 42
    assert snapshot["synthetic_fixture_default_bar_count"] == 30
    assert snapshot["synthetic_fixture_default_start_price"] == 100.0
    assert snapshot["synthetic_fixture_default_timeframe"] == "DAILY"
    assert snapshot["synthetic_fixture_allow_disk_writes"] is False
    assert snapshot["synthetic_fixture_output_root"] == "data/synthetic_fixtures"
    assert snapshot["synthetic_fixture_label"] == "synthetic-local-test-only"
    assert snapshot["instrument_persistence_enabled"] is True
    assert snapshot["instrument_persistence_require_validation"] is True
    assert snapshot["instrument_persistence_allow_synthetic_seed"] is True
    assert snapshot["instrument_persistence_schema_version"] == "v1"
    assert snapshot["market_data_batch_persistence_enabled"] is True
    assert snapshot["market_data_batch_persistence_require_validation"] is True
    assert snapshot["market_data_batch_persistence_allow_synthetic"] is True
    assert snapshot["market_data_batch_persistence_schema_version"] == "v1"
    assert "clickhouse_user" not in snapshot
    assert "clickhouse_password" not in snapshot


@pytest.mark.parametrize("api_port", [0, 65536])
def test_api_port_validation(api_port: int) -> None:
    with pytest.raises(ValidationError):
        Settings(api_port=api_port)


def test_execution_flags_fail_closed_when_enabled() -> None:
    with pytest.raises(ValidationError):
        Settings(execution_apis_enabled=True)


def test_market_data_batch_persistence_schema_version_validation() -> None:
    with pytest.raises(ValidationError):
        Settings(market_data_batch_persistence_schema_version="")
