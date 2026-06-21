# Redis Streams Foundation

Redis Streams are Stark Terminal's lightweight event pipeline layer. They provide early event coordination for later ingestion, normalization, feature computation, regime updates, options updates, risk updates, decision generation, backtest events, Paper Lab events, audit events, and system health events.

Redis Streams are not the system of record. PostgreSQL remains the durable system of record. TimescaleDB remains the operational time-series storage target. DuckDB and Parquet remain the research lake. Redis cache remains separate from Redis Streams semantics.

## Prompt 06 Scope

Prompt 06 implements:

- Redis Streams settings with streams disabled by default.
- Stream naming policy.
- EventEnvelope schema.
- Stream serialization helpers.
- Producer and consumer wrappers.
- In-memory stream fallback for deterministic local tests.
- Safe stream health checks.
- `GET /streams/health`.

Prompt 06 does not implement real workers, market-data ingestion, provider clients, broker integrations, execution APIs, Kafka/Redpanda, ClickHouse, Feature Store, analytics engines, or trading behavior.

Prompt 07 implements Worker System foundations separately. Stream-to-worker production wiring remains future work.

## Local And Test Behavior

Prompt 06 does not require Redis locally. When Redis Streams are disabled and `REDIS_STREAMS_USE_MEMORY_FALLBACK=true`, the stream producer and consumer use a local in-memory stream store. This fallback is for local development and tests only. It is not durable and must not be treated as a source of truth.

## Safety Rules

- `REDIS_URL` is sensitive and must never be exposed by API responses.
- Event payloads must not include secrets, credentials, raw URLs, provider tokens, API keys, or broker tokens.
- Event payloads must be JSON-serializable.
- Events coordinate future work; they do not execute trades.
- Kafka/Redpanda deferred to a later durable event replay prompt.
- Execution APIs remain forbidden.

## Next Step

Prompt 07 implements Worker System Foundation with worker configuration contracts, worker roles, job envelopes, safe test harnesses, and health checks. It does not implement real market data ingestion, infinite production loops, or execution APIs.
