# Provider Approval Workflow

Prompt 20 defines provider approval workflow schemas before any real provider adapter is implemented.

## Approval Statuses

Provider approval records may be:

- `DRAFT`
- `BLOCKED`
- `APPROVED_FOR_DESIGN`
- `APPROVED_FOR_LOCAL_TESTS`
- `APPROVED_FOR_NETWORK_TESTS`
- `APPROVED_FOR_PRODUCTION`
- `REJECTED`
- `UNKNOWN`

Production approval is documented as a future state only. No real provider is approved in Prompt 20.

## Capabilities

Requested and approved capabilities must come from read-only market-data capabilities:

- instrument master
- historical bars
- latest bar
- options chain
- futures chain
- corporate actions
- health check

Broker execution, order placement, broker credential handling, live trading, and real-money routing are not allowed capabilities.

## Reviewer Requirements

Future provider work requires a reviewer, explicit status transition, and a documented reason. Design approval is not network approval. Network test approval is not production approval. Real ingestion still requires a future explicit prompt even after approval artifacts exist.

## Candidate Selection Is Pre-Approval

Prompt 23 provider candidate selection is pre-approval. A candidate profile, readiness checklist, risk score, shortlist, or capability gap analysis does not create an approval record and does not authorize network calls, provider SDKs, scraping, credentials, real ingestion, production use, broker behavior, order placement, trading signals, decisions, or execution APIs.

## Required Approval Inputs

- provider name
- requested mode
- requested capabilities
- requester
- reviewer when reviewed
- terms review status
- network, scraping, credential, and execution flags
- sanitized notes

Execution required must always be false. Scraping cannot be approved for production by default.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
