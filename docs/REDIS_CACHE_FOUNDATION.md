# Redis Cache Foundation

Redis is Stark Terminal's low-latency cache layer. It is used for short-lived service state, latest health/status snapshots, future latest market-state lookups, latest DecisionObject cache entries, API response cache entries, and temporary computation results.

Redis is not the system of record. PostgreSQL remains the durable system of record. TimescaleDB remains the operational time-series storage target. DuckDB and Parquet remain the research lake.

## Prompt 05 Scope

Prompt 05 implements:

- Redis/cache settings with Redis disabled by default.
- Cache key namespace policy.
- JSON-safe cache serialization helpers.
- A small Redis cache client wrapper.
- In-memory fallback for deterministic local tests.
- Safe cache health checks.
- `GET /cache/health`.

Prompt 05 does not implement Redis Streams, event pipelines, market-data ingestion, provider clients, broker integrations, execution APIs, Kafka/Redpanda, ClickHouse, Feature Store, analytics engines, or trading behavior.

Prompt 06 implements Redis Streams separately. Cache semantics remain separate from stream/event pipeline semantics.

## Local And Test Behavior

Prompt 05 does not require Redis locally. When Redis is disabled and `CACHE_USE_MEMORY_FALLBACK=true`, the cache client uses a local in-memory backend. This fallback is for local development and tests only. It is not durable and must not be treated as a source of truth.

## Safety Rules

- `REDIS_URL` is sensitive and must never be exposed by API responses.
- Cache keys must not include secrets, credentials, raw URLs, or provider tokens.
- Cache values should be JSON-serializable.
- Cache entries should use explicit TTLs or the configured default TTL.
- Cache misses must not imply missing durable truth.
- Execution APIs remain forbidden.

## Next Step

Prompt 06 implements Redis Streams Event Pipeline Foundation. Prompt 07 should implement Worker System Foundation.
