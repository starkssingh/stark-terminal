# Architecture

## Model

Stark Terminal is a cloud-brain plus Windows-native terminal. The desktop application provides a dense terminal-style user experience for Indian-market research and decision support. The backend acts as the cloud brain, exposing typed APIs and eventually coordinating data ingestion, feature computation, analytics, backtesting, risk, options analytics, and audit trails.

## Backend

The backend is FastAPI. Prompt 00 implements only the application shell and health endpoint. The backend will evolve into a REST-first API layer with service boundaries for instruments, market data, features, regime/state, decisions, backtests, options, risk, research artifacts, and system health.

REST is the default integration model. WebSockets may be introduced later only when a concrete streaming UI workflow requires them.

## Desktop Client

The desktop client is PySide6 / Qt 6 for a Windows-native terminal. Prompt 00 includes only a minimal placeholder shell. Later prompts will implement the Retail Decision Console, Quant Lab, Options Desk, Backtest Lab, Risk Lab, Data Lab, Paper Lab, Journal, Settings, and System Health / Infrastructure Console.

## Service-Layer Architecture

The architecture layers are:

```text
desktop app
  -> API gateway/backend
  -> service layer
  -> core domain
  -> data platform
  -> analytics engines
  -> storage/event systems
```

The service layer will coordinate application use cases without leaking storage details into the desktop client or analytics engines. Core domain contracts remain typed and testable.

## Package Separation

- `apps/api`: FastAPI app and HTTP routes.
- `apps/desktop`: PySide6 desktop shell and future UI surfaces.
- `packages/core`: Shared domain contracts and enums.
- `packages/data_platform`: Future storage, data lake, provider, streaming, feature store, and data-quality abstractions.
- `packages/analytics`: Future quant, statistical, ML, optimization, options, risk, and backtesting logic.
- `packages/research`: Future Paper Lab, StrategyCandidate, experiment tracking, and research artifacts.

## Target Storage and Event Systems

- PostgreSQL will become the system of record for metadata, users' local research state, instruments, configurations, decisions, audits, and durable relational records.
- TimescaleDB will become the operational time-series store for market bars, events, and time-indexed observations that need PostgreSQL compatibility.
- DuckDB and Parquet will form the research lake for analytical queries, reproducible datasets, feature snapshots, backtest-ready data, and research artifacts.
- Redis provides the low-latency cache foundation in Prompt 05.
- Redis Streams provide the lightweight event pipeline foundation in Prompt 06 for future worker coordination.
- Worker System foundation in Prompt 07 defines typed worker roles, job envelopes, results, registry, in-process test harness, and health checks.
- Instrument Master and Market Data Provider contracts in Prompt 08 define stable instrument identity, symbol normalization, read-only provider interfaces, synthetic fixtures, and health checks.
- ClickHouse Warehouse foundation in Prompt 09 defines analytical table contracts, DDL helpers, disabled-safe client behavior, memory query recorder fallback, and health checks.
- Feature Registry foundation in Prompt 10 defines feature definitions, feature sets, typed values, snapshots, quality reports, lineage records, an in-memory registry, and health checks.
- Kafka/Redpanda Event Backbone foundation in Prompt 12 defines durable topic contracts, DurableEventEnvelope compatibility helpers, producer/consumer wrappers, memory fallback, and health checks.
- Data Quality + Validation Framework in Prompt 13 defines deterministic validation issues, rules, results, reports, quality gates, built-in validators, registry, and health checks.
- ClickHouse will provide high-speed analytical warehouse workloads for large scans and aggregate-heavy market research.
- Feast or a custom Stark Feature Registry will provide feature governance, lineage, and consistency between research and serving workflows.

Current prompts implement controlled foundations only. Prompt 13 adds Data Quality + Validation Framework contracts and local deterministic validators. It does not implement real production worker loops, market-data ingestion, external provider clients, scraping, production dashboards, analytics engines, analytics signals, feature computation, Feast integration, production Kafka/Redpanda pipelines, production validation pipelines, broker integrations, automatic ClickHouse table creation, or execution APIs.
