# Warehouse Query Policy

ClickHouse warehouse queries must remain analytical, explicit, and safe.

## Rules

- Do not put secrets, credentials, tokens, API keys, raw URLs, ClickHouse passwords, broker tokens, or provider credentials in queries.
- Do not create execution, broker, order, or live-trading data routes.
- Do not create tables automatically from imports, health checks, API routes, or application startup.
- DDL helpers return SQL only.
- Analytical queries must not become trade calls.
- Query code must remain read/analytical unless a future explicit write prompt defines ingestion.
- Production dashboard analytics are deferred.

## Store Boundaries

ClickHouse is analytical warehouse storage. PostgreSQL remains system of record, TimescaleDB remains operational time-series storage, and DuckDB/Parquet remains the research lake.

## Prompt 09 Boundary

Prompt 09 does not ingest market data, run production analytics, build dashboards, create real ClickHouse tables automatically, or implement execution APIs.
