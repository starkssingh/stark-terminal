# Batch Metadata Policy

Prompt 16 defines the policy for batch metadata records. Batch metadata supports auditability and local deterministic tests; it is not full OHLCV storage and not real market data ingestion.

## Batch Identity

Each metadata record has a stable `batch_id`. Persistence is idempotent by `batch_id`, so repeated writes update the same metadata record instead of creating duplicates.

Batch identity must be safe to log and return through read-only API endpoints. It must not contain secrets, raw URLs, provider credentials, broker credentials, tokens, or execution-related values.

## Source References

`source_data_reference` is required. It explains where the batch metadata came from without exposing credentials or raw sensitive URLs.

Synthetic records must use a reference that clearly includes synthetic/local/test or dev semantics. A synthetic fixture reference may link to a fixture catalog entry through `fixture_id`.

## Metadata Fields

Batch metadata includes:

- `instrument_id`
- `timeframe`
- provider identity when available
- `quality_status`
- `row_count`
- `start_timestamp`
- `end_timestamp`
- `source_data_reference`
- `synthetic`
- `fixture_id`
- `dataset_manifest_id`
- `validation_report_id`
- `schema_version`
- `created_at`
- sanitized notes

`row_count`, `start_timestamp`, and `end_timestamp` describe the validated batch. They do not imply full bars are stored in PostgreSQL.

## Linkage

`fixture_id` links local synthetic fixture metadata to the batch metadata record. `validation_report_id` links the batch metadata to Data Quality Framework output. `dataset_manifest_id` is reserved for later explicit dataset metadata wiring.

## Storage Boundary

The `market_data_batch_records` table stores no full OHLCV bars. It must not contain open, high, low, close, volume, tick history, provider payloads, options chain payloads, trading signals, recommendations, broker data, order data, or execution state.

Full operational bar storage remains a later TimescaleDB prompt. Research storage remains DuckDB/Parquet. Analytical copies remain ClickHouse. Event publishing remains Redis Streams or Kafka/Redpanda prompts.

## Safety Rules

- no real market ingestion.
- no external calls.
- no provider network calls.
- no scraping.
- no secrets in errors or API responses.
- no market-data batch metadata as trade signal.
- no execution APIs.

Development and tests run on Mac mini M2 / macOS / Apple Silicon, and the target desktop product remains Windows-native Stark Terminal.
