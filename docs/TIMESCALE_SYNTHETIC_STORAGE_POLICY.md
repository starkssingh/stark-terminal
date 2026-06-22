# Timescale Synthetic Storage Policy

Prompt 18 adds a synthetic-only TimescaleDB OHLCV storage policy for Stark Terminal.

The policy exists to keep the new `OHLCVBarRepository` and `SyntheticOHLCVStorageService` inside a narrow test/dev boundary. The service may store generated synthetic OHLCV bars through the existing `OHLCVBarORM`, but it must not store real market data or claim production ingestion.

Required storage posture:

- Synthetic OHLCV Storage only.
- `stores_real_data` must remain false.
- `source_data_reference` must include synthetic/local/test semantics.
- Provider identity should be `LOCAL_SAMPLE` where practical.
- Validation-before-storage is required.
- SQLite is allowed for local tests and development.
- TimescaleDB is not required for tests.
- No hypertable creation is performed by Prompt 18.
- No TimescaleDB-specific SQL is executed by Prompt 18.

Forbidden behavior:

- no real market data;
- no real market ingestion;
- no external calls;
- no NSE/BSE/provider API calls;
- no scraping;
- no event publishing;
- no ClickHouse, DuckDB/Parquet, Redis, Kafka, or Redis Streams writes;
- no analytics from stored bars;
- no trading signals;
- no decision generation;
- no execution APIs.

Difference from future production ingestion:

Prompt 18 proves the repository/service boundary and idempotent storage contract using synthetic data. Future production TimescaleDB ingestion must be implemented only after provider adapters, validation gates, data policy review, lineage/source tracking, and explicit safety approval exist. Real provider data must not enter this storage path until that future prompt.

Prompt 19 may export stored synthetic bars to DuckDB/Parquet research artifacts through a validation-before-export contract. This remains synthetic-only and does not change the future production ingestion boundary.

The storage identity is deterministic:

`instrument_id + timeframe + timestamp + provider_id`

This identity supports idempotent synthetic fixture writes during tests/dev. It does not imply that the service is a production data loader.

Development and platform status:

- Development environment: Mac mini M2 / macOS / Apple Silicon.
- Target desktop product: Windows-native Stark Terminal.
- Backend target: Oracle Cloud deployment.
- Execution APIs: forbidden.
