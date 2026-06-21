# Services

This package contains service-layer orchestration around repositories and validators.

Prompt 15 adds `InstrumentMetadataService` for validation-before-persistence, idempotent synthetic instrument seeding, and safe repository health checks. The service persists instrument metadata only. It does not ingest market data, persist OHLCV bars, call providers, publish events, compute analytics, or expose execution APIs.

Prompt 16 adds `MarketDataBatchMetadataService` for validation-before-persistence, synthetic/local batch metadata persistence, and safe repository health checks. The service persists batch metadata only. It does not ingest market data, persist full OHLCV bars, write TimescaleDB/ClickHouse/DuckDB/Parquet production stores, publish events, call providers, compute analytics, or expose execution APIs.
