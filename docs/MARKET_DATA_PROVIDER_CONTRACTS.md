# Market Data Provider Contracts

Market Data Provider contracts define the read-only adapter boundary for future market data sources. Prompt 08 creates interfaces and local synthetic behavior only.

## Read-Only Provider Rule

Provider adapters are read-only. They must not place orders, route money, manage broker credentials, trigger execution, or create autonomous trading behavior. Broker execution remains forbidden.

## Prompt 08 Scope

Prompt 08 implements:

- `MarketDataRequest`
- `MarketDataResponse`
- `ProviderCapabilityReport`
- `MarketDataProvider` base contract
- `LocalSampleMarketDataProvider`
- `ProviderRegistry`
- Provider contract health checks

Prompt 08 does not implement provider SDKs, NSE/BSE clients, scraping, external API calls, real data loading, production ingestion, analytics engines, or execution APIs. It is explicitly no scraping and no external calls.

## Network Calls

Network calls are disabled by default:

- `ALLOW_EXTERNAL_MARKET_DATA_CALLS=false`
- `ALLOW_PROVIDER_NETWORK_CALLS=false`

Prompt 08 settings fail closed if these flags are enabled. Future provider implementations require explicit prompt scope and data policy review.

## Capabilities

Provider capabilities are declared explicitly:

- Instrument master
- Historical bars
- Latest bar
- Options chain
- Futures chain
- Corporate actions
- Health check

The Prompt 08 local sample provider supports only instrument master and health check using synthetic fixtures. Prompt 21 adds `LocalSampleProviderAdapter` v0 with synthetic/local/test-only instrument master, historical bars, and health check support.

## Request / Response Schema

Market data requests must declare request kind, schema version, instrument, timeframe, start/end where required, provider identity, and adjustment mode. Historical bar requests require instrument, timeframe, start, and end.

Responses must include bars, instruments, or sanitized errors. Responses also carry provider metadata, quality status, source data reference where available, and received timestamp.

## Credentials And Terms

No credentials, tokens, API keys, raw URLs with secrets, broker tokens, or provider secrets may be committed or exposed. Provider terms must be respected before any future implementation.

## Prompt 20 Provider Guardrail Layer

Prompt 20 adds a provider guardrail layer before any real provider implementation. The new contracts include `ProviderGuardrailPolicy`, `ProviderApprovalRecord`, `ProviderComplianceChecklist`, and `ProviderReadinessReport`.

Provider implementation now requires:

- approval workflow record
- compliance checklist
- terms review
- data quality plan
- audit logging plan
- no-execution scope review
- explicit future prompt before real ingestion

Prompt 20 still implements no real provider client, no provider SDK, no scraping, no external calls, no credentials, no real market ingestion, no live-data claims, no analytics signals, and no execution APIs. The current allowed mode is synthetic-only local fixture planning.

Development environment remains Mac mini M2 / macOS / Apple Silicon. Target desktop product remains Windows-native Stark Terminal.

## Prompt 21 Local Sample Provider Adapter v0

Prompt 21 implements the first concrete provider adapter, but only for synthetic local samples. `LocalSampleProviderAdapter` is read-only, guardrail-protected, and uses:

- existing synthetic/local instrument fixtures for instrument master responses.
- existing synthetic OHLCV generation for deterministic historical bars.
- `LOCAL_SAMPLE` provider identity.
- `synthetic-local-test-only` source references.
- Data Quality Framework validation where practical.

Supported capabilities are instrument master, historical bars, and health check. Unsupported capabilities include real latest bar, real options chain, real futures chain, corporate actions, broker execution, order placement, credentials, network calls, scraping, and real market ingestion.

Prompt 21 still implements no real provider client, no provider SDK, no external calls, no scraping, no credentials, no real market data, no analytics signals, no decisions, and no execution APIs.

## Prompt 23 Real Provider Readiness Checklist And Candidate Selection

Prompt 23 adds `ProviderCandidateProfile`, `ProviderCandidateChecklist`, `ProviderSelectionCriteria`, `ProviderCapabilityGap`, `ProviderCandidateScore`, and `ProviderCandidateRegistry` contracts.

This layer evaluates future provider candidates before implementation. It performs Candidate Selection, risk scoring, and capability gap analysis only. It makes no external calls, installs no SDKs, performs no scraping, stores no credentials, ingests no real market data, grants no production approval, produces no trading signals, and exposes no execution APIs.

Candidate selection is pre-approval. A candidate score or shortlist does not approve a real provider, network test, production integration, broker execution, order placement, or real market ingestion.

## Prompt 24 Local File Provider Adapter v0

Prompt 24 implements `LocalFileProviderAdapter` v0 as a second safe adapter. It is local-file-only, read-only, path-safe, guardrail-protected, and test/dev only.

The adapter supports instrument master and historical bars from explicitly supplied CSV/Parquet `LocalFileSource` objects under an allowed root. It uses `MANUAL` provider identity, local-file/test/dev source references, provider guardrail evaluation, and Data Quality Framework validation before responses are returned.

The API surface exposes only `/local-file-provider/health` and `/local-file-provider/contracts`. It does not expose arbitrary file read API behavior and does not accept caller-supplied file paths over HTTP.

Prompt 24 still implements no live provider client, no external calls, no provider SDK, no scraping, no credentials, no real market data, no real market ingestion, no production approval, no analytics signals, no decisions, and no execution APIs.

## Prompt 25 Provider Adapter Milestone Audit

Prompt 25 audits Provider Adapter Guardrails, Real Provider Readiness and Candidate Selection, Local Sample Provider Adapter v0, and Local File Provider Adapter v0.

The audit confirms current provider code can perform only governance, synthetic/local sample responses, explicit local-file/test/dev responses under path safety, and read-only health/contracts/template/sample API metadata.

Current provider code still cannot make real API calls, scrape websites, load credentials, use provider SDKs, approve production providers, ingest real market data, expose arbitrary file read APIs, compute analytics/signals/decisions, or expose execution APIs.
