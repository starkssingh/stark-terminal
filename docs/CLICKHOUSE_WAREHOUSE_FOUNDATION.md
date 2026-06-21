# ClickHouse Warehouse Foundation

ClickHouse is Stark Terminal's analytical warehouse layer. It is intended for high-speed historical scans, cross-sectional analytics, dashboard query acceleration, and future analytical rollups.

## Role

ClickHouse is not the system of record. PostgreSQL remains the system of record for durable metadata and audit records. TimescaleDB remains the operational time-series layer. DuckDB and Parquet remain the research lake. Redis and Redis Streams remain cache and lightweight event foundations.

## Prompt 09 Scope

Prompt 09 implements:

- ClickHouse configuration contracts.
- Analytical table contracts.
- DDL helpers that return SQL strings only.
- ClickHouse client wrapper with disabled-safe behavior.
- Memory query recorder for local/test fallback.
- Warehouse health checks.
- API warehouse health and contracts endpoints.

Prompt 09 does not ingest real data, connect to market providers, create real ClickHouse tables automatically, implement dashboards, run analytics engines, create production rollups, or expose execution APIs.

## Local And Test Behavior

Prompt 09 does not require ClickHouse locally. When ClickHouse is disabled and `CLICKHOUSE_USE_MEMORY_FALLBACK=true`, the warehouse client uses a local memory query recorder. The recorder is local/test-only and is not a real warehouse.

## Boundaries

DDL helpers return SQL only. Application imports, health checks, and API contract endpoints do not create tables. Real analytical ingestion requires a future explicit prompt and data policy review.

## Next Step

Prompt 10 should implement Feature Store / Stark Feature Registry Foundation.
