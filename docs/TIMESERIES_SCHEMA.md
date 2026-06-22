# Time-Series Schema

Prompt 03 adds operational time-series storage contracts. These are PostgreSQL-compatible SQLAlchemy models designed for future TimescaleDB hypertables. They do not ingest data and do not implement analytics or decision logic.

## OHLCVBarORM

`OHLCVBarORM` stores operational OHLCV bars by instrument, timeframe, timestamp, provider, quality status, and source data reference. It maps to and from the Prompt 01 `MarketDataBar` domain model.

## OptionsChainSnapshotORM

`OptionsChainSnapshotORM` stores snapshot-level options-chain metadata: underlying, expiry, timestamp, provider, contract count, quality status, and a safe payload summary. Full normalized strike/contract-level storage is intentionally deferred to a later Options/F&O prompt. Full `to_domain()` reconstruction is intentionally not implemented because the normalized option-contract table does not exist yet.

## FuturesBasisSnapshotORM

`FuturesBasisSnapshotORM` stores future basis snapshots by underlying, contract symbol, expiry, timestamp, optional spot/futures prices, basis, provider, quality status, and source data reference. It does not implement pricing logic.

## MarketStateSnapshotORM

`MarketStateSnapshotORM` stores generated market-state history placeholders such as state, regime, action state, confidence, risk, source, payload, and source data reference. It does not implement regime detection or decision generation.

## RegimeSnapshotORM

`RegimeSnapshotORM` stores future regime-engine output history: regime label, confidence, method, model or rule version, evidence, timestamp, and source data reference. It does not implement a regime engine.

## Operational Store vs Research Lake

Operational time-series storage is optimized for recent and replayable application workflows in PostgreSQL/TimescaleDB. The future DuckDB + Parquet research lake will hold reproducible research datasets, offline experiments, feature-ready datasets, backtest-ready partitions, and research artifacts.

## Snapshot Storage vs Analytics Logic

Snapshot tables store facts or generated outputs with timestamps and source references. They do not decide, predict, price, trade, or backtest. Analytics and decision logic remain separate future systems.

## Prompt 16 Boundary

Prompt 16 does not store OHLCV bars in TimescaleDB. Market Data Batch Persistence records batch metadata only in PostgreSQL-ready metadata tables. Full operational OHLCV storage remains deferred to a future explicit TimescaleDB prompt after provider adapters, validation gates, and data policy review.

## Prompt 17 Readiness Check

Prompt 17 confirms TimescaleDB has not yet received synthetic or real OHLCV bars. The next phase may add TimescaleDB Synthetic OHLCV Storage Foundation, but that phase must remain synthetic-only, validation-gated, and local-testable. Real ingestion remains forbidden until provider adapter guardrails, validation gates, source reference policy, and data-policy review are complete.

## Prompt 18 Synthetic OHLCV Storage Boundary

Prompt 18 uses `OHLCVBarORM` through `OHLCVBarRepository` and `SyntheticOHLCVStorageService` for synthetic-only bars. Stored synthetic bars retain instrument, timeframe, timestamp, provider, quality status, and source data reference.

This is not production ingestion. It does not store real market data, call providers, scrape, create hypertables, require live TimescaleDB in tests, compute analytics, generate trading signals, generate decisions, or expose execution APIs. Real operational OHLCV ingestion remains a future provider-gated prompt.
