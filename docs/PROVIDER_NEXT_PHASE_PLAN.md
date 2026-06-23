# Provider Next Phase Plan

Prompt 25 completes the Provider Adapter Milestone Audit. Prompt 26 started analytics planning and Prompt 27 completed numerical analytics core contracts.

## Current Readiness State

The provider foundation now has:

- fail-closed Provider Adapter Guardrails.
- approval workflow contracts.
- compliance checklist contracts.
- real-provider readiness and candidate-selection governance.
- deterministic risk scoring and capability gap analysis.
- Local Sample Provider Adapter v0 for synthetic/local/test-only responses.
- Local File Provider Adapter v0 for explicit CSV/Parquet local test/dev files under path safety checks.
- read-only provider health/contracts/template/sample API surfaces.
- audit coverage for no external calls, no scraping, no credentials, no provider SDKs, no real ingestion, no production approval, no arbitrary file read API, no analytics/signals/decisions, and no execution APIs.

Prompt 26 added Quant/Time-Series Analytics Foundation planning contracts and Prompt 27 added Numerical Analytics Core Contracts. Neither loosened provider restrictions, implemented real ingestion, or generated signals/decisions.

## Recommended Next Prompt

Prompt 28 - Returns and Rolling Window Analytics v0.

The next phase has moved from provider adapter foundations to analytics implementation planning because the provider boundary is audited and still safely local/governance-only. Prompt 28 should implement returns and rolling window analytics using validated synthetic/local inputs only.

## Proposed Next 5 Prompts

1. Prompt 28 - Returns and Rolling Window Analytics v0.
2. Prompt 29 - Volatility and Drawdown Analytics v0.
3. Prompt 30 - Analytics Milestone Audit.
4. Prompt 31 - Correlation and Beta Analytics v0.
5. Prompt 34 - Regime Feature Preparation Contracts.

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
- no production provider approval.
- no arbitrary file read API.
- no production provider pipelines.
- no ClickHouse real-data writes.
- no Redis/Kafka event publishing from providers.
- no analytics/signals/decisions in provider code.
- no feature computation.
- no backtesting engine.
- no options pricing engine.
- no ML pipelines.

Real provider integration remains forbidden until a future explicit prompt completes provider terms/compliance review, data-policy review, source reference policy, Data Quality gates, audit logging, and production-readiness approval.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
