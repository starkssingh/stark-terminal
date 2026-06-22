# Real Provider Readiness Checklist

Prompt 23 implements Real Provider Readiness Checklist contracts only. It does not implement a real provider, provider SDK, scraping client, credential flow, external call, real market ingestion, analytics signal, decision generator, broker integration, or execution API.

## Purpose

The readiness checklist is a pre-implementation governance layer for future real market data providers. A provider candidate must be described, scored, and reviewed before any adapter design can move beyond local synthetic or local-file planning.

Required metadata:

- provider candidate profile with candidate ID, provider name, display name, data access method, requested read-only capabilities, claimed exchanges, and claimed segments.
- provider readiness checklist with terms review, storage rights, redistribution rights, rate limits, attribution, delayed data requirements, data quality plan, audit logging plan, fallback plan, and no-execution scope confirmation.
- terms and compliance metadata placeholders.
- explicit no credentials, no SDKs, no external calls, no scraping, no real market ingestion, no production approval, and no execution APIs.

## Current Rules

- Local Sample Provider and Local File Provider are the only implemented adapters after Prompt 24; both are local/test/dev only.
- Candidate records are metadata only and do not approve real provider implementation.
- Network checks are disabled by default.
- Scraping checks are disabled by default.
- Credentials are disallowed.
- Production approval is unavailable in Prompt 23.
- Broker execution providers, order placement providers, credential vaults, and secret injection are rejected.

## Future Flow

Future real integration requires provider guardrails, candidate selection, approval workflow, compliance checklist, data-policy review, source references, Data Quality gates, audit logging, and a future explicit implementation prompt.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
