# Local File Provider Adapter

Prompt 24 implements Local File Provider Adapter v0 as a local-file-only, test/dev-only, read-only provider adapter.

This adapter is not a real provider and is not real market ingestion. It enforces no real market data claims. It makes no external calls, installs no provider SDK, performs no scraping, loads no credentials, writes no persistence stores, publishes no events, computes no analytics, generates no trading signals, generates no decisions, and exposes no execution APIs.

## Purpose

The Local File Provider gives Stark Terminal a controlled way to exercise provider-shaped `MarketDataRequest` and `MarketDataResponse` contracts against explicitly supplied local files before any real provider integration exists.

Supported file formats:

- CSV
- Parquet

Supported capabilities:

- instrument master
- historical bars
- health check

Unsupported capabilities:

- real latest bar
- real options chain
- real futures chain
- corporate actions
- broker execution
- order placement
- credential loading
- provider account access

## Adapter Behavior

`LocalFileProviderAdapter` accepts a `LocalFileSource` object and reads that explicit source only. It does not auto-discover files, scan directories, read network paths, or expose arbitrary file reads through HTTP.

Instrument master files must include `symbol`, `exchange`, `segment`, `display_name`, and `asset_class`. Historical OHLCV files must include `symbol`, `exchange`, `segment`, `timeframe`, `timestamp`, `open`, `high`, `low`, and `close`.

Every response is labelled `local-file-test-dev-only`, reports `real_market_data: false` where surfaced by APIs, and must not be presented as live, tradable, production, provider-sourced, or investment data.

## Guardrails And Validation

The adapter evaluates Prompt 20 provider guardrails before use. The only allowed mode is local file test/dev operation with no network, no scraping, no credentials, no real-data claims, and no execution behavior.

Responses use the Data Quality Framework where practical. Invalid local file rows return sanitized errors instead of successful responses.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
