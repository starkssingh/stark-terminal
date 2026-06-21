# Analytical Table Contracts

Analytical table contracts define the intended ClickHouse warehouse tables before ingestion exists. They are schema contracts and DDL inputs only.

## Tables

### analytical_ohlcv_bars

Stores future analytical OHLCV copies for historical scans. Ordered by exchange, segment, symbol, timeframe, and timestamp. Partitioned by `toYYYYMM(timestamp)`.

### analytical_options_chain_snapshots

Stores future snapshot-level options-chain history. Ordered by exchange, underlying symbol, expiry, and timestamp. Partitioned by `toYYYYMM(timestamp)`.

### analytical_futures_basis_snapshots

Stores future analytical futures-basis history. Ordered by exchange, underlying symbol, contract symbol, expiry, and timestamp. Partitioned by `toYYYYMM(timestamp)`.

### analytical_market_state_snapshots

Stores future analytical market-state snapshots. Ordered by exchange, segment, symbol, timeframe, and timestamp. Partitioned by `toYYYYMM(timestamp)`.

### analytical_regime_snapshots

Stores future analytical regime history. Ordered by exchange, segment, symbol, timeframe, and timestamp. Partitioned by `toYYYYMM(timestamp)`.

### analytical_decision_objects

Stores future analytical DecisionObject history. Ordered by exchange, segment, instrument, timeframe, and generated timestamp. Partitioned by `toYYYYMM(generated_at)`.

## Difference From TimescaleDB

TimescaleDB is the operational time-series store for application workflows and recent/replayable time-series state. ClickHouse is the analytical warehouse for large scans, aggregate-heavy workloads, and future dashboard acceleration.

## Difference From DuckDB / Parquet

DuckDB and Parquet provide reproducible local research lake workflows. ClickHouse provides a server-side analytical warehouse target for high-speed shared analytical queries.

## Scope Boundary

Prompt 09 creates table contracts only. There is no real market data ingestion, no automatic table creation, no production dashboard analytics, and no execution APIs.
