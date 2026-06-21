# ClickHouse Warehouse Package

This package contains the ClickHouse analytical warehouse foundation.

Prompt 09 does not ingest real data, create real ClickHouse tables automatically, run production dashboards, compute analytics, or implement execution APIs. DDL helpers return SQL strings only.

ClickHouse is the analytical warehouse, not the system of record. PostgreSQL remains the system of record, TimescaleDB remains the operational time-series store, and DuckDB/Parquet remains the research lake.

The memory query recorder is for local/test fallback only. It is not a real warehouse and must not be treated as durable storage.
