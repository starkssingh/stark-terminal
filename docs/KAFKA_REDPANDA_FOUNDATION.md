# Kafka/Redpanda Event Backbone Foundation

Kafka/Redpanda is Stark Terminal's durable institutional event backbone. It is intended for future high-throughput event routing, independent consumers, replayable workflows, cross-service coordination, ingestion pipelines, feature computation pipelines, regime/decision/backtest pipeline events, and future analytical pipeline events.

## Relationship To Existing Foundations

- Kafka/Redpanda is the durable event backbone.
- Redis Streams remains the lightweight event pipeline foundation.
- Kafka/Redpanda is not system of record.
- PostgreSQL remains system of record.
- TimescaleDB remains the operational time-series layer.
- DuckDB/Parquet remains the research lake.
- ClickHouse remains the analytical warehouse.
- Feature Registry remains the feature governance layer.

## Prompt 12 Scope

Prompt 12 implements:

- Kafka/Redpanda configuration contracts.
- Event-backbone topic policy.
- DurableEventEnvelope contracts compatible with Redis Streams EventEnvelope semantics.
- Producer/consumer wrappers.
- In-memory event backbone fallback for deterministic local tests.
- Safe event-backbone health checks.
- `GET /event-backbone/health`.
- Read-only `GET /event-backbone/topics`.

Prompt 12 does not implement production pipelines, production Kafka consumers, real market data ingestion, schema registry integration, ClickHouse ingestion, Feature Store computation pipelines, analytics engines, broker integrations, or execution APIs.

## Local And Test Behavior

Prompt 12 does not require Kafka/Redpanda locally. When Kafka is disabled and `KAFKA_USE_MEMORY_FALLBACK=true`, producer and consumer wrappers use the in-memory event backbone. This memory fallback is local/test only and is not durable storage.

`confluent-kafka` is installed as the client dependency, but imports are optional and no Kafka connection is created at import time.

## Safety

- `KAFKA_BOOTSTRAP_SERVERS`, SASL username, and SASL password are sensitive and must never be exposed.
- Durable event payloads must be JSON-serializable.
- Durable event payloads must not include secrets, credentials, raw URLs, database URLs, Redis URLs, ClickHouse URLs, Kafka bootstrap servers, broker tokens, or broker secrets.
- no execution APIs.
- no market data ingestion.
- no execution/order/broker/live-trading topics or events.

## Next Step

Prompt 13 - Data Quality + Validation Framework.

Development environment remains Mac mini M2 / macOS / Apple Silicon. Target desktop product remains Windows-native Stark Terminal.
