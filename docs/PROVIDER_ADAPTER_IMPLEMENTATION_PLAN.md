# Provider Adapter Implementation Plan

Prompt 20 implements the Data Provider Adapter Implementation Plan and Guardrails. It does not implement any real provider adapter, provider SDK, scraping client, credential flow, real market ingestion, analytics engine, trading signal, decision generator, broker integration, or execution API.

## Purpose

Provider adapters are a future read-only data boundary for market data. Prompt 20 creates the governance layer that must exist before real provider work begins:

- provider approval workflow contracts
- provider guardrail policy contracts
- provider compliance checklist contracts
- provider readiness report contracts
- safe API health and contract endpoints
- deterministic tests that reject accidental real ingestion, scraping, credentials, or execution behavior

The current allowed mode is `SYNTHETIC_ONLY`. Provider test mode can use local synthetic fixtures only.

## Staged Future Process

1. Provider readiness checklist and candidate selection
2. Provider design contract
3. Sandbox or local file tests using synthetic/local fixtures
4. Controlled network tests only after explicit approval and a future implementation prompt
5. Real ingestion only after provider terms review, data policy review, source reference policy, Data Quality gates, audit logging, and an explicit future prompt

Production approval is not available in Prompt 20. No real provider is approved yet.

## Prompt 23 Candidate Selection Phase

Prompt 23 adds metadata-only candidate profiles, readiness checklists, selection criteria, risk scoring, and capability gap analysis. It does not approve any provider for production and does not implement network checks, provider SDKs, scraping, credentials, real ingestion, analytics signals, decisions, or execution APIs.

## Required Reviews Before Real Provider Work

Every future real provider implementation must have:

- approval record with requested and approved capabilities
- terms/compliance checklist
- no-execution scope review
- data quality plan
- audit logging plan
- rate-limit and attribution documentation if network calls are ever approved
- source data reference policy
- no credentials committed to the repository

## Current Prohibitions

- no scraping
- no external calls
- no real market ingestion
- no provider SDKs
- no provider credentials
- no broker execution adapters
- no order placement providers
- no credential vaults
- no live trading or real-money routing
- no analytics signals, features, backtests, regimes, decisions, or recommendations

## Prompt 25 Provider Milestone Audit

Prompt 25 audits the provider guardrails, provider readiness/candidate selection, Local Sample Provider Adapter v0, and Local File Provider Adapter v0. The audit confirms the implementation plan remains intact: real provider integration is still not started, no provider is approved for production, and no provider SDKs, scraping, credentials, external calls, real ingestion, analytics signals, decisions, or execution APIs exist.

After Prompt 25, the roadmap transitions to Prompt 26 - Quant/Time-Series Analytics Foundation Plan. That transition is planning-only and does not loosen provider guardrails.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
