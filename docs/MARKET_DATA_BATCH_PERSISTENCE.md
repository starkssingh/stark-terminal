# Market Data Batch Persistence

Prompt 16 adds Market Data Batch Persistence Contracts for validated synthetic/local `MarketDataBatch` metadata. This is a metadata-only persistence foundation for auditability, fixture linkage, source references, row counts, time ranges, quality status, and validation report references.

This prompt does not persist full OHLCV bars. It does not implement real market ingestion, external provider calls, NSE/BSE scraping, TimescaleDB writes, DuckDB/Parquet production writes, ClickHouse analytical writes, Redis/Kafka event publishing, analytics engines, feature computation, signals, decisions, or execution APIs.

## Role

PostgreSQL remains the intended system of record. The existing SQLite fallback remains available for deterministic local tests and development on Mac mini M2 / macOS / Apple Silicon while the target desktop product remains Windows-native Stark Terminal.

Prompt 16 creates the first batch metadata contract:

- `MarketDataBatchMetadata`: batch identity, instrument, timeframe, provider, quality status, row count, start/end timestamps, source reference, synthetic flag, fixture linkage, dataset manifest linkage, validation report linkage, schema version, creation time, and notes.
- `MarketDataBatchPersistenceResult`: safe result contract for metadata persistence attempts.
- `MarketDataBatchRecordORM`: SQLAlchemy metadata table mapping for `market_data_batch_records`.
- `MarketDataBatchRepository`: explicit batch metadata upsert/get/list/search/count/delete operations.
- `MarketDataBatchMetadataService`: validation-before-persistence, synthetic/local helper flow, commit/rollback ownership, and health status.

## Persistence Boundary

The table stores batch metadata only. It does not store open, high, low, close, volume, open interest, options chains, tick data, provider payloads, or production history.

Future storage ownership remains separated:

- TimescaleDB remains the future operational OHLCV bar store.
- DuckDB/Parquet remains the future research lake storage path.
- ClickHouse remains the future analytical copy and scan layer.
- Redis Streams and Kafka/Redpanda remain event foundations, not batch metadata truth.

## Validation

Prompt 16 uses validation-before-persistence through the Data Quality Framework. Synthetic fixture batches from Prompt 14 can be converted to `MarketDataBatchMetadata` and persisted in local/test/dev contexts only when validation passes.

Validation failure blocks persistence. Metadata persistence must not silently pass failed data, and no validation gate can become a trade call.

## Safety

Market data batch metadata persistence is not a market-data ingestion system. It makes no external calls, creates no provider client, persists no real production market data, and stores no secrets.

Synthetic batch metadata must remain clearly labeled synthetic, local-only, and test/dev only. It is not real market data, not trading data, and not investment advice.

Execution APIs remain forbidden.

## Prompt 18 Synthetic Storage Linkage

Prompt 18 allows validated synthetic `MarketDataBatch` bars to be stored through the synthetic-only OHLCV storage service. Batch metadata can conceptually link to storage results through batch ids, fixture ids, source references, and validation report ids.

This does not change the Prompt 16 boundary: `market_data_batch_records` still stores metadata only and no full bars. Prompt 18 does not implement production ingestion, external provider calls, ClickHouse writes, DuckDB/Parquet production writes, event publishing, analytics, signals, decisions, or execution APIs.
