# Synthetic OHLCV Research Lake Export

Prompt 19 implements the Synthetic OHLCV Research Lake Export Contract for Stark Terminal.

This foundation exports validated synthetic-only OHLCV bars from the Prompt 18 synthetic storage repository to temporary Parquet research artifacts. The export creates a `DatasetManifest`, validates bars before writing, and verifies that exported Parquet can be read back with DuckDB.

## Scope

- Source: synthetic-only OHLCV storage from `OHLCVBarRepository`.
- Output: Parquet research artifact with `DatasetManifest` linkage.
- Validation: validation-before-export through the Data Quality Framework and `MarketDataBarValidator`.
- Filesystem posture: temp/test-only by default; production research lake writes are disabled unless an explicit safe output path is passed.
- Platform posture: developed on Mac mini M2 / macOS / Apple Silicon and kept portable for a Windows-native Stark Terminal target.

## Explicit Non-Scope

Prompt 19 does not implement real market data ingestion, provider API calls, scraping, analytics indicators, feature computation, regimes, decisions, trading signals, backtests, broker behavior, or execution APIs. The policy phrase for this phase is no real market ingestion.

Synthetic OHLCV exports are not real market data, not live market data, not tradable data, not investment advice, and not provider-sourced datasets. The export policy is no real market data.

## Store Boundaries

- TimescaleDB/SQLite synthetic storage remains the operational synthetic bar source.
- DuckDB/Parquet remains the research lake artifact layer.
- PostgreSQL remains metadata/system-of-record foundation.
- ClickHouse, Redis, Redis Streams, and Kafka/Redpanda are not written by Prompt 19.

## Future Path

Future real-data export can only happen after provider adapters, provider capability approval, data policy review, source auditability, validation gates, and explicit prompt approval exist. Prompt 19 is a synthetic-only contract.
