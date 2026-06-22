# Configuration

Prompt 25 maintains typed application settings through `stark_terminal_core.config.settings.Settings` and adds no new settings. Prompt 24 added safe Local File Provider settings, Prompt 23 added safe Provider Readiness settings, Prompt 21 added safe Local Sample Provider settings, Prompt 20 added Provider Guardrail settings, Prompt 19 added Synthetic OHLCV Export settings, Prompt 18 added Synthetic OHLCV Storage settings, Prompt 14 added Synthetic Fixture settings, Prompt 15 added Instrument Persistence settings, and Prompt 16 added Market Data Batch Persistence settings.

## Settings

Settings define the current app identity, API host/port, placeholder infrastructure URLs, feature store mode, safety flags, and local data roots. Values load from environment variables and `.env` when present.

Important defaults:

- `STARK_ENV=development`
- `APP_NAME=Stark Terminal`
- `APP_VERSION=0.1.0`
- `PROMPT_NUMBER=25`
- `API_HOST=127.0.0.1`
- `API_PORT=8000`
- `FEATURE_STORE_MODE=custom`

## Environment Variables

The settings model supports placeholders for `DATABASE_URL`, `TIMESCALE_DATABASE_URL`, `REDIS_URL`, `CLICKHOUSE_URL`, and `KAFKA_BOOTSTRAP_SERVERS`. Prompt 19 adds no sensitive settings and keeps raw secrets hidden. Feast integration remains deferred.

## Database Settings

Prompt 02 adds PostgreSQL-ready database settings:

- `DATABASE_URL`
- `DATABASE_ECHO=false`
- `DATABASE_POOL_SIZE=5`
- `DATABASE_MAX_OVERFLOW=10`
- `DATABASE_POOL_PRE_PING=true`
- `DATABASE_CONNECT_TIMEOUT_SECONDS=10`

`DATABASE_URL` is sensitive and must never be exposed. When it is not configured, the database foundation uses a SQLite fallback for local tests/dev only.

## TimescaleDB Settings

Prompt 03 adds TimescaleDB-oriented settings:

- `TIMESCALE_DATABASE_URL`
- `TIMESCALE_ENABLED=false`
- `TIMESCALE_EXTENSION_NAME=timescaledb`
- `TIMESCALE_CREATE_EXTENSION=false`
- `TIMESCALE_CREATE_HYPERTABLES=false`
- `TIMESCALE_CHUNK_INTERVAL=7 days`

TimescaleDB is disabled by default. Extension creation and hypertable creation are also disabled by default. `TIMESCALE_DATABASE_URL` is sensitive and must never be exposed. Safe API snapshots expose only booleans such as `timescale_configured`, `timescale_enabled`, `timescale_create_extension`, and `timescale_create_hypertables`.

## Research Lake Settings

Prompt 04 adds research lake settings:

- `LAKE_ROOT=data/lake`
- `DUCKDB_DATABASE_PATH=data/lake/stark_terminal.duckdb`
- `DUCKDB_READ_ONLY=false`
- `PARQUET_COMPRESSION=zstd`
- `CREATE_LAKE_DIRS=false`

`CREATE_LAKE_DIRS=false` means health checks do not create directories by default. Directory creation happens only when explicitly requested. `PARQUET_COMPRESSION` supports `zstd`, `snappy`, `gzip`, and `none`.

All path handling must use `pathlib`. Do not hardcode macOS-specific or Windows-specific paths. Development currently runs on Mac mini M2 / macOS / Apple Silicon, while the desktop target remains Windows-native Stark Terminal.

## Redis Cache Settings

Prompt 05 adds Redis/cache settings:

- `REDIS_URL`
- `REDIS_ENABLED=false`
- `REDIS_SOCKET_TIMEOUT_SECONDS=2.0`
- `REDIS_CONNECT_TIMEOUT_SECONDS=2.0`
- `REDIS_HEALTH_CHECK_INTERVAL_SECONDS=30`
- `CACHE_DEFAULT_TTL_SECONDS=300`
- `CACHE_KEY_PREFIX=stark`
- `CACHE_ENVIRONMENT_NAMESPACE=development`
- `CACHE_USE_MEMORY_FALLBACK=true`

Redis is disabled by default and `REDIS_URL` is sensitive. Safe API snapshots expose only `redis_configured`, `redis_enabled`, `cache_default_ttl_seconds`, `cache_key_prefix`, `cache_environment_namespace`, and `cache_use_memory_fallback`.

The in-memory fallback is for local development and deterministic tests only. It is not durable storage.

## Redis Streams Settings

Prompt 06 adds Redis Streams settings:

- `REDIS_STREAMS_ENABLED=false`
- `REDIS_STREAMS_USE_MEMORY_FALLBACK=true`
- `STREAM_KEY_PREFIX=stark`
- `STREAM_ENVIRONMENT_NAMESPACE=development`
- `STREAM_CONSUMER_GROUP=stark-terminal`
- `STREAM_READ_COUNT=10`
- `STREAM_BLOCK_MS=1000`
- `STREAM_MAX_LEN=10000`
- `STREAM_APPROXIMATE_TRIM=true`
- `EVENT_SCHEMA_VERSION=v1`

Redis Streams are disabled by default and share the sensitive `REDIS_URL`. Safe API snapshots expose only `redis_streams_enabled`, `redis_streams_use_memory_fallback`, stream naming fields, read limits, trim settings, and `event_schema_version`.

The in-memory stream fallback is for local development and deterministic tests only. It is not durable storage. Kafka/Redpanda remains deferred.

## Worker Settings

Prompt 07 adds Worker System settings:

- `WORKERS_ENABLED=false`
- `WORKER_HARNESS_MODE=in_process`
- `WORKER_DEFAULT_TIMEOUT_SECONDS=30`
- `WORKER_MAX_RETRIES=0`
- `WORKER_DEFAULT_QUEUE=default`
- `WORKER_SCHEMA_VERSION=v1`
- `WORKER_ALLOW_BACKGROUND_THREADS=false`
- `WORKER_ALLOW_INFINITE_LOOPS=false`

Workers are disabled by default. The in-process harness is for local/test use only. Background threads and infinite loops are disabled by default and are treated as unsafe for this foundation stage.

## Instrument Master And Provider Settings

Prompt 08 adds Instrument Master and provider contract settings:

- `INSTRUMENT_MASTER_MODE=local`
- `INSTRUMENT_MASTER_SOURCE=synthetic`
- `ALLOW_EXTERNAL_MARKET_DATA_CALLS=false`
- `ALLOW_PROVIDER_NETWORK_CALLS=false`
- `MARKET_DATA_CONTRACT_SCHEMA_VERSION=v1`
- `DEFAULT_MARKET_DATA_PROVIDER=local_sample`
- `DEFAULT_EXCHANGE=NSE`
- `DEFAULT_MARKET_SEGMENT=NSE_EQUITY`

External market data calls and provider network calls are disabled by default and fail closed in Prompt 08. The local instrument master uses synthetic fixtures only. No provider credentials or broker credentials exist in settings.

## ClickHouse Warehouse Settings

Prompt 09 adds ClickHouse Warehouse settings:

- `CLICKHOUSE_URL`
- `CLICKHOUSE_ENABLED=false`
- `CLICKHOUSE_HOST=localhost`
- `CLICKHOUSE_PORT=8123`
- `CLICKHOUSE_DATABASE=stark_terminal`
- `CLICKHOUSE_USER`
- `CLICKHOUSE_PASSWORD`
- `CLICKHOUSE_SECURE=false`
- `CLICKHOUSE_CONNECT_TIMEOUT_SECONDS=5`
- `CLICKHOUSE_SEND_RECEIVE_TIMEOUT_SECONDS=30`
- `CLICKHOUSE_USE_MEMORY_FALLBACK=true`
- `WAREHOUSE_SCHEMA_VERSION=v1`

ClickHouse is disabled by default. `CLICKHOUSE_URL`, `CLICKHOUSE_USER`, and `CLICKHOUSE_PASSWORD` are sensitive and must never be exposed. When ClickHouse is disabled and memory fallback is enabled, the warehouse client records queries in a local memory recorder for deterministic tests only.

## Feature Registry Settings

Prompt 10 adds Feature Registry settings:

- `FEATURE_STORE_MODE=custom`
- `FEATURE_REGISTRY_ENABLED=false`
- `FEATURE_REGISTRY_BACKEND=memory`
- `FEATURE_REGISTRY_SCHEMA_VERSION=v1`
- `FEATURE_REGISTRY_ALLOW_EXTERNAL_BACKEND=false`
- `FEATURE_REGISTRY_REQUIRE_LINEAGE=true`
- `FEATURE_REGISTRY_REQUIRE_QUALITY_REPORT=true`
- `FEATURE_DEFAULT_FRESHNESS_SECONDS=86400`
- `FEATURE_MAX_ALLOWED_STALENESS_SECONDS=604800`

`FEATURE_STORE_MODE` supports `custom`, `feast_planned`, and `disabled`. `FEATURE_REGISTRY_BACKEND` supports `memory`, `postgres_planned`, and `feast_planned`. The registry is disabled by default and external backends are disabled by default. Feast planned mode is a documented future option, not an implemented integration.

## Kafka/Redpanda Event Backbone Settings

Prompt 12 adds event backbone settings:

- `EVENT_BACKBONE_MODE=memory`
- `KAFKA_ENABLED=false`
- `KAFKA_BOOTSTRAP_SERVERS`
- `KAFKA_CLIENT_ID=stark-terminal`
- `KAFKA_SECURITY_PROTOCOL=PLAINTEXT`
- `KAFKA_SASL_USERNAME`
- `KAFKA_SASL_PASSWORD`
- `KAFKA_DEFAULT_PARTITIONS=3`
- `KAFKA_REPLICATION_FACTOR=1`
- `KAFKA_REQUEST_TIMEOUT_SECONDS=5`
- `KAFKA_TOPIC_PREFIX=stark`
- `KAFKA_ENVIRONMENT_NAMESPACE=development`
- `KAFKA_USE_MEMORY_FALLBACK=true`
- `DURABLE_EVENT_SCHEMA_VERSION=v1`

Kafka is disabled by default. `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_SASL_USERNAME`, and `KAFKA_SASL_PASSWORD` are sensitive and must never be exposed. When Kafka/Redpanda is disabled and memory fallback is enabled, event backbone producer and consumer wrappers use an in-memory local/test backbone.

## Data Quality Settings

Prompt 13 adds Data Quality + Validation Framework settings:

- `DATA_QUALITY_ENABLED=true`
- `DATA_QUALITY_SCHEMA_VERSION=v1`
- `DATA_QUALITY_DEFAULT_FAIL_ON_ERROR=true`
- `DATA_QUALITY_DEFAULT_FAIL_ON_WARNING=false`
- `DATA_QUALITY_MAX_ISSUES_PER_REPORT=100`
- `DATA_QUALITY_REQUIRE_SOURCE_REFERENCE=true`
- `DATA_QUALITY_REQUIRE_TIMEZONE_AWARE_TIMESTAMPS=true`
- `DATA_QUALITY_ALLOW_SYNTHETIC_DATA=true`
- `DATA_QUALITY_EXTERNAL_VALIDATION_ENABLED=false`

Data quality is enabled by default, but external validation is disabled by default. Prompt 13 validators are deterministic and local. They do not make external calls, ingest real market data, run production validation pipelines, compute analytics signals, or enable execution APIs.

Source references and timezone-aware timestamps are required by default. Synthetic/local test data remains allowed so deterministic tests can validate contracts without external providers.

## Synthetic Fixture Settings

Prompt 14 adds Synthetic Market Data Fixture settings:

- `SYNTHETIC_FIXTURES_ENABLED=true`
- `SYNTHETIC_FIXTURE_SCHEMA_VERSION=v1`
- `SYNTHETIC_FIXTURE_DEFAULT_SEED=42`
- `SYNTHETIC_FIXTURE_DEFAULT_BAR_COUNT=30`
- `SYNTHETIC_FIXTURE_DEFAULT_START_PRICE=100.0`
- `SYNTHETIC_FIXTURE_DEFAULT_TIMEFRAME=DAILY`
- `SYNTHETIC_FIXTURE_ALLOW_DISK_WRITES=false`
- `SYNTHETIC_FIXTURE_OUTPUT_ROOT=data/synthetic_fixtures`
- `SYNTHETIC_FIXTURE_LABEL=synthetic-local-test-only`

Synthetic fixtures are enabled by default for local/test/dev use. Disk writes are disabled by default for the configured output root. Deterministic seed, bar count, start price, timeframe, schema version, and label fields are exposed through the safe settings snapshot.

## Safety Flags

Execution-related flags default to false:

- `EXECUTION_APIS_ENABLED=false`
- `BROKER_INTEGRATIONS_ENABLED=false`
- `LIVE_TRADING_ENABLED=false`

These flags fail closed in Prompt 16. Enabling them raises configuration validation errors because execution APIs, broker integrations, live trading, external market data calls, and provider network calls remain forbidden.

## Safe Settings Snapshot

`safe_settings_snapshot()` returns only non-secret display fields and boolean configured indicators for infrastructure URLs. It does not expose raw database, Redis, ClickHouse, Kafka, credential, token, or secret values.

Raw URLs and secrets must never be exposed by API responses.

Database and TimescaleDB configuration are exposed only as booleans such as `database_configured` and `timescale_configured`. Research lake settings expose safe relative roots and booleans only. Redis cache, Redis Streams, Kafka/Redpanda Event Backbone, Data Quality, Synthetic Fixtures, Worker System, Instrument Master/Provider, ClickHouse Warehouse, and Feature Registry settings expose safe booleans and policy fields only. Raw database URLs, Timescale URLs, Redis URLs, ClickHouse URLs, Kafka bootstrap servers, Kafka SASL usernames/passwords, ClickHouse users/passwords, credentials, and host strings with secrets are not returned by `/config`, `/database/health`, `/timeseries/health`, `/research-lake/health`, `/cache/health`, `/streams/health`, `/event-backbone/health`, `/data-quality/health`, `/fixtures/health`, `/workers/health`, `/instruments/health`, `/providers/health`, `/warehouse/health`, or `/features/health`.

## Prompt 16 Configuration Audit

Prompt 16 confirms sensitive URLs and secrets are exposed only as configured booleans/status, not raw values. Safe snapshots must not expose raw database URLs, TimescaleDB URLs, Redis URLs, ClickHouse URLs, ClickHouse users, ClickHouse passwords, Kafka bootstrap strings, Kafka SASL credentials, API keys, tokens, broker secrets, or provider credentials. no execution APIs, no market data ingestion, no external validation, no external provider calls, and no analytics signals remain enforced through disabled-by-default settings, local deterministic validators, synthetic fixture labels, and validation-gated metadata persistence.

## Instrument Persistence Settings

Prompt 15 adds Instrument Metadata Persistence settings:

- `INSTRUMENT_PERSISTENCE_ENABLED=true`
- `INSTRUMENT_PERSISTENCE_REQUIRE_VALIDATION=true`
- `INSTRUMENT_PERSISTENCE_ALLOW_SYNTHETIC_SEED=true`
- `INSTRUMENT_PERSISTENCE_SCHEMA_VERSION=v1`

Validation is required by default. Synthetic seeding is allowed by default for local/test/dev workflows only. `instrument_persistence_schema_version` cannot be empty. Safe settings snapshots may expose these booleans and schema status but must not expose database URLs or credentials.

Instrument persistence remains metadata-only: no real market ingestion, no external calls, no OHLCV persistence, no broker behavior, and no execution APIs.

## Market Data Batch Persistence Settings

Prompt 16 adds Market Data Batch Persistence settings:

- `MARKET_DATA_BATCH_PERSISTENCE_ENABLED=true`
- `MARKET_DATA_BATCH_PERSISTENCE_REQUIRE_VALIDATION=true`
- `MARKET_DATA_BATCH_PERSISTENCE_ALLOW_SYNTHETIC=true`
- `MARKET_DATA_BATCH_PERSISTENCE_SCHEMA_VERSION=v1`

Validation is required by default. Synthetic batch metadata is allowed by default for local/test/dev workflows only. `market_data_batch_persistence_schema_version` cannot be empty. Safe settings snapshots may expose these booleans and schema status but must not expose database URLs or credentials.

Market data batch persistence remains metadata-only: no real market ingestion, no external calls, no full OHLCV bars, no broker behavior, and no execution APIs.

## Synthetic OHLCV Storage Settings

Prompt 18 adds TimescaleDB Synthetic OHLCV Storage settings:

- `SYNTHETIC_OHLCV_STORAGE_ENABLED=true`
- `SYNTHETIC_OHLCV_STORAGE_REQUIRE_VALIDATION=true`
- `SYNTHETIC_OHLCV_STORAGE_ALLOW_SQLITE=true`
- `SYNTHETIC_OHLCV_STORAGE_SCHEMA_VERSION=v1`
- `SYNTHETIC_OHLCV_STORAGE_MAX_BARS_PER_BATCH=10000`

Validation is required by default. SQLite is allowed by default for local tests/dev so Prompt 18 does not require a live TimescaleDB server. The schema version cannot be empty, and max bars per batch must be positive.

Safe settings snapshots may expose these booleans and schema/limit fields. They must not expose database URLs, TimescaleDB URLs, provider credentials, broker secrets, tokens, or API keys.

Synthetic OHLCV storage remains synthetic-only: no real market data, no real market ingestion, no external calls, no analytics signals, no decisions, and no execution APIs.

## Synthetic OHLCV Export Settings

Prompt 19 adds Synthetic OHLCV Export settings:

- `SYNTHETIC_OHLCV_EXPORT_ENABLED=true`
- `SYNTHETIC_OHLCV_EXPORT_REQUIRE_VALIDATION=true`
- `SYNTHETIC_OHLCV_EXPORT_ALLOW_DISK_WRITES=false`
- `SYNTHETIC_OHLCV_EXPORT_SCHEMA_VERSION=v1`
- `SYNTHETIC_OHLCV_EXPORT_DEFAULT_ZONE=RESEARCH_ARTIFACTS`
- `SYNTHETIC_OHLCV_EXPORT_MAX_ROWS=10000`

Validation is required by default. Disk writes are disabled by default for configured production-style paths; tests pass an explicit temporary path. The schema version and default zone cannot be empty, the default zone must be supported, and max rows must be positive.

Safe settings snapshots may expose these booleans and schema/limit/zone fields. They must not expose database URLs, TimescaleDB URLs, provider credentials, broker secrets, tokens, or API keys.

Synthetic OHLCV export remains synthetic-only: no real market data, no real market ingestion, no external calls, no production research lake writes by default, no analytics signals, no decisions, and no execution APIs.

## Provider Guardrail Settings

Prompt 20 adds Provider Adapter Guardrail settings:

- `PROVIDER_GUARDRAILS_ENABLED=true`
- `PROVIDER_IMPLEMENTATION_APPROVAL_REQUIRED=true`
- `PROVIDER_TERMS_REVIEW_REQUIRED=true`
- `PROVIDER_NETWORK_CALLS_DEFAULT_ALLOWED=false`
- `PROVIDER_SCRAPING_DEFAULT_ALLOWED=false`
- `PROVIDER_CREDENTIALS_ALLOWED=false`
- `PROVIDER_GUARDRAIL_SCHEMA_VERSION=v1`

Provider guardrails are enabled by default. Approval and terms review are required by default. Network calls, scraping, and credentials are disabled by default and fail closed if enabled in the current phase. The schema version cannot be empty.

Safe settings snapshots may expose these booleans and the schema version. They must not expose provider credentials, provider URLs, API keys, tokens, broker secrets, raw database URLs, or any sensitive configuration value.

Provider guardrails remain governance contracts only: no real provider implementation, no provider SDKs, no external calls, no scraping, no real market ingestion, no analytics signals, no decisions, and no execution APIs.

## Local Sample Provider Settings

Prompt 21 adds Local Sample Provider Adapter v0 settings:

- `LOCAL_SAMPLE_PROVIDER_ENABLED=true`
- `LOCAL_SAMPLE_PROVIDER_SCHEMA_VERSION=v1`
- `LOCAL_SAMPLE_PROVIDER_DEFAULT_SEED=42`
- `LOCAL_SAMPLE_PROVIDER_DEFAULT_BAR_COUNT=30`
- `LOCAL_SAMPLE_PROVIDER_DEFAULT_START_PRICE=100.0`
- `LOCAL_SAMPLE_PROVIDER_ALLOW_NETWORK=false`
- `LOCAL_SAMPLE_PROVIDER_ALLOW_REAL_DATA=false`

The local sample provider is enabled by default for synthetic local/test/dev responses. Network calls and real data are disabled by default and fail closed if enabled. The schema version cannot be empty, default bar count must be positive, and default start price must be positive.

Safe settings snapshots may expose these booleans and deterministic generation defaults. They must not expose provider credentials, provider URLs, API keys, broker secrets, raw database URLs, or any sensitive configuration value.

Local Sample Provider Adapter v0 remains synthetic-only: no external calls, no real market data, no scraping, no credentials, no analytics signals, no decisions, and no execution APIs.

## Provider Readiness Settings

Prompt 23 adds Real Provider Readiness and Candidate Selection settings:

- `PROVIDER_READINESS_ENABLED=true`
- `PROVIDER_CANDIDATE_SELECTION_SCHEMA_VERSION=v1`
- `PROVIDER_CANDIDATE_REAL_IMPLEMENTATION_ALLOWED=false`
- `PROVIDER_CANDIDATE_NETWORK_CHECKS_ALLOWED=false`
- `PROVIDER_CANDIDATE_SCRAPING_CHECKS_ALLOWED=false`
- `PROVIDER_CANDIDATE_CREDENTIALS_ALLOWED=false`
- `PROVIDER_CANDIDATE_MINIMUM_SCORE_FOR_DESIGN=70`
- `PROVIDER_CANDIDATE_MINIMUM_SCORE_FOR_NETWORK_TESTS=85`
- `PROVIDER_CANDIDATE_MINIMUM_SCORE_FOR_PRODUCTION=95`

Provider readiness is enabled by default, but real implementation, network checks, scraping checks, and credentials are all disabled by default and fail closed if enabled in Prompt 23. The schema version cannot be empty. Scores must be between 0 and 100, the network-test threshold must be greater than or equal to the design threshold, and the production threshold must be greater than or equal to the network-test threshold.

Safe settings snapshots may expose these booleans and thresholds. They must not expose provider credentials, API keys, tokens, raw provider URLs, broker secrets, or any sensitive configuration value.

Provider readiness remains governance-only: no provider SDKs, no external calls, no scraping, no credentials, no real market ingestion, no production approval, no analytics signals, no decisions, and no execution APIs.

## Local File Provider Settings

Prompt 24 adds Local File Provider Adapter v0 settings:

- `LOCAL_FILE_PROVIDER_ENABLED=true`
- `LOCAL_FILE_PROVIDER_SCHEMA_VERSION=v1`
- `LOCAL_FILE_PROVIDER_ALLOWED_ROOT=data/local_files`
- `LOCAL_FILE_PROVIDER_ALLOW_CSV=true`
- `LOCAL_FILE_PROVIDER_ALLOW_PARQUET=true`
- `LOCAL_FILE_PROVIDER_ALLOW_NETWORK_PATHS=false`
- `LOCAL_FILE_PROVIDER_ALLOW_SYMLINKS=false`
- `LOCAL_FILE_PROVIDER_MAX_ROWS=10000`
- `LOCAL_FILE_PROVIDER_ALLOW_REAL_DATA_CLAIMS=false`

The local file provider is enabled by default for explicit local/test/dev file workflows. CSV and Parquet are allowed by default. Network paths, symlinks, and real-data claims are disabled by default and fail closed if enabled in Prompt 24. The schema version and allowed root cannot be empty, and max rows must be positive.

Safe settings snapshots may expose these booleans, the local test/dev root, schema version, and row limit. They must not expose provider credentials, provider URLs, API keys, tokens, broker secrets, raw database URLs, or any sensitive configuration value.

Local File Provider Adapter v0 remains local-file-only and test/dev only: no external calls, no real market data claims, no scraping, no credentials, no arbitrary file read API, no analytics signals, no decisions, and no execution APIs.
