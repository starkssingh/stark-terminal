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
