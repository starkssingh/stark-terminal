# Provider Guardrail Policy

Prompt 20 provider guardrails define the safety boundary for future Data Provider Adapter work.

## Default Policy

The default `ProviderGuardrailPolicy` is fail-closed:

- read-only provider adapters only
- network calls disabled by default
- scraping disabled by default
- credentials disallowed in the current phase
- execution always forbidden
- real ingestion disallowed in the current phase
- approval required
- provider terms review required
- synthetic-only current mode

Guardrail decisions are `ALLOW`, `WARN`, or `BLOCK`. Prompt 20 uses these decisions for readiness contracts only. A guardrail result cannot enable execution APIs.

## Blocking Conditions

Provider work is blocked when any of the following appears:

- execution, order, broker, live trading, or real-money routing concepts
- missing approval when approval is required
- missing terms review when terms review is required
- requested network calls under the default no-network policy
- scraping under the default no-scraping policy
- requested credentials in the current phase
- real ingestion without future explicit approval artifacts

Synthetic-only local fixture design can be allowed only when the approval and compliance records fit the current phase and no external calls, credentials, scraping, real ingestion, or execution behavior are requested.

## Scope Boundary

Prompt 20 is a governance layer before ingestion. It implements no provider clients, no external calls, no scraping, no real market data ingestion, no analytics signals, and no execution APIs.

## Prompt 21 Allowed Adapter

Local Sample Provider Adapter v0 is the only currently allowed adapter because it is synthetic, local-only, test/dev only, and uses no external provider source. It still passes through provider guardrail evaluation before use.

This allowance does not approve real provider implementation. Network calls, scraping, credentials, real ingestion, live-data claims, broker behavior, order placement, analytics signals, decisions, and execution APIs remain blocked.

## Prompt 23 Candidate Readiness Gate

Prompt 23 adds a Real Provider Readiness and Candidate Selection gate before provider approval. Candidate records are metadata only. Candidate risk scoring, capability gap analysis, and shortlist decisions do not override guardrails and do not approve real provider implementation.

The current default still blocks network calls, scraping, credentials, real market ingestion, production approval, broker behavior, order placement, trading signals, decisions, and execution APIs.

## Prompt 24 Local File Adapter Allowance

Local File Provider Adapter v0 is allowed only as a local-file/test/dev adapter. It must use explicit `LocalFileSource` objects, configured allowed roots, CSV/Parquet extension allowlists, no network paths, no symlink escape, no credentials, no real-data claims, and no arbitrary file read API.

This allowance does not approve real provider implementation. Network calls, scraping, provider SDKs, credentials, real ingestion, live-data claims, broker behavior, order placement, trading signals, decisions, and execution APIs remain blocked.

## Prompt 25 Audit Confirmation

Prompt 25 audits the provider milestone and confirms guardrails remain fail-closed. Provider guardrails still block network calls by default, scraping by default, credentials by default, real ingestion, production approval, broker behavior, order placement, trading signals, decisions, and execution APIs.

Local Sample Provider and Local File Provider remain the only implemented adapters, and both are local/test/dev-only. No real provider implementation exists.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
