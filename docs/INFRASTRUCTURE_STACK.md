# Infrastructure Stack

Prompt 14 implements the PostgreSQL-ready SQLAlchemy/Alembic foundation for metadata persistence, the TimescaleDB-oriented operational time-series schema foundation, the DuckDB + Parquet research lake foundation, the Redis cache foundation, the Redis Streams foundation, the Kafka/Redpanda Event Backbone foundation, the Data Quality + Validation Framework, the Synthetic Fixtures foundation, the Worker System foundation, the Instrument Master/Provider Contracts foundation, the ClickHouse Warehouse foundation, and the custom Stark Feature Registry foundation. Other infrastructure systems remain planned and not implemented.

## PostgreSQL

PostgreSQL is the system of record for relational and durable metadata: instruments, configurations, user research state, DecisionObject records, audits, experiment metadata, provider metadata, and operational control tables.

Prompt 02 implemented:

- SQLAlchemy base and engine/session foundation
- Alembic migration foundation
- Metadata ORM models for instruments, data providers, audit records, and decision object records
- Database health checks
- SQLite fallback for local tests/dev only

## TimescaleDB

TimescaleDB provides the operational time-series role for market bars, snapshots, generated market states, and future regime history. Prompt 03 implements PostgreSQL-compatible operational time-series tables, Alembic migration scaffolding, safe capability checks, and opt-in hypertable SQL planning.

Live TimescaleDB deployment is not required for tests. SQLite remains available for local/dev metadata checks. Actual hypertable creation requires PostgreSQL with the TimescaleDB extension and explicit configuration.

## DuckDB

DuckDB provides embedded analytical querying over Parquet datasets for research, local reproducibility, batch experiments, feature exploration, and future offline backtests. Prompt 04 implements local DuckDB connection and query helpers for the research lake. Production analytical dashboards are not implemented.

## Parquet Zone Plan

The Parquet research data lake will be separated into:

- `raw`: Provider-native or minimally touched source extracts.
- `cleaned`: Source data after basic quality checks and format cleanup.
- `normalized`: Canonical Stark market-data contracts and aligned schemas.
- `feature-ready`: Inputs prepared for feature computation.
- `backtest-ready`: Deterministic datasets for backtesting.
- `research-artifacts`: Experiment outputs, derived datasets, reports, and reproducibility artifacts.

Prompt 04 implements Parquet zone contracts and small local read/write helpers. Actual market datasets are not ingested yet.

## Redis

Redis provides the low-latency cache layer for short-lived status, health, latest state, latest DecisionObject, API response, and temporary computation-result cache entries. Prompt 05 implements Redis/cache settings, a cache key policy, JSON-safe serialization, a Redis client wrapper, in-memory local/test fallback, and safe cache health checks.

Redis is not the system of record. PostgreSQL remains durable truth, TimescaleDB remains operational time-series storage, and DuckDB/Parquet remains the research lake.

## Redis Streams

Redis Streams provide the lightweight event pipeline foundation for future worker coordination. Prompt 06 implements stream settings, stream naming policy, typed event envelopes, producer and consumer wrappers, in-memory local/test fallback, and safe stream health checks.

Redis cache and Redis Streams are separate semantics: cache accelerates short-lived lookup values; streams coordinate events. Neither is durable truth.

## Worker System

The Worker System foundation defines typed worker roles, JobEnvelope contracts, WorkerResult contracts, base worker lifecycle abstractions, a worker registry, an in-process test/local harness, and worker health checks. Prompt 07 does not implement actual production worker loops, schedulers, daemons, market data ingestion, analytics engines, broker integrations, or execution APIs.

Workers coordinate future jobs only after explicit implementation. They do not mean live execution or trading.

## Instrument Master / Provider Contracts

The Instrument Master/Provider Contracts foundation defines stable instrument identity, symbol normalization, instrument universe snapshots, read-only market data provider interfaces, local synthetic fixtures, and provider capability reports. Prompt 08 does not implement real ingestion, external provider clients, scraping, provider SDKs, broker integrations, or execution APIs.

Stable instrument identity is required across PostgreSQL, TimescaleDB, DuckDB/Parquet, Redis, Redis Streams, Worker System jobs, future ClickHouse analytical tables, and the future Feature Store.

## ClickHouse

ClickHouse supports high-speed analytical warehouse workloads, large scans, aggregate-heavy research, and future dashboard/query surfaces where PostgreSQL, TimescaleDB, or DuckDB are not the right serving layer. Prompt 09 implements table contracts, DDL helpers, disabled-safe client behavior, a memory query recorder, and warehouse health checks.

ClickHouse is not the system of record. Prompt 09 does not implement real analytical ingestion, production dashboards, automatic table creation, broker integrations, or execution APIs.

## Feature Registry

The custom Stark Feature Registry governs feature definitions, feature sets, typed feature values, snapshots, quality reports, lineage, freshness/staleness metadata, and training/serving consistency contracts. Prompt 10 implements in-memory metadata/governance contracts and health checks only.

The Feature Registry is not a computation engine and not a source of trade calls. Prompt 10 does not compute features, run indicators, train models, ingest market data, implement production feature pipelines, integrate Feast, or expose execution APIs.

Feast planned support remains a future option. It is not installed or implemented in Prompt 10.

## Kafka / Redpanda-Compatible Event Backbone

Kafka or a Redpanda-compatible event backbone provides the durable institutional event replay foundation for historical reprocessing, independent consumers, decoupled data pipelines, and replayable audit trails for production-grade workflows. Prompt 12 implements configuration contracts, topic policy, DurableEventEnvelope compatibility helpers, producer/consumer wrappers, an in-memory local/test fallback, health checks, and API routes.

Kafka/Redpanda is not system of record. Redis Streams remains the lightweight event pipeline foundation; Kafka/Redpanda is the durable event backbone foundation. Prompt 12 does not implement production event pipelines, production Kafka consumers, schema registry integration, ClickHouse ingestion, Feature Store computation pipelines, real market ingestion, broker integrations, or execution APIs.

## Data Quality + Validation Framework

The Data Quality + Validation Framework provides deterministic local validation contracts, issue schemas, rule schemas, validation reports, quality gates, a registry, built-in validators, and health checks. Prompt 13 implements it as a foundation only.

The framework sits across the storage and event layers: it can validate future PostgreSQL metadata contracts, TimescaleDB operational bars, DuckDB/Parquet research datasets, ClickHouse warehouse table contracts, Feature Registry snapshots, provider responses, Redis Streams events, and Kafka/Redpanda durable events after explicit future prompts wire those flows. It does not ingest real market data, run production validation pipelines, make external calls, compute analytics signals, mutate durable state, or enable execution APIs.

## Synthetic Fixtures

Prompt 14 implements deterministic synthetic OHLCV fixtures, fixture manifests, a local metadata catalog, validation helpers, temporary Parquet roundtrip helpers, and fixture health checks.

Synthetic Fixtures are not infrastructure truth, not a system of record, not provider data, and not live market data. They exist only for local/test/dev workflows. Disk writes are disabled by default for the configured output root, and any test Parquet writes must be explicitly directed to temporary paths.

No real ingestion exists in Prompt 14. Real market ingestion still requires provider adapters, data-policy review, source references, quality gates, and a future explicit prompt.

## Worker Pipeline Plan

Planned workers:

- `ingestion_worker`
- `normalization_worker`
- `feature_worker`
- `regime_worker`
- `options_worker`
- `risk_worker`
- `decision_worker`
- `backtest_worker`
- `paper_lab_worker`
- `audit_worker`

Prompt 07 adds worker contracts and a local/test harness. Actual worker implementations and production loops remain deferred.

## Audit / Event Log Strategy

Every important data mutation, feature computation, regime update, decision generation, backtest run, options/risk calculation, and research artifact should eventually be auditable. The audit/event strategy will use append-only logs, deterministic identifiers, source data references, model or rule versions, generated timestamps, and replayable event streams where appropriate.

## Prompt 11 Infrastructure Audit Summary

Implemented foundation layers: PostgreSQL metadata, TimescaleDB schema planning, DuckDB/Parquet research lake helpers, Redis cache, Redis Streams, Kafka/Redpanda Event Backbone, Data Quality + Validation Framework, Synthetic Fixtures, Worker System, Instrument/Provider Contracts, ClickHouse Warehouse contracts, and Feature Registry contracts. Planned layers: external feature store backends, real ingestion pipelines, production worker deployment, production event pipelines, production validation pipelines, production dashboards, and analytics engines.

Prompt 11 adds audit tooling only. It does not implement Kafka/Redpanda, real market ingestion, external provider calls, automatic table creation, feature computation, broker integrations, or no execution APIs.

## Prompt 15 Instrument Metadata Persistence Wiring

Prompt 15 marks Instrument Metadata Persistence Wiring as implemented. PostgreSQL remains the intended system of record, and the existing SQLite fallback supports deterministic local tests and development. The first repository/service wiring is metadata-only through `InstrumentRepository` and `InstrumentMetadataService`.

This layer persists canonical instrument metadata after validation-before-persistence. It does not persist OHLCV bars, run real market ingestion, call external providers, publish events, compute analytics, or expose execution APIs.

## Prompt 16 Market Data Batch Persistence Contracts

Prompt 16 marks Market Data Batch Persistence Contracts as implemented. PostgreSQL remains the intended system of record and now has metadata-only repository/service wiring for validated synthetic/local market data batch records through `MarketDataBatchRecordORM`, `MarketDataBatchRepository`, and `MarketDataBatchMetadataService`.

This layer stores batch metadata only: batch id, instrument, timeframe, row count, time range, quality status, source reference, synthetic flag, fixture linkage, dataset manifest linkage, and validation report linkage. It stores no full OHLCV bars and performs no TimescaleDB data writes, ClickHouse writes, DuckDB/Parquet production writes, Redis/Kafka publishing, real market ingestion, external calls, analytics, or execution APIs.

TimescaleDB still owns future operational bar storage. DuckDB/Parquet still owns future research datasets. ClickHouse still owns future analytical copies. Prompt 16 only records metadata needed to audit future batch flows.
