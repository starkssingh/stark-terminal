# Instrument Metadata Persistence Foundation

Prompt 15 wires instrument metadata into the existing PostgreSQL-ready SQLAlchemy foundation through an explicit repository and service layer.

## Purpose

Instrument metadata persistence gives Stark Terminal a first system-of-record path for canonical instruments. PostgreSQL remains the intended production system of record, while SQLite fallback remains available for local tests and development through the existing database foundation.

This foundation persists instrument metadata only:

- symbol, exchange, and segment identity
- display name, asset class, status, lot size, and tick size
- optional classification metadata such as ISIN, sector, and industry
- synthetic/local fixture metadata for deterministic tests

It does not persist OHLCV bars, options-chain history, provider payloads, analytics outputs, features, decisions, orders, or broker data.

## Repository And Service Split

`InstrumentRepository` owns SQLAlchemy persistence operations using a caller-provided `Session`. It does not create engines, create tables, commit automatically, make external calls, or hold global state.

`InstrumentMetadataService` owns validation-before-persistence, commit/rollback boundaries, synthetic seed behavior, and health reporting. The service uses the Data Quality `InstrumentValidator` before writing when validation is required.

## Identity And Idempotency

Persistence is idempotent on:

```text
symbol + exchange + segment
```

Lookups normalize symbol, exchange, and segment using the existing symbol normalization helpers. Upserting the same instrument identity updates metadata rather than creating duplicates.

## Synthetic Seeding

Synthetic fixture seeding uses `create_sample_instruments()` and is local/test/dev only. Seeded instruments are synthetic, not live market data, not trading data, not investment advice, and have no external provider source.

## Boundaries

- no real market ingestion
- no external calls
- no NSE/BSE scraping
- no provider-specific live clients
- no OHLCV persistence
- no broker/execution behavior
- no execution APIs

Future real provider adapters must pass data-policy review and validation gates before any production instrument metadata ingestion is implemented.

## Platform

Development and tests run on Mac mini M2 / macOS / Apple Silicon. The target desktop product remains Windows-native Stark Terminal.
