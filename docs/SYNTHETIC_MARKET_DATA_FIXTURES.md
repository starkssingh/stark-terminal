# Synthetic Market Data Fixtures

Prompt 14 implements deterministic synthetic market data fixtures for Stark Terminal tests and local development.

## Purpose

Synthetic fixtures provide tiny, reproducible OHLCV samples so future ingestion, validation, analytics, feature, backtest, and decision-support tests can run without real market data, provider APIs, scraping, or external services.

These fixtures are:

- synthetic
- local-only
- test/dev only
- not real market data
- not trading data
- not investment advice
- no external provider source

## Deterministic Generation

Synthetic OHLCV bars are generated with an explicit seed, timezone-aware UTC timestamps, stable instrument identity, `LOCAL_SAMPLE` provider metadata, and a source data reference of `synthetic-local-test-only`.

The default fixture settings keep row counts tiny. The same seed and configuration must produce the same bars. Different seeds may produce different synthetic bars.

## Scope Boundary

Prompt 14 does not implement real market data ingestion, NSE/BSE scraping, external provider calls, production data lake writes, TimescaleDB writes, ClickHouse writes, Kafka/Redis publishing, analytics indicators, feature computation, backtesting, regime detection, options pricing, ML models, signals, recommendations, or execution APIs.

Prompt 17 audit note: synthetic fixture generation remains deterministic local/test/dev only with no external calls and no real ingestion.

Synthetic fixtures must never be presented as live, tradable, production, or provider-sourced market history.

## Future Use

Future prompts may use these fixtures to test ingestion contracts, Data Quality validation, research lake roundtrips, warehouse loads, feature pipelines, backtests, and decision-support evidence paths. Real data remains blocked until read-only provider adapters, data-policy review, source references, and quality gates are implemented.

Development environment remains Mac mini M2 / macOS / Apple Silicon. Target desktop product remains Windows-native Stark Terminal.

## Prompt 16 Batch Metadata Linkage

Prompt 16 can persist synthetic fixture batch metadata through `MarketDataBatchMetadataService`. This persists metadata only: row count, time range, fixture id, validation report id, and source reference. It does not persist full OHLCV bars and does not turn synthetic fixtures into real market data.

## Prompt 18 Synthetic Storage Linkage

Prompt 18 can store generated synthetic fixture bars through `SyntheticOHLCVStorageService` after validation-before-storage. This storage path requires synthetic/local/test source references and `LOCAL_SAMPLE` provider identity where practical.

Stored fixture bars remain synthetic local-only test/dev data. They are not live data, not real market data, not provider-sourced data, not trading signals, not decision inputs, and not investment advice. Prompt 18 does not call external providers, publish events, export research datasets, compute analytics, or expose execution APIs.

## Prompt 21 Local Sample Provider Linkage

Prompt 21 uses synthetic fixtures through Local Sample Provider Adapter v0. The adapter returns synthetic/local instruments and deterministic synthetic historical bars as provider-shaped `MarketDataResponse` objects for local tests and API samples.

This does not turn fixtures into real market data. The adapter makes no external calls, performs no scraping, uses no credentials, writes no persistence stores, computes no analytics, generates no trading signals, and exposes no execution APIs.
