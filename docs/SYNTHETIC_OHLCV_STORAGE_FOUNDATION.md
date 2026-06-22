# Synthetic OHLCV Storage Foundation

Prompt 18 implements the Stark Terminal TimescaleDB Synthetic OHLCV Storage Foundation.

The purpose is to wire deterministic synthetic OHLCV fixtures into the existing operational time-series ORM so later prompts can test storage, query, and export workflows without real market data ingestion. TimescaleDB remains the intended operational time-series layer, while SQLite remains the local development and test fallback. The foundation uses the existing `OHLCVBarORM`, `MarketDataBar`, `MarketDataBatch`, and Data Quality validators.

This is synthetic-only operational storage. It is not live market data ingestion, not provider ingestion, not a production market data pipeline, and not a trading system.

Implemented scope:

- `OHLCVBarRepository` for explicit SQLAlchemy session-scoped bar upsert/query operations.
- `SyntheticOHLCVStorageService` for validation-before-storage and synthetic-only storage boundaries.
- Idempotent upsert identity: instrument_id + timeframe + timestamp + provider_id.
- SQLite-compatible tests that do not require live TimescaleDB.
- Safe API health/sample/contracts endpoints under `/synthetic-ohlcv-storage`.
- Validation through `MarketDataBarValidator` before storage.

Storage rules:

- Stored bars must be synthetic.
- Stored bars must carry a synthetic/local/test `source_data_reference`.
- Stored bars are expected to carry `LOCAL_SAMPLE` provider identity.
- Stored bars must pass deterministic Data Quality validation.
- Stored bars must not be treated as real market data, tradable data, signals, recommendations, or investment advice.
- The service stores no analytics, features, regimes, decisions, backtest results, or trading signals.

Prompt 18 does not:

- ingest real market data;
- call NSE, BSE, broker, vendor, or provider APIs;
- scrape any website;
- execute TimescaleDB-specific SQL or create hypertables;
- require TimescaleDB in tests;
- write ClickHouse, DuckDB/Parquet, Redis, Redis Streams, or Kafka;
- compute analytics, indicators, features, regimes, backtests, signals, or decisions;
- expose execution APIs.

Store responsibilities remain unchanged:

- PostgreSQL remains the metadata/system-of-record store.
- TimescaleDB is the intended operational OHLCV/time-series store.
- DuckDB/Parquet remains the research lake path.
- ClickHouse remains the analytical warehouse copy path.
- Redis remains cache only.
- Redis Streams and Kafka/Redpanda remain event coordination/backbone systems only.

The future path to real ingestion requires provider adapters, data policy review, validation gates, source auditability, and explicit prompt approval. Prompt 18 is only the synthetic storage foundation.

## Prompt 19 Research Lake Export Linkage

Prompt 19 adds a synthetic-only export contract from stored synthetic bars to DuckDB/Parquet research artifacts. The export path uses `SyntheticOHLCVResearchLakeExportService`, DatasetManifest creation, validation-before-export, temporary Parquet writes in tests, and DuckDB readback verification.

Stored synthetic bars may be exported only as synthetic/local/test artifacts. The export path does not ingest real market data, call external providers, scrape, compute analytics, generate trading signals, generate decisions, or expose execution APIs.

Development and platform status:

- Development environment: Mac mini M2 / macOS / Apple Silicon.
- Target desktop product: Windows-native Stark Terminal.
- Backend target: Oracle Cloud deployment.
- Execution APIs: forbidden.
