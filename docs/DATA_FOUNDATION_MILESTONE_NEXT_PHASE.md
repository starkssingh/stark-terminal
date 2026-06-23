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

Prompt 28 - Returns and Rolling Window Analytics v0.

Prompt 27 completed numerical analytics core contracts without computing returns, volatility, drawdown, correlation, indicators, features, signals, decisions, recommendations, or backtests.

## Proposed Next 5 Prompts

1. Prompt 28 - Returns and Rolling Window Analytics v0.
2. Prompt 29 - Volatility and Drawdown Analytics v0.
3. Prompt 30 - Analytics Milestone Audit.
4. Prompt 31 - Correlation and Beta Analytics v0.
5. Prompt 34 - Regime Feature Preparation Contracts.

## Prompt 26 Completion

Prompt 26 completes the Quant/Time-Series Analytics Foundation Plan after the provider adapter milestone audit. It adds analytics planning contracts, safety policy, dependency staging, roadmap metadata, and safe read-only analytics foundation endpoints. It does not compute analytics, indicators, features, signals, recommendations, decisions, or backtests.

## Prompt 27 Completion

Prompt 27 completes Numerical Analytics Core Contracts with source/vector/table contracts, computation request/result contracts, validation helpers, dependency gates, tiny descriptive stdlib summaries, docs, API metadata endpoints, and deterministic tests. It does not compute returns, volatility, drawdown, correlation, indicators, features, signals, recommendations, DecisionObjects, decisions, or backtests.

Prompt 28 should implement Returns and Rolling Window Analytics v0. Real ingestion, external calls, scraping, credentials, SDKs, provider integration, trading signals, recommendations, and execution APIs remain forbidden.

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
