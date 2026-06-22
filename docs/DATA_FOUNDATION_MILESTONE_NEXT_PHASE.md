# Data Foundation Milestone Next Phase

Prompt 25 completes the Provider Adapter Milestone Audit after the Prompt 24 Local File Provider Adapter v0 foundation.

## Current Readiness State

The data foundation now has:

- deterministic synthetic OHLCV fixtures.
- instrument metadata persistence and market data batch metadata persistence.
- synthetic-only operational OHLCV storage.
- synthetic-only OHLCV research lake export with DatasetManifest linkage.
- provider adapter guardrails, approval workflow contracts, compliance checklist contracts, and readiness report contracts.
- Local Sample Provider Adapter v0 for synthetic/local/test-only instrument master and historical bar responses.
- Local File Provider Adapter v0 for explicitly supplied local CSV/Parquet test/dev files under path-safety guardrails.
- audit coverage for no real ingestion, no external calls, no scraping, no credentials, no execution APIs, and no analytics/signals/decisions.
- real provider readiness candidate profiles, readiness checklists, provider selection criteria, deterministic risk scoring, capability gap analysis, and in-memory candidate registry.
- Provider Adapter Milestone Audit documentation and invariant tests for Prompts 20-24.

## Recommended Next Prompt

Prompt 26 - Quant/Time-Series Analytics Foundation Plan.

Prompt 26 should define quant/time-series analytics planning docs, analytics module boundaries, numerical stack policy, analytics safety rules, and staged dependency rules without computing actual indicators, features, signals, decisions, recommendations, or backtests.

## Proposed Next 5 Prompts

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
- no provider credentials.
- no real market ingestion.
- no external provider calls.
- no provider-specific live clients.
- no provider SDKs.
- no scraping.
- no NSE/BSE loading.
- no production provider pipelines.
- no production research lake writes by default.
- no ClickHouse real-data writes.
- no Redis/Kafka event publishing from providers.
- no analytics/signals/decisions.
- no feature computation.
- no backtesting engine.
- no options pricing engine.
- no ML pipelines.

Real ingestion remains forbidden until provider readiness review, local-file provider testing, provider terms/compliance review, Data Quality gates, source reference policy, and an explicit future implementation prompt approve it.

This plan is reconciled with `PROVIDER_NEXT_PHASE_PLAN.md`.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
