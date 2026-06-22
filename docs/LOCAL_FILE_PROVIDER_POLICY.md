# Local File Provider Policy

The Local File Provider is allowed only as a local-file-only test/dev adapter. It is not a real provider implementation, not a production ingestion pipeline, and not proof that any provider is approved.

## Rules

- Explicit file paths only.
- Files must remain under the configured allowed root.
- No auto-discovery.
- No network paths.
- No scraping.
- No credentials.
- No provider SDKs.
- No real market data claims.
- No arbitrary file read API.
- No persistence writes from provider responses.
- No Redis, Redis Streams, Kafka, ClickHouse, TimescaleDB, DuckDB, or Parquet production writes.
- No analytics, features, trading signals, recommendations, decisions, backtests, or execution APIs.

## Data Labels

Every source and response must retain local/test/dev semantics. The default source label and source reference is `local-file-test-dev-only`.

Local file input is not trusted real market data by default. It may only be used to exercise local parsing, provider request/response contracts, path safety, and validation behavior.

## API Boundary

Prompt 24 exposes health and contract endpoints only:

- `/local-file-provider/health`
- `/local-file-provider/contracts`

These endpoints do not read files and do not accept caller-supplied paths. File reading is service/test-level only in Prompt 24. This is a no arbitrary file read API policy.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
