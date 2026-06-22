from stark_terminal_core.config.settings import Settings


def test_safe_settings_snapshot_excludes_raw_sensitive_values() -> None:
    settings = Settings(
        database_url="postgresql://user:database-secret@localhost/stark",
        timescale_database_url="postgresql+psycopg://user:timescale-secret@localhost/stark",
        redis_url="redis://:redis-secret@localhost:6379/0",
        clickhouse_url="http://clickhouse-secret@localhost:8123",
        clickhouse_user="clickhouse-user-secret",
        clickhouse_password="clickhouse-password-secret",
        kafka_bootstrap_servers="kafka-secret:9092",
        kafka_sasl_username="kafka-user-secret",
        kafka_sasl_password="kafka-password-secret",
    )

    snapshot = settings.safe_settings_snapshot()
    snapshot_text = repr(snapshot)

    forbidden_keys = {
        "database_url",
        "timescale_database_url",
        "redis_url",
        "clickhouse_url",
        "clickhouse_user",
        "clickhouse_password",
        "kafka_bootstrap_servers",
        "kafka_sasl_username",
        "kafka_sasl_password",
    }
    forbidden_values = {
        "database-secret",
        "timescale-secret",
        "redis-secret",
        "clickhouse-secret",
        "clickhouse-user-secret",
        "clickhouse-password-secret",
        "kafka-secret",
        "kafka-user-secret",
        "kafka-password-secret",
    }

    assert forbidden_keys.isdisjoint(snapshot)
    for value in forbidden_values:
        assert value not in snapshot_text

    assert snapshot["database_configured"] is True
    assert snapshot["timescale_configured"] is True
    assert snapshot["redis_configured"] is True
    assert snapshot["clickhouse_configured"] is True
    assert snapshot["kafka_configured"] is True
    assert snapshot["data_quality_enabled"] is True
    assert snapshot["data_quality_external_validation_enabled"] is False
    assert snapshot["synthetic_fixtures_enabled"] is True
    assert snapshot["synthetic_fixture_allow_disk_writes"] is False
    assert snapshot["instrument_persistence_enabled"] is True
    assert snapshot["instrument_persistence_require_validation"] is True
    assert snapshot["instrument_persistence_allow_synthetic_seed"] is True
    assert snapshot["instrument_persistence_schema_version"] == "v1"
    assert snapshot["market_data_batch_persistence_enabled"] is True
    assert snapshot["market_data_batch_persistence_require_validation"] is True
    assert snapshot["market_data_batch_persistence_allow_synthetic"] is True
    assert snapshot["market_data_batch_persistence_schema_version"] == "v1"
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
    assert snapshot["local_file_provider_enabled"] is True
    assert snapshot["local_file_provider_schema_version"] == "v1"
    assert snapshot["local_file_provider_allowed_root"] == "data/local_files"
    assert snapshot["local_file_provider_allow_csv"] is True
    assert snapshot["local_file_provider_allow_parquet"] is True
    assert snapshot["local_file_provider_allow_network_paths"] is False
    assert snapshot["local_file_provider_allow_symlinks"] is False
    assert snapshot["local_file_provider_max_rows"] == 10000
    assert snapshot["local_file_provider_allow_real_data_claims"] is False
    assert snapshot["execution_apis_enabled"] is False
    assert snapshot["broker_integrations_enabled"] is False
    assert snapshot["live_trading_enabled"] is False
