# Local Sample Provider Policy

The Local Sample Provider is one of the currently implemented safe provider adapters. It is allowed because it is synthetic, local-only, test/dev only, read-only, and uses no external provider source. Prompt 24 adds Local File Provider Adapter v0 as a second local/test/dev adapter.

## Rules

- Data source must be synthetic fixtures and local sample instruments only.
- Provider identity must be `LOCAL_SAMPLE`.
- Source reference must use synthetic/local/test semantics such as `synthetic-local-test-only`.
- Network calls are forbidden.
- Scraping is forbidden.
- Credentials are forbidden.
- Real market data is forbidden.
- Real latest-bar, options-chain, futures-chain, and corporate-action provider behavior is unsupported.
- Broker execution, order placement, live trading, real-money routing, and execution APIs are forbidden.
- Responses must not be interpreted as trading data, investment advice, analytics signals, features, decisions, or recommendations.

## Deterministic Bars

Historical bars are generated deterministically from explicit seed, instrument, timeframe, start timestamp, bar count, and start price settings. Supported synthetic timeframes are `DAILY`, `FIFTEEN_MINUTE`, and `FIVE_MINUTE`.

The adapter returns tiny synthetic responses for API samples. It does not write to PostgreSQL, TimescaleDB, DuckDB/Parquet, ClickHouse, Redis, Redis Streams, Kafka/Redpanda, or local data files.

## API Labeling

Local sample provider API responses must include safe labels:

- `synthetic: true` where applicable
- `real_market_data: false`
- `network_calls: false`
- `credentials_required: false`
- source reference `synthetic-local-test-only`

Prompt 21 adds no real provider implementation, no provider SDKs, no scraping dependencies, no credentials, no real market ingestion, no trading signals, and no execution APIs.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
