# Configuration

Prompt 13 maintains typed application settings through `stark_terminal_core.config.settings.Settings` and adds Data Quality + Validation Framework settings.

## Settings

Settings define the current app identity, API host/port, placeholder infrastructure URLs, feature store mode, safety flags, and local data roots. Values load from environment variables and `.env` when present.

Important defaults:

- `STARK_ENV=development`
- `APP_NAME=Stark Terminal`
- `APP_VERSION=0.1.0`
- `PROMPT_NUMBER=13`
- `API_HOST=127.0.0.1`
- `API_PORT=8000`
- `FEATURE_STORE_MODE=custom`

## Environment Variables

The settings model supports placeholders for `DATABASE_URL`, `TIMESCALE_DATABASE_URL`, `REDIS_URL`, `CLICKHOUSE_URL`, and `KAFKA_BOOTSTRAP_SERVERS`. Prompt 13 adds Data Quality + Validation Framework settings while keeping raw secrets hidden. Feast integration remains deferred.

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

## Safety Flags

Execution-related flags default to false:

- `EXECUTION_APIS_ENABLED=false`
- `BROKER_INTEGRATIONS_ENABLED=false`
- `LIVE_TRADING_ENABLED=false`

These flags fail closed in Prompt 13. Enabling them raises configuration validation errors because execution APIs, broker integrations, live trading, external market data calls, and provider network calls remain forbidden.

## Safe Settings Snapshot

`safe_settings_snapshot()` returns only non-secret display fields and boolean configured indicators for infrastructure URLs. It does not expose raw database, Redis, ClickHouse, Kafka, credential, token, or secret values.

Raw URLs and secrets must never be exposed by API responses.

Database and TimescaleDB configuration are exposed only as booleans such as `database_configured` and `timescale_configured`. Research lake settings expose safe relative roots and booleans only. Redis cache, Redis Streams, Kafka/Redpanda Event Backbone, Data Quality, Worker System, Instrument Master/Provider, ClickHouse Warehouse, and Feature Registry settings expose safe booleans and policy fields only. Raw database URLs, Timescale URLs, Redis URLs, ClickHouse URLs, Kafka bootstrap servers, Kafka SASL usernames/passwords, ClickHouse users/passwords, credentials, and host strings with secrets are not returned by `/config`, `/database/health`, `/timeseries/health`, `/research-lake/health`, `/cache/health`, `/streams/health`, `/event-backbone/health`, `/data-quality/health`, `/workers/health`, `/instruments/health`, `/providers/health`, `/warehouse/health`, or `/features/health`.

## Prompt 13 Configuration Audit

Prompt 13 confirms sensitive URLs and secrets are exposed only as configured booleans/status, not raw values. Safe snapshots must not expose raw database URLs, TimescaleDB URLs, Redis URLs, ClickHouse URLs, ClickHouse users, ClickHouse passwords, Kafka bootstrap strings, Kafka SASL credentials, API keys, tokens, broker secrets, or provider credentials. no execution APIs, no market data ingestion, no external validation, and no analytics signals remain enforced through disabled-by-default settings and local deterministic validators.
