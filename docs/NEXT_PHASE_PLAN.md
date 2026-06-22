# Next Phase Plan

## Recommended Next Prompt

Prompt 26 - Quant/Time-Series Analytics Foundation Plan.

## Why This Follows

Prompts 00-10 establish typed contracts, safety boundaries, data platform foundations, cache/stream primitives, worker contracts, instrument/provider contracts, analytical warehouse contracts, and Feature Registry governance. Prompt 11 audits and consolidates that foundation. Prompt 12 adds the durable event backbone layer. Prompt 13 adds deterministic Data Quality + Validation Framework contracts. Prompt 14 adds synthetic local-only OHLCV fixtures.

Prompt 15 completed Instrument Metadata Persistence Wiring so canonical instruments can be stored through the PostgreSQL-ready ORM foundation with SQLite test fallback and validation gates. Prompt 16 completed Market Data Batch Persistence Contracts so validated synthetic/local `MarketDataBatch` metadata can be persisted without storing full production OHLCV history. Prompt 17 completes the Data Foundation Audit and Readiness Check across Prompts 14-16. Prompt 18 completes TimescaleDB Synthetic OHLCV Storage Foundation using validation-before-storage, `LOCAL_SAMPLE` provider identity, and SQLite-compatible tests. Prompt 19 completes the Synthetic OHLCV to Research Lake Export Contract with DatasetManifest linkage, validation-before-export, Parquet writes, DuckDB readback, and temp-only tests.

Prompt 20 completed provider adapter implementation planning and guardrails before any real provider work. Prompt 21 completed Local Sample Provider Adapter v0 using synthetic fixtures, guardrail checks, no API calls, no scraping, no credentials, no real ingestion, and no execution APIs.

Prompt 22 completes the milestone audit of Prompts 18-21 before expanding the provider/data path. Prompt 23 completes the real-provider readiness checklist and candidate-selection framework with no provider API calls, no SDK installation, no scraping, no credentials, no real ingestion, no production approval, and no execution behavior.

Prompt 24 completes Local File Provider Adapter v0 with explicit local test/dev files, path safety, provider guardrails, Data Quality validation, no arbitrary file read API, no network calls, no scraping, no credentials, no real ingestion, and no execution APIs.

Prompt 25 completes the Provider Adapter Milestone Audit across provider guardrails, real provider readiness, Local Sample Provider, and Local File Provider. It confirms no external calls, no scraping, no credentials, no SDKs, no real ingestion, no production approval, no arbitrary file read API, no analytics/signals/decisions, and no execution APIs.

The next institutional step is quant/time-series analytics foundation planning. Prompt 26 should define analytics module boundaries, numerical stack policy, and analytics safety rules without computing indicators, features, signals, decisions, recommendations, or backtests.

## Proposed Phase After Audit

The next phase should remain infrastructure-first and safety-bounded:

1. Prompt 26 - Quant/Time-Series Analytics Foundation Plan.
2. Prompt 27 - Numerical Analytics Core Contracts.
3. Prompt 28 - Returns and Rolling Window Analytics v0.
4. Prompt 29 - Volatility and Drawdown Analytics v0.
5. Prompt 30 - Analytics Milestone Audit.

## Still Forbidden

- no execution APIs.
- no broker execution.
- no order placement.
- no real-money routing.
- no broker credential handling.
- no real market ingestion.
- no provider-specific live clients.
- no NSE/BSE scraping.
- no real provider integration until separately approved.
- Real ingestion remains forbidden until provider readiness review, local-file provider testing, provider terms/compliance review, data-policy review, source reference policy, validation gates, provider-adapter audit, and a future explicit implementation prompt are complete.
- no provider SDKs.
- no provider credentials.
- no production Kafka/Redpanda pipelines.
- no production validation pipelines.
- no full OHLCV production persistence.
- no analytics engines, ML models, feature computation, backtesting engine, options pricing engine, or paper-to-strategy implementation.

## Platform Notes

Development and tests currently run on Mac mini M2 / macOS / Apple Silicon. The target desktop product remains Windows-native Stark Terminal. Backend target remains Oracle Cloud deployment.
