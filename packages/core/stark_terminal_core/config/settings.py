from __future__ import annotations

from functools import lru_cache
import re
from typing import Any

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    stark_env: str = "development"
    app_name: str = "Stark Terminal"
    app_version: str = "0.1.0"
    prompt_number: str = "25"

    api_host: str = "127.0.0.1"
    api_port: int = Field(default=8000, ge=1, le=65535)
    api_reload: bool = False

    database_url: str | None = None
    database_echo: bool = False
    database_pool_size: int = Field(default=5, gt=0)
    database_max_overflow: int = Field(default=10, ge=0)
    database_pool_pre_ping: bool = True
    database_connect_timeout_seconds: int = Field(default=10, gt=0)
    timescale_database_url: str | None = None
    timescale_enabled: bool = False
    timescale_extension_name: str = "timescaledb"
    timescale_create_extension: bool = False
    timescale_create_hypertables: bool = False
    timescale_chunk_interval: str = "7 days"
    redis_url: str | None = None
    redis_enabled: bool = False
    redis_socket_timeout_seconds: float = Field(default=2.0, gt=0)
    redis_connect_timeout_seconds: float = Field(default=2.0, gt=0)
    redis_health_check_interval_seconds: int = Field(default=30, gt=0)
    cache_default_ttl_seconds: int = Field(default=300, gt=0)
    cache_key_prefix: str = "stark"
    cache_environment_namespace: str = "development"
    cache_use_memory_fallback: bool = True
    redis_streams_enabled: bool = False
    redis_streams_use_memory_fallback: bool = True
    stream_key_prefix: str = "stark"
    stream_environment_namespace: str = "development"
    stream_consumer_group: str = "stark-terminal"
    stream_read_count: int = Field(default=10, gt=0)
    stream_block_ms: int = Field(default=1000, ge=0)
    stream_max_len: int = Field(default=10000, gt=0)
    stream_approximate_trim: bool = True
    event_schema_version: str = "v1"
    workers_enabled: bool = False
    worker_harness_mode: str = "in_process"
    worker_default_timeout_seconds: int = Field(default=30, gt=0)
    worker_max_retries: int = Field(default=0, ge=0)
    worker_default_queue: str = "default"
    worker_schema_version: str = "v1"
    worker_allow_background_threads: bool = False
    worker_allow_infinite_loops: bool = False
    instrument_master_mode: str = "local"
    instrument_master_source: str = "synthetic"
    allow_external_market_data_calls: bool = False
    allow_provider_network_calls: bool = False
    market_data_contract_schema_version: str = "v1"
    default_market_data_provider: str = "local_sample"
    default_exchange: str = "NSE"
    default_market_segment: str = "NSE_EQUITY"
    clickhouse_url: str | None = None
    clickhouse_enabled: bool = False
    clickhouse_host: str = "localhost"
    clickhouse_port: int = Field(default=8123, ge=1, le=65535)
    clickhouse_database: str = "stark_terminal"
    clickhouse_user: str | None = None
    clickhouse_password: str | None = None
    clickhouse_secure: bool = False
    clickhouse_connect_timeout_seconds: int = Field(default=5, gt=0)
    clickhouse_send_receive_timeout_seconds: int = Field(default=30, gt=0)
    clickhouse_use_memory_fallback: bool = True
    warehouse_schema_version: str = "v1"
    event_backbone_mode: str = "memory"
    kafka_enabled: bool = False
    kafka_bootstrap_servers: str | None = None
    kafka_client_id: str = "stark-terminal"
    kafka_security_protocol: str = "PLAINTEXT"
    kafka_sasl_username: str | None = None
    kafka_sasl_password: str | None = None
    kafka_default_partitions: int = Field(default=3, gt=0)
    kafka_replication_factor: int = Field(default=1, gt=0)
    kafka_request_timeout_seconds: int = Field(default=5, gt=0)
    kafka_topic_prefix: str = "stark"
    kafka_environment_namespace: str = "development"
    kafka_use_memory_fallback: bool = True
    durable_event_schema_version: str = "v1"
    data_quality_enabled: bool = True
    data_quality_schema_version: str = "v1"
    data_quality_default_fail_on_error: bool = True
    data_quality_default_fail_on_warning: bool = False
    data_quality_max_issues_per_report: int = Field(default=100, gt=0)
    data_quality_require_source_reference: bool = True
    data_quality_require_timezone_aware_timestamps: bool = True
    data_quality_allow_synthetic_data: bool = True
    data_quality_external_validation_enabled: bool = False
    synthetic_fixtures_enabled: bool = True
    synthetic_fixture_schema_version: str = "v1"
    synthetic_fixture_default_seed: int = 42
    synthetic_fixture_default_bar_count: int = Field(default=30, gt=0)
    synthetic_fixture_default_start_price: float = Field(default=100.0, gt=0)
    synthetic_fixture_default_timeframe: str = "DAILY"
    synthetic_fixture_allow_disk_writes: bool = False
    synthetic_fixture_output_root: str = "data/synthetic_fixtures"
    synthetic_fixture_label: str = "synthetic-local-test-only"
    instrument_persistence_enabled: bool = True
    instrument_persistence_require_validation: bool = True
    instrument_persistence_allow_synthetic_seed: bool = True
    instrument_persistence_schema_version: str = "v1"
    market_data_batch_persistence_enabled: bool = True
    market_data_batch_persistence_require_validation: bool = True
    market_data_batch_persistence_allow_synthetic: bool = True
    market_data_batch_persistence_schema_version: str = "v1"
    synthetic_ohlcv_storage_enabled: bool = True
    synthetic_ohlcv_storage_require_validation: bool = True
    synthetic_ohlcv_storage_allow_sqlite: bool = True
    synthetic_ohlcv_storage_schema_version: str = "v1"
    synthetic_ohlcv_storage_max_bars_per_batch: int = Field(default=10000, gt=0)
    synthetic_ohlcv_export_enabled: bool = True
    synthetic_ohlcv_export_require_validation: bool = True
    synthetic_ohlcv_export_allow_disk_writes: bool = False
    synthetic_ohlcv_export_schema_version: str = "v1"
    synthetic_ohlcv_export_default_zone: str = "RESEARCH_ARTIFACTS"
    synthetic_ohlcv_export_max_rows: int = Field(default=10000, gt=0)
    provider_guardrails_enabled: bool = True
    provider_implementation_approval_required: bool = True
    provider_terms_review_required: bool = True
    provider_network_calls_default_allowed: bool = False
    provider_scraping_default_allowed: bool = False
    provider_credentials_allowed: bool = False
    provider_guardrail_schema_version: str = "v1"
    local_sample_provider_enabled: bool = True
    local_sample_provider_schema_version: str = "v1"
    local_sample_provider_default_seed: int = 42
    local_sample_provider_default_bar_count: int = Field(default=30, gt=0)
    local_sample_provider_default_start_price: float = Field(default=100.0, gt=0)
    local_sample_provider_allow_network: bool = False
    local_sample_provider_allow_real_data: bool = False
    provider_readiness_enabled: bool = True
    provider_candidate_selection_schema_version: str = "v1"
    provider_candidate_real_implementation_allowed: bool = False
    provider_candidate_network_checks_allowed: bool = False
    provider_candidate_scraping_checks_allowed: bool = False
    provider_candidate_credentials_allowed: bool = False
    provider_candidate_minimum_score_for_design: int = Field(default=70, ge=0, le=100)
    provider_candidate_minimum_score_for_network_tests: int = Field(default=85, ge=0, le=100)
    provider_candidate_minimum_score_for_production: int = Field(default=95, ge=0, le=100)
    local_file_provider_enabled: bool = True
    local_file_provider_schema_version: str = "v1"
    local_file_provider_allowed_root: str = "data/local_files"
    local_file_provider_allow_csv: bool = True
    local_file_provider_allow_parquet: bool = True
    local_file_provider_allow_network_paths: bool = False
    local_file_provider_allow_symlinks: bool = False
    local_file_provider_max_rows: int = Field(default=10000, gt=0)
    local_file_provider_allow_real_data_claims: bool = False

    feature_store_mode: str = "custom"
    feature_registry_enabled: bool = False
    feature_registry_backend: str = "memory"
    feature_registry_schema_version: str = "v1"
    feature_registry_allow_external_backend: bool = False
    feature_registry_require_lineage: bool = True
    feature_registry_require_quality_report: bool = True
    feature_default_freshness_seconds: int = Field(default=86400, gt=0)
    feature_max_allowed_staleness_seconds: int = Field(default=604800, gt=0)

    execution_apis_enabled: bool = False
    broker_integrations_enabled: bool = False
    live_trading_enabled: bool = False

    data_root: str = "data"
    parquet_root: str = "data/parquet"
    research_artifacts_root: str = "data/research_artifacts"
    lake_root: str = "data/lake"
    duckdb_database_path: str = "data/lake/stark_terminal.duckdb"
    duckdb_read_only: bool = False
    parquet_compression: str = "zstd"
    create_lake_dirs: bool = False

    @field_validator("app_version")
    @classmethod
    def app_version_must_be_non_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("app_version cannot be empty")
        return value

    @field_validator("feature_store_mode")
    @classmethod
    def feature_store_mode_must_be_supported(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in {"custom", "feast_planned", "disabled"}:
            raise ValueError("feature_store_mode must be custom, feast_planned, or disabled")
        return normalized

    @field_validator("feature_registry_backend")
    @classmethod
    def feature_registry_backend_must_be_supported(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in {"memory", "postgres_planned", "feast_planned"}:
            raise ValueError("feature_registry_backend must be memory, postgres_planned, or feast_planned")
        return normalized

    @field_validator("feature_registry_schema_version")
    @classmethod
    def feature_registry_schema_version_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("feature_registry_schema_version cannot be empty")
        return normalized

    @field_validator("timescale_extension_name", "timescale_chunk_interval")
    @classmethod
    def timescale_text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("TimescaleDB text settings cannot be empty")
        return normalized

    @field_validator(
        "data_root",
        "parquet_root",
        "research_artifacts_root",
        "lake_root",
        "duckdb_database_path",
    )
    @classmethod
    def path_settings_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("path settings cannot be empty")
        return normalized

    @field_validator("parquet_compression")
    @classmethod
    def parquet_compression_must_be_supported(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in {"zstd", "snappy", "gzip", "none"}:
            raise ValueError("parquet_compression must be zstd, snappy, gzip, or none")
        return normalized

    @field_validator(
        "cache_key_prefix",
        "cache_environment_namespace",
        "stream_key_prefix",
        "stream_environment_namespace",
        "stream_consumer_group",
        "kafka_topic_prefix",
        "kafka_environment_namespace",
    )
    @classmethod
    def namespace_settings_must_be_safe_slugs(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not normalized:
            raise ValueError("namespace settings cannot be empty")
        if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", normalized):
            raise ValueError("namespace settings must be safe slug-like strings")
        return normalized

    @field_validator("event_schema_version")
    @classmethod
    def event_schema_version_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("event_schema_version cannot be empty")
        return normalized

    @field_validator("event_backbone_mode")
    @classmethod
    def event_backbone_mode_must_be_supported(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in {"memory", "kafka", "redpanda", "disabled"}:
            raise ValueError("event_backbone_mode must be memory, kafka, redpanda, or disabled")
        return normalized

    @field_validator("kafka_client_id", "kafka_security_protocol", "durable_event_schema_version")
    @classmethod
    def kafka_text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Kafka/Event Backbone text settings cannot be empty")
        return normalized

    @field_validator("data_quality_schema_version")
    @classmethod
    def data_quality_schema_version_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("data_quality_schema_version cannot be empty")
        return normalized

    @field_validator(
        "synthetic_fixture_schema_version",
        "synthetic_fixture_default_timeframe",
        "synthetic_fixture_output_root",
        "synthetic_fixture_label",
    )
    @classmethod
    def synthetic_fixture_text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("synthetic fixture text settings cannot be empty")
        return normalized

    @field_validator(
        "instrument_persistence_schema_version",
        "market_data_batch_persistence_schema_version",
        "synthetic_ohlcv_storage_schema_version",
        "synthetic_ohlcv_export_schema_version",
        "synthetic_ohlcv_export_default_zone",
        "provider_guardrail_schema_version",
        "local_sample_provider_schema_version",
        "provider_candidate_selection_schema_version",
        "local_file_provider_schema_version",
        "local_file_provider_allowed_root",
    )
    @classmethod
    def persistence_schema_version_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("persistence/export text settings cannot be empty")
        return normalized

    @field_validator("synthetic_ohlcv_export_default_zone")
    @classmethod
    def synthetic_ohlcv_export_default_zone_must_be_supported(cls, value: str) -> str:
        normalized = value.strip().upper().replace("-", "_")
        if normalized not in {
            "RAW",
            "CLEANED",
            "NORMALIZED",
            "FEATURE_READY",
            "BACKTEST_READY",
            "RESEARCH_ARTIFACTS",
        }:
            raise ValueError("synthetic_ohlcv_export_default_zone must be a supported data lake zone")
        return normalized

    @field_validator("worker_harness_mode")
    @classmethod
    def worker_harness_mode_must_be_supported(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in {"in_process", "disabled"}:
            raise ValueError("worker_harness_mode must be 'in_process' or 'disabled'")
        return normalized

    @field_validator("worker_default_queue", "worker_schema_version")
    @classmethod
    def worker_text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("worker text settings cannot be empty")
        return normalized

    @field_validator("instrument_master_mode")
    @classmethod
    def instrument_master_mode_must_be_supported(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in {"local", "disabled", "external_planned"}:
            raise ValueError("instrument_master_mode must be local, disabled, or external_planned")
        return normalized

    @field_validator(
        "instrument_master_source",
        "market_data_contract_schema_version",
        "default_market_data_provider",
        "default_exchange",
        "default_market_segment",
    )
    @classmethod
    def instrument_text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("instrument/provider text settings cannot be empty")
        return normalized

    @field_validator("clickhouse_host", "clickhouse_database", "warehouse_schema_version")
    @classmethod
    def clickhouse_text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("ClickHouse text settings cannot be empty")
        return normalized

    @model_validator(mode="after")
    def execution_flags_must_remain_disabled(self) -> Settings:
        if self.execution_apis_enabled:
            raise ValueError("execution APIs are forbidden in Prompt 25")
        if self.broker_integrations_enabled:
            raise ValueError("broker integrations are forbidden in Prompt 25")
        if self.live_trading_enabled:
            raise ValueError("live trading is forbidden in Prompt 25")
        if self.allow_external_market_data_calls:
            raise ValueError("external market data calls are forbidden in Prompt 25")
        if self.allow_provider_network_calls:
            raise ValueError("provider network calls are forbidden in Prompt 25")
        if self.provider_network_calls_default_allowed:
            raise ValueError("provider network calls are disabled by default in Prompt 25")
        if self.provider_scraping_default_allowed:
            raise ValueError("provider scraping is disabled by default in Prompt 25")
        if self.provider_credentials_allowed:
            raise ValueError("provider credentials are forbidden in Prompt 25")
        if self.local_sample_provider_allow_network:
            raise ValueError("local sample provider network calls are forbidden in Prompt 25")
        if self.local_sample_provider_allow_real_data:
            raise ValueError("local sample provider real data is forbidden in Prompt 25")
        if self.provider_candidate_real_implementation_allowed:
            raise ValueError("real provider implementation is forbidden in Prompt 25")
        if self.provider_candidate_network_checks_allowed:
            raise ValueError("provider candidate network checks are forbidden in Prompt 25")
        if self.provider_candidate_scraping_checks_allowed:
            raise ValueError("provider candidate scraping checks are forbidden in Prompt 25")
        if self.provider_candidate_credentials_allowed:
            raise ValueError("provider candidate credentials are forbidden in Prompt 25")
        if self.local_file_provider_allow_network_paths:
            raise ValueError("local file provider network paths are forbidden in Prompt 25")
        if self.local_file_provider_allow_symlinks:
            raise ValueError("local file provider symlinks are forbidden in Prompt 25")
        if self.local_file_provider_allow_real_data_claims:
            raise ValueError("local file provider real data claims are forbidden in Prompt 25")
        if (
            self.provider_candidate_minimum_score_for_network_tests
            < self.provider_candidate_minimum_score_for_design
        ):
            raise ValueError("network test threshold must be >= design threshold")
        if (
            self.provider_candidate_minimum_score_for_production
            < self.provider_candidate_minimum_score_for_network_tests
        ):
            raise ValueError("production threshold must be >= network test threshold")
        if self.feature_max_allowed_staleness_seconds < self.feature_default_freshness_seconds:
            raise ValueError("feature_max_allowed_staleness_seconds must be >= feature_default_freshness_seconds")
        return self

    def safe_settings_snapshot(self) -> dict[str, Any]:
        return {
            "app_name": self.app_name,
            "app_version": self.app_version,
            "stark_env": self.stark_env,
            "prompt_number": self.prompt_number,
            "api_host": self.api_host,
            "api_port": self.api_port,
            "feature_store_mode": self.feature_store_mode,
            "execution_apis_enabled": self.execution_apis_enabled,
            "broker_integrations_enabled": self.broker_integrations_enabled,
            "live_trading_enabled": self.live_trading_enabled,
            "data_root": self.data_root,
            "parquet_root": self.parquet_root,
            "research_artifacts_root": self.research_artifacts_root,
            "lake_root": self.lake_root,
            "duckdb_database_configured": bool(self.duckdb_database_path),
            "parquet_compression": self.parquet_compression,
            "create_lake_dirs": self.create_lake_dirs,
            "database_configured": bool(self.database_url),
            "timescale_configured": bool(self.timescale_database_url),
            "timescale_enabled": self.timescale_enabled,
            "timescale_create_extension": self.timescale_create_extension,
            "timescale_create_hypertables": self.timescale_create_hypertables,
            "redis_configured": bool(self.redis_url),
            "redis_enabled": self.redis_enabled,
            "cache_default_ttl_seconds": self.cache_default_ttl_seconds,
            "cache_key_prefix": self.cache_key_prefix,
            "cache_environment_namespace": self.cache_environment_namespace,
            "cache_use_memory_fallback": self.cache_use_memory_fallback,
            "redis_streams_enabled": self.redis_streams_enabled,
            "redis_streams_use_memory_fallback": self.redis_streams_use_memory_fallback,
            "stream_key_prefix": self.stream_key_prefix,
            "stream_environment_namespace": self.stream_environment_namespace,
            "stream_consumer_group": self.stream_consumer_group,
            "stream_read_count": self.stream_read_count,
            "stream_block_ms": self.stream_block_ms,
            "stream_max_len": self.stream_max_len,
            "stream_approximate_trim": self.stream_approximate_trim,
            "event_schema_version": self.event_schema_version,
            "workers_enabled": self.workers_enabled,
            "worker_harness_mode": self.worker_harness_mode,
            "worker_default_timeout_seconds": self.worker_default_timeout_seconds,
            "worker_max_retries": self.worker_max_retries,
            "worker_default_queue": self.worker_default_queue,
            "worker_schema_version": self.worker_schema_version,
            "worker_allow_background_threads": self.worker_allow_background_threads,
            "worker_allow_infinite_loops": self.worker_allow_infinite_loops,
            "instrument_master_mode": self.instrument_master_mode,
            "instrument_master_source": self.instrument_master_source,
            "allow_external_market_data_calls": self.allow_external_market_data_calls,
            "allow_provider_network_calls": self.allow_provider_network_calls,
            "market_data_contract_schema_version": self.market_data_contract_schema_version,
            "default_market_data_provider": self.default_market_data_provider,
            "default_exchange": self.default_exchange,
            "default_market_segment": self.default_market_segment,
            "clickhouse_configured": bool(self.clickhouse_url),
            "clickhouse_enabled": self.clickhouse_enabled,
            "clickhouse_host": self.clickhouse_host,
            "clickhouse_port": self.clickhouse_port,
            "clickhouse_database": self.clickhouse_database,
            "clickhouse_secure": self.clickhouse_secure,
            "clickhouse_use_memory_fallback": self.clickhouse_use_memory_fallback,
            "warehouse_schema_version": self.warehouse_schema_version,
            "feature_registry_enabled": self.feature_registry_enabled,
            "feature_registry_backend": self.feature_registry_backend,
            "feature_registry_schema_version": self.feature_registry_schema_version,
            "feature_registry_allow_external_backend": self.feature_registry_allow_external_backend,
            "feature_registry_require_lineage": self.feature_registry_require_lineage,
            "feature_registry_require_quality_report": self.feature_registry_require_quality_report,
            "feature_default_freshness_seconds": self.feature_default_freshness_seconds,
            "feature_max_allowed_staleness_seconds": self.feature_max_allowed_staleness_seconds,
            "event_backbone_mode": self.event_backbone_mode,
            "kafka_enabled": self.kafka_enabled,
            "kafka_configured": bool(self.kafka_bootstrap_servers),
            "kafka_client_id": self.kafka_client_id,
            "kafka_security_protocol": self.kafka_security_protocol,
            "kafka_default_partitions": self.kafka_default_partitions,
            "kafka_replication_factor": self.kafka_replication_factor,
            "kafka_request_timeout_seconds": self.kafka_request_timeout_seconds,
            "kafka_topic_prefix": self.kafka_topic_prefix,
            "kafka_environment_namespace": self.kafka_environment_namespace,
            "kafka_use_memory_fallback": self.kafka_use_memory_fallback,
            "durable_event_schema_version": self.durable_event_schema_version,
            "data_quality_enabled": self.data_quality_enabled,
            "data_quality_schema_version": self.data_quality_schema_version,
            "data_quality_default_fail_on_error": self.data_quality_default_fail_on_error,
            "data_quality_default_fail_on_warning": self.data_quality_default_fail_on_warning,
            "data_quality_max_issues_per_report": self.data_quality_max_issues_per_report,
            "data_quality_require_source_reference": self.data_quality_require_source_reference,
            "data_quality_require_timezone_aware_timestamps": self.data_quality_require_timezone_aware_timestamps,
            "data_quality_allow_synthetic_data": self.data_quality_allow_synthetic_data,
            "data_quality_external_validation_enabled": self.data_quality_external_validation_enabled,
            "synthetic_fixtures_enabled": self.synthetic_fixtures_enabled,
            "synthetic_fixture_schema_version": self.synthetic_fixture_schema_version,
            "synthetic_fixture_default_seed": self.synthetic_fixture_default_seed,
            "synthetic_fixture_default_bar_count": self.synthetic_fixture_default_bar_count,
            "synthetic_fixture_default_start_price": self.synthetic_fixture_default_start_price,
            "synthetic_fixture_default_timeframe": self.synthetic_fixture_default_timeframe,
            "synthetic_fixture_allow_disk_writes": self.synthetic_fixture_allow_disk_writes,
            "synthetic_fixture_output_root": self.synthetic_fixture_output_root,
            "synthetic_fixture_label": self.synthetic_fixture_label,
            "instrument_persistence_enabled": self.instrument_persistence_enabled,
            "instrument_persistence_require_validation": self.instrument_persistence_require_validation,
            "instrument_persistence_allow_synthetic_seed": self.instrument_persistence_allow_synthetic_seed,
            "instrument_persistence_schema_version": self.instrument_persistence_schema_version,
            "market_data_batch_persistence_enabled": self.market_data_batch_persistence_enabled,
            "market_data_batch_persistence_require_validation": self.market_data_batch_persistence_require_validation,
            "market_data_batch_persistence_allow_synthetic": self.market_data_batch_persistence_allow_synthetic,
            "market_data_batch_persistence_schema_version": self.market_data_batch_persistence_schema_version,
            "synthetic_ohlcv_storage_enabled": self.synthetic_ohlcv_storage_enabled,
            "synthetic_ohlcv_storage_require_validation": self.synthetic_ohlcv_storage_require_validation,
            "synthetic_ohlcv_storage_allow_sqlite": self.synthetic_ohlcv_storage_allow_sqlite,
            "synthetic_ohlcv_storage_schema_version": self.synthetic_ohlcv_storage_schema_version,
            "synthetic_ohlcv_storage_max_bars_per_batch": self.synthetic_ohlcv_storage_max_bars_per_batch,
            "synthetic_ohlcv_export_enabled": self.synthetic_ohlcv_export_enabled,
            "synthetic_ohlcv_export_require_validation": self.synthetic_ohlcv_export_require_validation,
            "synthetic_ohlcv_export_allow_disk_writes": self.synthetic_ohlcv_export_allow_disk_writes,
            "synthetic_ohlcv_export_schema_version": self.synthetic_ohlcv_export_schema_version,
            "synthetic_ohlcv_export_default_zone": self.synthetic_ohlcv_export_default_zone,
            "synthetic_ohlcv_export_max_rows": self.synthetic_ohlcv_export_max_rows,
            "provider_guardrails_enabled": self.provider_guardrails_enabled,
            "provider_implementation_approval_required": self.provider_implementation_approval_required,
            "provider_terms_review_required": self.provider_terms_review_required,
            "provider_network_calls_default_allowed": self.provider_network_calls_default_allowed,
            "provider_scraping_default_allowed": self.provider_scraping_default_allowed,
            "provider_credentials_allowed": self.provider_credentials_allowed,
            "provider_guardrail_schema_version": self.provider_guardrail_schema_version,
            "local_sample_provider_enabled": self.local_sample_provider_enabled,
            "local_sample_provider_schema_version": self.local_sample_provider_schema_version,
            "local_sample_provider_default_seed": self.local_sample_provider_default_seed,
            "local_sample_provider_default_bar_count": self.local_sample_provider_default_bar_count,
            "local_sample_provider_default_start_price": self.local_sample_provider_default_start_price,
            "local_sample_provider_allow_network": self.local_sample_provider_allow_network,
            "local_sample_provider_allow_real_data": self.local_sample_provider_allow_real_data,
            "provider_readiness_enabled": self.provider_readiness_enabled,
            "provider_candidate_selection_schema_version": self.provider_candidate_selection_schema_version,
            "provider_candidate_real_implementation_allowed": self.provider_candidate_real_implementation_allowed,
            "provider_candidate_network_checks_allowed": self.provider_candidate_network_checks_allowed,
            "provider_candidate_scraping_checks_allowed": self.provider_candidate_scraping_checks_allowed,
            "provider_candidate_credentials_allowed": self.provider_candidate_credentials_allowed,
            "provider_candidate_minimum_score_for_design": self.provider_candidate_minimum_score_for_design,
            "provider_candidate_minimum_score_for_network_tests": self.provider_candidate_minimum_score_for_network_tests,
            "provider_candidate_minimum_score_for_production": self.provider_candidate_minimum_score_for_production,
            "local_file_provider_enabled": self.local_file_provider_enabled,
            "local_file_provider_schema_version": self.local_file_provider_schema_version,
            "local_file_provider_allowed_root": self.local_file_provider_allowed_root,
            "local_file_provider_allow_csv": self.local_file_provider_allow_csv,
            "local_file_provider_allow_parquet": self.local_file_provider_allow_parquet,
            "local_file_provider_allow_network_paths": self.local_file_provider_allow_network_paths,
            "local_file_provider_allow_symlinks": self.local_file_provider_allow_symlinks,
            "local_file_provider_max_rows": self.local_file_provider_max_rows,
            "local_file_provider_allow_real_data_claims": self.local_file_provider_allow_real_data_claims,
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()
