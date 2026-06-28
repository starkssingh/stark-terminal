# Research Artifact Index API Contract Skeleton

Prompt 78 implements the Research Artifact Index API contract skeleton only.
It is a backend contract layer for future Research Artifact Index API surfaces.
It is read-only, unavailable-by-default, and exposes placeholder metadata only.

## Scope

- API contract metadata for `stark-terminal-research-artifact-index-api`.
- Request placeholders and response placeholders.
- Index metadata, key, reference, tag, provenance, lifecycle, and registry reference placeholders.
- Unavailable API responses as the default behavior.
- Read-only API contract endpoints.
- Safety helpers that reject/block dangerous behavior only.

## Explicit Non-Implementation

- No indexing engine exists.
- No search engine exists.
- No ranking engine exists.
- No retrieval engine exists.
- No embeddings or vector store exist.
- No active artifact ingestion/storage exists.
- No database tables, migrations, object storage, or persistent index writes are introduced.
- No file upload/download/preview endpoints exist.
- No paper parsing, PDF parsing, arXiv ingestion, or LLM paper analysis exists.
- No strategy generation/code generation exists.
- No backtesting, optimization, parameter search, walk-forward analysis, or performance claims exist.
- No recommendations, confidence scoring, action generation, DecisionObject generation, or readiness-to-trade exists.
- No broker controls, approvals, overrides, or execution APIs exist.
- No execution exists.

Prompt 78 explicit audit phrases: No PDF parsing exists. No arXiv ingestion exists.
No LLM paper analysis exists. No strategy code generation exists. No optimization
exists. No confidence scoring exists. No DecisionObject generation exists.

Development remains on Mac mini M2 / macOS / Apple Silicon. The target desktop
product remains Windows-native Stark Terminal. The Active Decision Architecture
Target remains future documentation only: decision candidate is not a trade and
execution APIs remain forbidden.

## Next Phase

Prompt 79 may add Research Artifact Index Display Contract Skeleton only. Future
prompts and audits are required before any implementation, indexing, search,
storage, parsing, recommendations, or execution capability can be considered.

## Prompt 79 Display Contract Skeleton Linkage

Prompt 79 adds a backend-only Research Artifact Index Display contract skeleton
that consumes no API data and creates no API-to-display implementation path.
It exposes display placeholders only and remains read-only and
unavailable-by-default.

No active UI, frontend implementation, desktop implementation, file preview,
indexing engine, search engine, ranking engine, retrieval engine, embeddings,
vector store, active artifact ingestion/storage, upload/download/preview,
paper parsing, strategy generation, backtesting, recommendations, broker
controls, readiness-to-trade, or execution APIs are introduced.

## Prompt 80 API Safety Boundary Audit Confirmation

Prompt 80 confirms the Research Artifact Index API contract skeleton remains
GET-only, read-only, unavailable-by-default, and placeholder-only. No POST
endpoints, upload/download/preview endpoints, ingestion/storage endpoints,
indexing/search/ranking/retrieval endpoints, embedding/vector-store endpoints,
parsing endpoints, strategy endpoints, backtest endpoints, recommendation
endpoints, broker controls, readiness-to-trade, or execution endpoints are
introduced.
