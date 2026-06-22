# Provider Candidate Selection Policy

Prompt 23 adds Candidate Selection policy for future provider candidates. This is a governance contract only: no real provider client, no provider SDK, no scraping, no credentials, no external calls, no real market ingestion, no production approval, and no execution APIs.

## Candidate Process

Candidate selection uses:

- `ProviderCandidateProfile`
- `ProviderCandidateChecklist`
- `ProviderSelectionCriteria`
- deterministic risk scoring
- capability gap analysis
- in-memory `ProviderCandidateRegistry`

Provider candidates may be classified as draft, needs review, design candidate, local file candidate, network test candidate, production candidate blocked, rejected, or unknown. These statuses do not authorize implementation.

## Data Access Methods

Supported metadata classifications:

- synthetic-only
- local file
- official API
- vendor API
- broker read-only API
- scraping
- unknown

The current allowed mode remains synthetic/local only. A local file candidate may be considered next. Real API, vendor API, and broker read-only candidates remain blocked until future approval artifacts exist. Scraping candidates are blocked by default. Execution providers are forbidden.

## Selection Boundary

Candidate selection evaluates readiness, risk, and capability gaps. It must not call provider systems, verify live terms by network, fetch data, scrape web pages, load credentials, or claim real market data readiness.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
