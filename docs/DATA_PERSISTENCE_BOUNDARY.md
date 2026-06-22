# Data Persistence Boundary

Prompt 19 consolidates the data movement boundary after adding synthetic-only OHLCV research lake export.

## Persisted Today

Stark Terminal currently persists metadata plus synthetic-only OHLCV bars:

- Instrument metadata through `InstrumentRepository` and `InstrumentMetadataService`.
- Market data batch metadata through `MarketDataBatchRepository` and `MarketDataBatchMetadataService`.
- Synthetic-only OHLCV bars through `OHLCVBarRepository` and `SyntheticOHLCVStorageService`.

All layers are validation-gated and use SQLAlchemy models with SQLite fallback for local tests/dev. Synthetic OHLCV storage uses the existing TimescaleDB-oriented ORM but does not require live TimescaleDB in tests.

## Not Persisted Today

The current repository does not persist:

- real market data.
- full OHLCV production bars or real OHLCV bars.
- provider-ingested datasets.
- provider-native payloads.
- strategy outputs.
- trading decisions.
- trading recommendations.
- analytics signals.
- broker credentials.
- order or execution records.

Prompt 16 stores batch metadata only. It does not store full bars in `market_data_batch_records`. Prompt 18 stores synthetic bars only through the synthetic OHLCV storage service.

## Store Ownership

- PostgreSQL: metadata system of record for instruments, provider metadata, audits, DecisionObject records, and batch metadata.
- TimescaleDB: intended operational OHLCV and time-series storage. It now has synthetic-only ORM/repository/service wiring; real ingestion remains future.
- DuckDB/Parquet: future research datasets and reproducible research lake storage. Prompt 14 Parquet writes are explicit, tiny, and temp/test-only.
- ClickHouse: future analytical warehouse copies. No production analytical ingestion exists.
- Redis: cache only, not durable truth.
- Redis Streams: lightweight event coordination only, not durable truth.
- Kafka/Redpanda: durable event backbone contracts only, not durable truth and no production pipelines.

No store currently receives real market data.

## Boundary Rules

- Instrument metadata persistence must not store OHLCV bars.
- Market data batch metadata persistence must not store full OHLCV bars.
- Synthetic OHLCV storage must not store real market data.
- Repositories and services must not call external providers.
- Repositories and services must not scrape NSE/BSE.
- Repositories and services must not publish Redis, Redis Streams, Kafka, or Redpanda events.
- Repositories and services must not write production TimescaleDB, ClickHouse, DuckDB, or Parquet datasets. Prompt 18 synthetic OHLCV writes are local/test/dev synthetic-only and validation-gated.
- Metadata persistence must not produce signals, decisions, recommendations, orders, or execution behavior.

## Next Boundary

Prompt 19 implements synthetic OHLCV to Research Lake Export Contract using Prompt 13 validation gates, Prompt 14 synthetic fixtures, and Prompt 18 synthetic storage only. It writes Parquet only when explicitly called with a safe path and creates DatasetManifest linkage. Real ingestion remains forbidden until a future provider adapter guardrail prompt explicitly approves it.
