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
