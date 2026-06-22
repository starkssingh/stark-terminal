# TimescaleDB Foundation

TimescaleDB is Stark Terminal's operational time-series layer. PostgreSQL remains the system of record for metadata, audit records, configuration, instruments, and durable relational state.

Prompt 03 implements schema foundation and migration planning only. It prepares operational tables for market time-series workloads with no market data ingestion, provider clients, analytics engines, or execution APIs.

## Testing And Deployment

Prompt 03 does not require TimescaleDB locally for tests. SQLite fallback remains available for tests/dev metadata checks. Actual deployment needs PostgreSQL with the TimescaleDB extension installed and explicitly enabled through configuration.

## Hypertable Candidates

- `ohlcv_bars`
- `options_chain_snapshots`
- `futures_basis_snapshots`
- `market_state_snapshots`
- `regime_snapshots`

The Alembic migration creates ordinary PostgreSQL-compatible tables first. TimescaleDB extension and hypertable conversion SQL is opt-in and guarded for PostgreSQL deployments.

## Scope Boundary

Prompt 03 does not implement market data ingestion, real NSE/BSE loading, provider-specific clients, Redis, Kafka, Redpanda, ClickHouse, DuckDB, Parquet, feature store, backtesting, regime engine logic, options pricing, ML pipelines, Paper Lab, broker integrations, or execution/trading APIs. There are no execution APIs in this foundation.

## Current Extension Path

Prompt 04 implements the DuckDB + Parquet research lake foundation. Market data ingestion remains intentionally not implemented.

## Prompt 18 Synthetic Storage Wiring

Prompt 18 wires `OHLCVBarORM` through `OHLCVBarRepository` and `SyntheticOHLCVStorageService` for synthetic-only OHLCV storage. This proves the repository/service boundary for operational bar storage without requiring live TimescaleDB in tests.

The Prompt 18 path is validation-gated, SQLite-compatible, and restricted to synthetic/local/test data with `LOCAL_SAMPLE` provider identity. It does not create hypertables, execute TimescaleDB-specific SQL, ingest real market data, call external providers, compute analytics, generate trading signals, generate decisions, or expose execution APIs.
