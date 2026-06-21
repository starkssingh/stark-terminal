# Instrument Repository Policy

Prompt 15 introduces metadata-only instrument persistence policy for `InstrumentRepository` and `InstrumentMetadataService`.

## Repository Responsibilities

`InstrumentRepository`:

- accepts an explicit SQLAlchemy `Session`
- performs idempotent upsert by normalized symbol, exchange, and segment
- supports get, get-by-id, list, search, count, and optional delete
- returns domain `Instrument` objects
- avoids global sessions and engine creation at import time
- avoids automatic commits so transaction ownership stays explicit

## Service Responsibilities

`InstrumentMetadataService`:

- runs validation-before-persistence through the Data Quality `InstrumentValidator`
- blocks writes when validation fails
- owns commit and rollback boundaries
- supports idempotent synthetic fixture seeding for local/test/dev use
- reports safe repository health without exposing database URLs

## Lookup And Validation Rules

All repository lookups normalize symbol, exchange, and segment before querying. Validation is required by default through `instrument_persistence_require_validation=true`.

Synthetic fixture seeding is allowed by default for local development and tests through `instrument_persistence_allow_synthetic_seed=true`; it does not imply real market ingestion.

## Transaction Policy

Repository methods flush through the provided session but do not commit. Service methods commit successful writes and roll back failed writes. API read endpoints do not seed or create tables automatically.

## Safety Boundaries

- no external calls from repositories or services
- no secrets in errors or API responses
- no market-data bars in instrument metadata persistence
- no real market ingestion
- no broker credential persistence
- no order placement
- no execution APIs

Instrument metadata persistence is a system-of-record metadata foundation only. It must never become a trade route, market-data fetcher, or broker integration.
