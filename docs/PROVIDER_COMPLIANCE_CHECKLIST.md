# Provider Compliance Checklist

Prompt 20 defines compliance checklist contracts for future provider adapter readiness. This checklist is documentation and schema only; it does not approve any real provider.

## Checklist Fields

Future provider review must document:

- terms review
- redistribution rights
- storage rights
- delayed data requirements
- attribution requirements
- scraping prohibition
- credential handling review
- rate limits
- data quality plan
- audit logging plan
- sanitized notes

Prompt 23 adds candidate checklist fields before approval:

- terms review available
- storage rights known
- redistribution rights known
- rate limits known
- attribution requirements known
- delayed data requirements known
- credential handling plan ready
- data quality plan ready
- audit logging plan ready
- fallback plan ready
- no-execution scope confirmed
- no scraping or separately approved scraping

## Current Phase

In Prompt 20, credentials are disallowed, network calls are disabled by default, scraping is disabled by default, and no real provider implementation exists. Readiness reports should block implementation when guardrails block, approval is missing, terms review is incomplete, data quality planning is missing, or audit logging planning is missing.

## Safety Boundary

The compliance checklist cannot authorize execution APIs, order placement, broker integrations, credential vaults, trading recommendations, analytics signals, or real market ingestion. Future real ingestion requires a provider adapter prompt, data policy review, validation gates, source references, and auditability.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
