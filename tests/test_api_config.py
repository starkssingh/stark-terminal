from fastapi.testclient import TestClient

from stark_terminal_api.main import app


def test_config_endpoint_returns_safe_settings_snapshot() -> None:
    client = TestClient(app)

    response = client.get("/config")

    assert response.status_code == 200
    body = response.json()
    assert body["app_name"] == "Stark Terminal"
    assert body["app_version"] == "0.1.0"
    assert body["stark_env"] == "development"
    assert body["prompt_number"] == "107"
    assert body["timescale_enabled"] is False
    assert body["timescale_create_extension"] is False
    assert body["timescale_create_hypertables"] is False
    assert body["lake_root"] == "data/lake"
    assert body["parquet_compression"] == "zstd"
    assert body["create_lake_dirs"] is False
    assert body["redis_enabled"] is False
    assert body["cache_default_ttl_seconds"] == 300
    assert body["cache_key_prefix"] == "stark"
    assert body["cache_environment_namespace"] == "development"
    assert body["cache_use_memory_fallback"] is True
    assert body["redis_streams_enabled"] is False
    assert body["redis_streams_use_memory_fallback"] is True
    assert body["stream_key_prefix"] == "stark"
    assert body["stream_environment_namespace"] == "development"
    assert body["stream_consumer_group"] == "stark-terminal"
    assert body["event_schema_version"] == "v1"
    assert body["workers_enabled"] is False
    assert body["worker_harness_mode"] == "in_process"
    assert body["worker_default_timeout_seconds"] == 30
    assert body["worker_max_retries"] == 0
    assert body["worker_default_queue"] == "default"
    assert body["worker_schema_version"] == "v1"
    assert body["worker_allow_background_threads"] is False
    assert body["worker_allow_infinite_loops"] is False
    assert body["instrument_master_mode"] == "local"
    assert body["instrument_master_source"] == "synthetic"
    assert body["allow_external_market_data_calls"] is False
    assert body["allow_provider_network_calls"] is False
    assert body["market_data_contract_schema_version"] == "v1"
    assert body["default_market_data_provider"] == "local_sample"
    assert body["default_exchange"] == "NSE"
    assert body["default_market_segment"] == "NSE_EQUITY"
    assert body["clickhouse_enabled"] is False
    assert body["clickhouse_host"] == "localhost"
    assert body["clickhouse_port"] == 8123
    assert body["clickhouse_database"] == "stark_terminal"
    assert body["clickhouse_secure"] is False
    assert body["clickhouse_use_memory_fallback"] is True
    assert body["warehouse_schema_version"] == "v1"
    assert body["feature_registry_enabled"] is False
    assert body["feature_registry_backend"] == "memory"
    assert body["feature_registry_schema_version"] == "v1"
    assert body["feature_registry_allow_external_backend"] is False
    assert body["feature_registry_require_lineage"] is True
    assert body["feature_registry_require_quality_report"] is True
    assert body["feature_default_freshness_seconds"] == 86400
    assert body["feature_max_allowed_staleness_seconds"] == 604800
    assert body["event_backbone_mode"] == "memory"
    assert body["kafka_enabled"] is False
    assert body["kafka_client_id"] == "stark-terminal"
    assert body["kafka_security_protocol"] == "PLAINTEXT"
    assert body["kafka_default_partitions"] == 3
    assert body["kafka_replication_factor"] == 1
    assert body["kafka_request_timeout_seconds"] == 5
    assert body["kafka_topic_prefix"] == "stark"
    assert body["kafka_environment_namespace"] == "development"
    assert body["kafka_use_memory_fallback"] is True
    assert body["durable_event_schema_version"] == "v1"
    assert body["data_quality_enabled"] is True
    assert body["data_quality_schema_version"] == "v1"
    assert body["data_quality_default_fail_on_error"] is True
    assert body["data_quality_default_fail_on_warning"] is False
    assert body["data_quality_max_issues_per_report"] == 100
    assert body["data_quality_require_source_reference"] is True
    assert body["data_quality_require_timezone_aware_timestamps"] is True
    assert body["data_quality_allow_synthetic_data"] is True
    assert body["data_quality_external_validation_enabled"] is False
    assert body["synthetic_fixtures_enabled"] is True
    assert body["synthetic_fixture_schema_version"] == "v1"
    assert body["synthetic_fixture_default_seed"] == 42
    assert body["synthetic_fixture_default_bar_count"] == 30
    assert body["synthetic_fixture_default_start_price"] == 100.0
    assert body["synthetic_fixture_default_timeframe"] == "DAILY"
    assert body["synthetic_fixture_allow_disk_writes"] is False
    assert body["synthetic_fixture_output_root"] == "data/synthetic_fixtures"
    assert body["synthetic_fixture_label"] == "synthetic-local-test-only"
    assert body["instrument_persistence_enabled"] is True
    assert body["instrument_persistence_require_validation"] is True
    assert body["instrument_persistence_allow_synthetic_seed"] is True
    assert body["instrument_persistence_schema_version"] == "v1"
    assert body["market_data_batch_persistence_enabled"] is True
    assert body["market_data_batch_persistence_require_validation"] is True
    assert body["market_data_batch_persistence_allow_synthetic"] is True
    assert body["market_data_batch_persistence_schema_version"] == "v1"
    assert body["provider_guardrails_enabled"] is True
    assert body["provider_implementation_approval_required"] is True
    assert body["provider_terms_review_required"] is True
    assert body["provider_network_calls_default_allowed"] is False
    assert body["provider_scraping_default_allowed"] is False
    assert body["provider_credentials_allowed"] is False
    assert body["provider_guardrail_schema_version"] == "v1"
    assert body["local_sample_provider_enabled"] is True
    assert body["local_sample_provider_schema_version"] == "v1"
    assert body["local_sample_provider_default_seed"] == 42
    assert body["local_sample_provider_default_bar_count"] == 30
    assert body["local_sample_provider_default_start_price"] == 100.0
    assert body["local_sample_provider_allow_network"] is False
    assert body["local_sample_provider_allow_real_data"] is False
    assert body["local_file_provider_enabled"] is True
    assert body["local_file_provider_schema_version"] == "v1"
    assert body["local_file_provider_allowed_root"] == "data/local_files"
    assert body["local_file_provider_allow_csv"] is True
    assert body["local_file_provider_allow_parquet"] is True
    assert body["local_file_provider_allow_network_paths"] is False
    assert body["local_file_provider_allow_symlinks"] is False
    assert body["local_file_provider_max_rows"] == 10000
    assert body["local_file_provider_allow_real_data_claims"] is False
    assert body["analytics_foundation_enabled"] is True
    assert body["analytics_schema_version"] == "v1"
    assert body["analytics_allow_real_data"] is False
    assert body["analytics_allow_trade_signals"] is False
    assert body["analytics_allow_recommendations"] is False
    assert body["analytics_require_validated_inputs"] is True
    assert body["analytics_require_source_reference"] is True
    assert body["analytics_dependency_stage"] == "contracts_only"
    assert body["volatility_analytics_enabled"] is True
    assert body["volatility_analytics_schema_version"] == "v1"
    assert body["volatility_analytics_allow_real_data"] is False
    assert body["volatility_analytics_allow_trade_signals"] is False
    assert body["volatility_analytics_allow_recommendations"] is False
    assert body["volatility_analytics_allow_decision_objects"] is False
    assert body["volatility_analytics_default_stddev_method"] == "sample"
    assert body["volatility_analytics_allow_annualization"] is True
    assert body["drawdown_analytics_enabled"] is True
    assert body["drawdown_analytics_require_positive_values"] is True
    assert body["drawdown_analytics_allow_signal_labels"] is False
    assert body["regime_feature_preparation_enabled"] is True
    assert body["regime_feature_preparation_schema_version"] == "v1"
    assert body["regime_feature_preparation_allow_real_data"] is False
    assert body["regime_feature_preparation_allow_feature_computation"] is False
    assert body["regime_feature_preparation_allow_feature_registry_writes"] is False
    assert body["regime_feature_preparation_allow_classification"] is False
    assert body["regime_feature_preparation_allow_trade_signals"] is False
    assert body["regime_feature_preparation_allow_recommendations"] is False
    assert body["regime_feature_preparation_allow_decision_objects"] is False
    assert body["regime_feature_preparation_require_provenance"] is True
    assert body["regime_feature_preparation_require_evidence_mapping"] is True
    assert body["regime_feature_preparation_dependency_stage"] == "contracts_only"
    assert body["api_host"] == "127.0.0.1"
    assert body["api_port"] == 8000
    assert body["feature_store_mode"] == "custom"
    assert body["execution_apis_enabled"] is False
    assert body["broker_integrations_enabled"] is False
    assert body["live_trading_enabled"] is False


def test_config_endpoint_does_not_expose_raw_url_keys() -> None:
    client = TestClient(app)

    body = client.get("/config").json()

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
        "timescale_database_url",
    }
    assert forbidden_keys.isdisjoint(body)
    assert "database_configured" in body
    assert "redis_configured" in body
    assert "redis_enabled" in body
    assert "redis_streams_enabled" in body
    assert "workers_enabled" in body
    assert "instrument_master_mode" in body
    assert "allow_provider_network_calls" in body
    assert "clickhouse_configured" in body
    assert "clickhouse_enabled" in body
    assert "feature_registry_enabled" in body
    assert "kafka_configured" in body
    assert "event_backbone_mode" in body
    assert "data_quality_enabled" in body
    assert "synthetic_fixtures_enabled" in body
    assert "instrument_persistence_enabled" in body
    assert "market_data_batch_persistence_enabled" in body
    assert "provider_guardrails_enabled" in body
    assert "local_sample_provider_enabled" in body
    assert "local_file_provider_enabled" in body
    assert "analytics_foundation_enabled" in body
