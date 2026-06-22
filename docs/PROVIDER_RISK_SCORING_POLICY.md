# Provider Risk Scoring Policy

Prompt 23 adds deterministic provider risk scoring for candidate selection. Scoring is conservative and cannot approve production use, real ingestion, network calls, scraping, credentials, SDKs, analytics signals, decisions, or execution APIs.

## Scoring Model

Candidate scoring starts at 100 and subtracts for:

- missing required capabilities
- missing terms review
- unknown storage rights
- unknown redistribution rights
- missing rate-limit metadata
- missing attribution or delayed-data requirements
- missing data quality plan
- missing audit logging plan
- missing fallback plan
- network requirement risk
- credential requirement risk
- scraping risk
- execution risk

Blockers force a `BLOCK` decision. Warnings reduce confidence but do not create approval. Missing terms review, unknown storage/redistribution rights, missing data quality plan, missing audit logging plan, default-disallowed network checks, default-disallowed credentials, scraping, and execution scope violations are blockers.

## Thresholds

Default readiness thresholds:

- design: 70
- network tests: 85
- production: 95

Network tests and production remain unavailable in Prompt 23. A high score does not approve real implementation, real market ingestion, production data use, provider SDK use, credentials, scraping, or external calls.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
