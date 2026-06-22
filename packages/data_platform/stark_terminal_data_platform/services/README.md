# Services

This package contains service-layer orchestration around repositories and validators.

Prompt 15 adds `InstrumentMetadataService` for validation-before-persistence, idempotent synthetic instrument seeding, and safe repository health checks. The service persists instrument metadata only. It does not ingest market data, persist OHLCV bars, call providers, publish events, compute analytics, or expose execution APIs.

Prompt 16 adds `MarketDataBatchMetadataService` for validation-before-persistence, synthetic/local batch metadata persistence, and safe repository health checks. The service persists batch metadata only. It does not ingest market data, persist full OHLCV bars, write TimescaleDB/ClickHouse/DuckDB/Parquet production stores, publish events, call providers, compute analytics, or expose execution APIs.

Prompt 18 adds `SyntheticOHLCVStorageService` for validation-before-storage and synthetic-only OHLCV bar persistence through the existing time-series ORM. It stores no real market data, requires synthetic/local/test source semantics, expects `LOCAL_SAMPLE` provider identity, publishes no events, computes no analytics/signals, and exposes no execution APIs.

Prompt 19 keeps export orchestration in `exports/` rather than this services package. `SyntheticOHLCVResearchLakeExportService` validates stored synthetic bars before writing explicit temp/test Parquet artifacts with DatasetManifest linkage and DuckDB readback. It makes no external calls, exports no real market data, computes no analytics/signals, and exposes no execution APIs.
