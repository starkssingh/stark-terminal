# DuckDB Foundation

DuckDB is Stark Terminal's embedded analytical engine for local research queries and Parquet scans.

## Role

DuckDB enables fast analytical reads over local Parquet datasets without requiring a running database server. It supports reproducible research workflows, cross-sectional scans, local joins, and future offline experiments.

## Difference From Other Stores

- PostgreSQL remains the system of record for metadata, audits, configuration, and durable relational state.
- TimescaleDB is the operational time-series store for application-facing market observations and generated snapshots.
- DuckDB is for embedded analytical research over local files.
- ClickHouse is still planned for future high-speed analytical warehouse workloads and is not implemented in Prompt 04.

## Prompt 04 Scope

Prompt 04 implements a local DuckDB client wrapper, query helpers, and Parquet scan helpers. It does not implement production dashboards, market data ingestion, analytics engines, backtests, model training, broker integrations, or execution APIs. There are no execution APIs in this foundation.

## Safety

DuckDB helpers are local only. Remote reads, provider clients, and unsafe SQL exposure through public APIs are out of scope.
