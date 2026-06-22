# Provider Capability Gap Analysis

Prompt 23 adds provider capability gap analysis for future real provider candidates. It is metadata-only governance and does not implement provider APIs, external calls, scraping, SDKs, credentials, real market ingestion, analytics signals, decisions, or execution APIs.

## Capability Gaps

Gap analysis compares required read-only capabilities with a candidate profile:

- instrument master
- historical bars
- latest bar
- options chain
- futures chain
- corporate actions
- health check

A gap records whether a capability is required, present, missing, and why it matters. Capability gaps reduce readiness score and can block candidate shortlisting when a required capability is missing.

## Safety Rule

Capability gaps never justify unsafe integration. Missing data coverage does not permit scraping, credential shortcuts, unapproved SDKs, unreviewed network calls, real ingestion, broker execution, order placement, live trading, trading signals, or decision generation.

Execution and broker capabilities are not allowed candidate capabilities. Local Sample Provider and Local File Provider are the only implemented adapters after Prompt 24, both remain local/test/dev-only, and real provider implementation is not started.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
