# Database Foundation

Prompt 02 implements the PostgreSQL + SQLAlchemy + Alembic persistence foundation for Stark Terminal metadata. Prompt 03 extends that foundation with TimescaleDB-oriented operational tables while keeping PostgreSQL as the metadata system of record.

## System Of Record

PostgreSQL remains the system of record for durable relational metadata. It will hold instruments, provider identities, audit records, decision-object metadata, configuration state, and future research control records. TimescaleDB extends PostgreSQL for operational time-series workloads; it does not replace PostgreSQL's metadata role.

## ORM And Migrations

SQLAlchemy 2.x is the ORM foundation. Alembic is the migration system. Schema changes must go through migrations rather than ad hoc table creation in application code.

Prompt 02 uses `psycopg[binary]` as the PostgreSQL driver dependency. It is modern psycopg 3 packaging with binary wheels suitable for this foundation stage.

## SQLite Fallback

SQLite fallback is for local tests/dev only when `DATABASE_URL` is not configured. It lets unit tests validate SQLAlchemy metadata, mapping helpers, and health checks without requiring a running PostgreSQL server.

## Sensitive Configuration

`DATABASE_URL` is sensitive and must never be exposed by API responses, logs, docs examples with credentials, or test snapshots. Public API responses expose only boolean configuration status.

## Prompt 02 Scope

Implemented metadata tables:

- `instruments`
- `data_providers`
- `audit_records`
- `decision_object_records`

Prompt 02 does not implement TimescaleDB hypertables yet. It does not implement market data ingestion, OHLCV storage, options-chain storage, Redis, Kafka, ClickHouse, DuckDB, Parquet, quant analytics, backtesting, broker integrations, execution/trading APIs, or any execution APIs. There are no execution APIs in the Prompt 02 database foundation.

## Prompt 03 Extension

Prompt 03 adds operational time-series tables and TimescaleDB extension/hypertable migration planning. It still does not implement market data ingestion or require a running TimescaleDB server for tests.

## Current Extension Path

Prompt 03 extended the PostgreSQL foundation with TimescaleDB-oriented operational time-series schemas and migration planning. Prompt 04 then added the DuckDB + Parquet research lake foundation. Market data ingestion remains intentionally not implemented.

## Prompt 15 Instrument Repository Wiring

`InstrumentORM` is now wired through `InstrumentRepository` and `InstrumentMetadataService`. PostgreSQL remains the intended system of record, while SQLite supports local tests and development. The repository uses a caller-provided SQLAlchemy `Session`, performs idempotent upsert by symbol, exchange, and segment, and does not create engines or commits at import time.

This is metadata-only persistence. It does not persist OHLCV bars, call external providers, run ingestion, or expose execution APIs.

## Prompt 16 Batch Metadata Table

Prompt 16 adds `market_data_batch_records` through `MarketDataBatchRecordORM` and Alembic migration `0003_market_data_batch_metadata.py`.

The table stores batch metadata only: batch id, instrument identity, timeframe, provider identity, quality status, row count, start/end timestamps, source reference, synthetic flag, fixture linkage, dataset manifest linkage, validation report linkage, schema version, and sanitized notes. It has a unique constraint on `batch_id` and indexes for instrument/time range and synthetic fixture lookup.

The table stores no full OHLCV bars and does not replace TimescaleDB operational bar storage, DuckDB/Parquet research storage, or ClickHouse analytical copies. No tables are created automatically at import time, and no external calls or execution APIs are introduced.

## Prompt 17 Data Foundation Audit Note

Prompt 17 confirms the database layer remains metadata-only after Prompts 14-16. `InstrumentRepository` persists canonical instrument metadata, and `MarketDataBatchRepository` persists batch metadata. Neither repository stores full OHLCV bars, performs real market ingestion, calls external providers, scrapes, publishes events, writes analytical/research stores, generates signals, or exposes execution APIs.
