# Provider Contracts Package

This package contains read-only market data provider contracts for Stark Terminal.

Prompt 08 does not implement real providers, provider SDKs, scraping, network calls, credentials, broker integrations, or execution APIs. Provider adapters are contract-first and read-only.

Future provider implementations must obey data policy, provider terms, credential handling rules, quality checks, and explicit prompt scope before any ingestion occurs.

Prompt 20 adds provider adapter guardrails, approval workflow contracts, compliance checklist contracts, and readiness reports. It still implements no real provider clients, no provider SDKs, no scraping, no credentials, no external calls, no real market ingestion, and no execution APIs.

Prompt 21 adds `LocalSampleProviderAdapter` v0. It is synthetic, local-only, test/dev only, read-only, and guardrail-protected. It supports instrument master, historical bars, and health checks using local fixtures only. It performs no external calls, no scraping, no credentials, no real market ingestion, no persistence writes, no event publishing, no analytics signals, no decisions, and no execution APIs.

Prompt 23 adds real provider readiness and candidate selection contracts through
`ProviderCandidateProfile`, `ProviderCandidateChecklist`, `ProviderSelectionCriteria`,
`ProviderCandidateRegistry`, and deterministic provider risk scoring helpers. These
contracts are metadata-only governance artifacts. They do not implement real provider
clients, provider SDKs, scraping, credentials, external calls, real market ingestion,
production approval, analytics signals, decisions, or execution APIs.

Prompt 24 adds `LocalFileProviderAdapter` v0. It is local-file-only, test/dev only,
read-only, path-safe, and guardrail-protected. It reads explicit CSV or Parquet source
objects under a configured allowed root for instrument master and historical bars.
It performs no external calls, no scraping, no credential loading, no provider SDK
calls, no arbitrary API file reads, no persistence writes, no event publishing, no
real market ingestion, no analytics signals, no decisions, and no execution APIs.
