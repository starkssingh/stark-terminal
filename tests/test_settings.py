from pydantic import ValidationError
import pytest

from stark_terminal_core.config.settings import Settings


def test_settings_defaults_load() -> None:
    settings = Settings()

    assert settings.app_name == "Stark Terminal"
    assert settings.app_version == "0.1.0"
    assert settings.prompt_number == "67"
    assert settings.api_port == 8000
    assert settings.feature_store_mode == "custom"
    assert settings.market_data_batch_persistence_enabled is True
    assert settings.market_data_batch_persistence_require_validation is True
    assert settings.market_data_batch_persistence_allow_synthetic is True
    assert settings.market_data_batch_persistence_schema_version == "v1"
    assert settings.synthetic_ohlcv_storage_enabled is True
    assert settings.synthetic_ohlcv_storage_require_validation is True
    assert settings.synthetic_ohlcv_storage_allow_sqlite is True
    assert settings.synthetic_ohlcv_storage_schema_version == "v1"
    assert settings.synthetic_ohlcv_storage_max_bars_per_batch == 10000
    assert settings.synthetic_ohlcv_export_enabled is True
    assert settings.synthetic_ohlcv_export_require_validation is True
    assert settings.synthetic_ohlcv_export_allow_disk_writes is False
    assert settings.synthetic_ohlcv_export_schema_version == "v1"
    assert settings.synthetic_ohlcv_export_default_zone == "RESEARCH_ARTIFACTS"
    assert settings.synthetic_ohlcv_export_max_rows == 10000
    assert settings.provider_guardrails_enabled is True
    assert settings.provider_implementation_approval_required is True
    assert settings.provider_terms_review_required is True
    assert settings.provider_network_calls_default_allowed is False
    assert settings.provider_scraping_default_allowed is False
    assert settings.provider_credentials_allowed is False
    assert settings.provider_guardrail_schema_version == "v1"
    assert settings.local_sample_provider_enabled is True
    assert settings.local_sample_provider_schema_version == "v1"
    assert settings.local_sample_provider_default_seed == 42
    assert settings.local_sample_provider_default_bar_count == 30
    assert settings.local_sample_provider_default_start_price == 100.0
    assert settings.local_sample_provider_allow_network is False
    assert settings.local_sample_provider_allow_real_data is False
    assert settings.provider_readiness_enabled is True
    assert settings.provider_candidate_selection_schema_version == "v1"
    assert settings.provider_candidate_real_implementation_allowed is False
    assert settings.provider_candidate_network_checks_allowed is False
    assert settings.provider_candidate_scraping_checks_allowed is False
    assert settings.provider_candidate_credentials_allowed is False
    assert settings.provider_candidate_minimum_score_for_design == 70
    assert settings.provider_candidate_minimum_score_for_network_tests == 85
    assert settings.provider_candidate_minimum_score_for_production == 95
    assert settings.local_file_provider_enabled is True
    assert settings.local_file_provider_schema_version == "v1"
    assert settings.local_file_provider_allowed_root == "data/local_files"
    assert settings.local_file_provider_allow_csv is True
    assert settings.local_file_provider_allow_parquet is True
    assert settings.local_file_provider_allow_network_paths is False
    assert settings.local_file_provider_allow_symlinks is False
    assert settings.local_file_provider_max_rows == 10000
    assert settings.local_file_provider_allow_real_data_claims is False
    assert settings.analytics_foundation_enabled is True
    assert settings.analytics_schema_version == "v1"
    assert settings.analytics_allow_real_data is False
    assert settings.analytics_allow_trade_signals is False
    assert settings.analytics_allow_recommendations is False
    assert settings.analytics_require_validated_inputs is True
    assert settings.analytics_require_source_reference is True
    assert settings.analytics_dependency_stage == "contracts_only"


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
    assert snapshot["synthetic_ohlcv_storage_enabled"] is True
    assert snapshot["synthetic_ohlcv_storage_require_validation"] is True
    assert snapshot["synthetic_ohlcv_storage_allow_sqlite"] is True
    assert snapshot["synthetic_ohlcv_storage_schema_version"] == "v1"
    assert snapshot["synthetic_ohlcv_storage_max_bars_per_batch"] == 10000
    assert snapshot["synthetic_ohlcv_export_enabled"] is True
    assert snapshot["synthetic_ohlcv_export_require_validation"] is True
    assert snapshot["synthetic_ohlcv_export_allow_disk_writes"] is False
    assert snapshot["synthetic_ohlcv_export_schema_version"] == "v1"
    assert snapshot["synthetic_ohlcv_export_default_zone"] == "RESEARCH_ARTIFACTS"
    assert snapshot["synthetic_ohlcv_export_max_rows"] == 10000
    assert snapshot["provider_guardrails_enabled"] is True
    assert snapshot["provider_implementation_approval_required"] is True
    assert snapshot["provider_terms_review_required"] is True
    assert snapshot["provider_network_calls_default_allowed"] is False
    assert snapshot["provider_scraping_default_allowed"] is False
    assert snapshot["provider_credentials_allowed"] is False
    assert snapshot["provider_guardrail_schema_version"] == "v1"
    assert snapshot["local_sample_provider_enabled"] is True
    assert snapshot["local_sample_provider_schema_version"] == "v1"
    assert snapshot["local_sample_provider_default_seed"] == 42
    assert snapshot["local_sample_provider_default_bar_count"] == 30
    assert snapshot["local_sample_provider_default_start_price"] == 100.0
    assert snapshot["local_sample_provider_allow_network"] is False
    assert snapshot["local_sample_provider_allow_real_data"] is False
    assert snapshot["provider_readiness_enabled"] is True
    assert snapshot["provider_candidate_selection_schema_version"] == "v1"
    assert snapshot["provider_candidate_real_implementation_allowed"] is False
    assert snapshot["provider_candidate_network_checks_allowed"] is False
    assert snapshot["provider_candidate_scraping_checks_allowed"] is False
    assert snapshot["provider_candidate_credentials_allowed"] is False
    assert snapshot["provider_candidate_minimum_score_for_design"] == 70
    assert snapshot["provider_candidate_minimum_score_for_network_tests"] == 85
    assert snapshot["provider_candidate_minimum_score_for_production"] == 95
    assert snapshot["local_file_provider_enabled"] is True
    assert snapshot["local_file_provider_schema_version"] == "v1"
    assert snapshot["local_file_provider_allowed_root"] == "data/local_files"
    assert snapshot["local_file_provider_allow_csv"] is True
    assert snapshot["local_file_provider_allow_parquet"] is True
    assert snapshot["local_file_provider_allow_network_paths"] is False
    assert snapshot["local_file_provider_allow_symlinks"] is False
    assert snapshot["local_file_provider_max_rows"] == 10000
    assert snapshot["local_file_provider_allow_real_data_claims"] is False
    assert snapshot["analytics_foundation_enabled"] is True
    assert snapshot["analytics_schema_version"] == "v1"
    assert snapshot["analytics_allow_real_data"] is False
    assert snapshot["analytics_allow_trade_signals"] is False
    assert snapshot["analytics_allow_recommendations"] is False
    assert snapshot["analytics_require_validated_inputs"] is True
    assert snapshot["analytics_require_source_reference"] is True
    assert snapshot["analytics_dependency_stage"] == "contracts_only"
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


def test_synthetic_ohlcv_storage_settings_validation() -> None:
    with pytest.raises(ValidationError):
        Settings(synthetic_ohlcv_storage_schema_version="")
    with pytest.raises(ValidationError):
        Settings(synthetic_ohlcv_storage_max_bars_per_batch=0)


def test_synthetic_ohlcv_export_settings_validation() -> None:
    with pytest.raises(ValidationError):
        Settings(synthetic_ohlcv_export_schema_version="")
    with pytest.raises(ValidationError):
        Settings(synthetic_ohlcv_export_default_zone="")
    with pytest.raises(ValidationError):
        Settings(synthetic_ohlcv_export_default_zone="unknown")
    with pytest.raises(ValidationError):
        Settings(synthetic_ohlcv_export_max_rows=0)


def test_provider_guardrail_settings_validation() -> None:
    with pytest.raises(ValidationError):
        Settings(provider_guardrail_schema_version="")
    with pytest.raises(ValidationError):
        Settings(provider_network_calls_default_allowed=True)
    with pytest.raises(ValidationError):
        Settings(provider_scraping_default_allowed=True)
    with pytest.raises(ValidationError):
        Settings(provider_credentials_allowed=True)


def test_local_sample_provider_settings_validation() -> None:
    with pytest.raises(ValidationError):
        Settings(local_sample_provider_schema_version="")
    with pytest.raises(ValidationError):
        Settings(local_sample_provider_default_bar_count=0)
    with pytest.raises(ValidationError):
        Settings(local_sample_provider_default_start_price=0)
    with pytest.raises(ValidationError):
        Settings(local_sample_provider_allow_network=True)
    with pytest.raises(ValidationError):
        Settings(local_sample_provider_allow_real_data=True)


def test_provider_readiness_settings_validation() -> None:
    with pytest.raises(ValidationError):
        Settings(provider_candidate_selection_schema_version="")
    with pytest.raises(ValidationError):
        Settings(provider_candidate_real_implementation_allowed=True)
    with pytest.raises(ValidationError):
        Settings(provider_candidate_network_checks_allowed=True)
    with pytest.raises(ValidationError):
        Settings(provider_candidate_scraping_checks_allowed=True)
    with pytest.raises(ValidationError):
        Settings(provider_candidate_credentials_allowed=True)
    with pytest.raises(ValidationError):
        Settings(provider_candidate_minimum_score_for_design=-1)
    with pytest.raises(ValidationError):
        Settings(
            provider_candidate_minimum_score_for_design=80,
            provider_candidate_minimum_score_for_network_tests=70,
        )
    with pytest.raises(ValidationError):
        Settings(
            provider_candidate_minimum_score_for_network_tests=90,
            provider_candidate_minimum_score_for_production=80,
        )


def test_local_file_provider_settings_validation() -> None:
    with pytest.raises(ValidationError):
        Settings(local_file_provider_schema_version="")
    with pytest.raises(ValidationError):
        Settings(local_file_provider_allowed_root="")
    with pytest.raises(ValidationError):
        Settings(local_file_provider_allow_network_paths=True)
    with pytest.raises(ValidationError):
        Settings(local_file_provider_allow_symlinks=True)
    with pytest.raises(ValidationError):
        Settings(local_file_provider_max_rows=0)
    with pytest.raises(ValidationError):
        Settings(local_file_provider_allow_real_data_claims=True)


def test_analytics_foundation_settings_validation() -> None:
    with pytest.raises(ValidationError):
        Settings(analytics_schema_version="")
    with pytest.raises(ValidationError):
        Settings(analytics_allow_real_data=True)
    with pytest.raises(ValidationError):
        Settings(analytics_allow_trade_signals=True)
    with pytest.raises(ValidationError):
        Settings(analytics_allow_recommendations=True)
    with pytest.raises(ValidationError):
        Settings(analytics_require_validated_inputs=False)
    with pytest.raises(ValidationError):
        Settings(analytics_require_source_reference=False)
    with pytest.raises(ValidationError):
        Settings(analytics_dependency_stage="calculations_enabled")
