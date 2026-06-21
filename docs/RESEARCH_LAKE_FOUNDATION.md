# Research Lake Foundation

DuckDB + Parquet are Stark Terminal's research lake foundation. PostgreSQL remains the system of record for metadata and durable relational state. TimescaleDB remains the operational time-series store for application-facing market history and generated snapshots.

The research lake is for reproducible analytical datasets: local research slices, feature-ready data, backtest-ready datasets, experiment artifacts, cross-sectional scans, and future quant workflows.

## Prompt 04 Scope

Prompt 04 implements lake contracts and helpers only:

- Data lake zone contracts
- Path helpers using `pathlib`
- Dataset manifest schemas
- In-memory dataset registry placeholder
- Parquet read/write helpers
- DuckDB local query helpers
- Research lake health checks

Prompt 04 does not implement market data ingestion, provider clients, actual NSE/BSE loading, analytics engines, model training, backtesting, broker integrations, or execution APIs. There are no execution APIs in this foundation.

## Test Data

Prompt 04 may use temporary synthetic data in tests only. Generated data files must not be checked into the repository.

## Registry

The dataset registry is an in-memory/file-contract placeholder. A persistent registry comes later, likely through PostgreSQL plus the Stark Feature Registry.

## Platform

Development currently runs on Mac mini M2 / macOS / Apple Silicon. The target desktop product remains Windows-native Stark Terminal. All paths should use `pathlib` and avoid macOS-specific or Windows-specific hardcoding.

## Current Extension Path

Prompt 05 implements the Redis Cache Foundation. Prompt 06 should add Redis Streams event pipeline contracts without market data ingestion.
