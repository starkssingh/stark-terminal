# Research Artifact Index Planning

Prompt 77 creates Research Artifact Index planning and guardrails only. The Research Artifact Index is a future metadata/indexing layer for artifact references, keys, tags, registry references, provenance references, lifecycle references, and index-safe metadata.

This is not an index implementation. Prompt 77 adds placeholder contracts, safety helpers, readiness metadata, read-only planning endpoints, documentation, tests, audit coverage, and verifier coverage only.

## Scope

- Research Artifact Index planning and guardrails only.
- Index metadata, key, reference, tag, provenance, and lifecycle placeholders only.
- Registry references are descriptive placeholders only.
- Read-only planning metadata endpoints only.
- Ready for Prompt 78 - Research Artifact Index API Contract Skeleton only.

## Forbidden

- No indexing engine.
- No search engine.
- No ranking engine.
- No retrieval engine.
- No embedding pipeline.
- No vector store.
- No semantic search or keyword search.
- No active artifact ingestion/storage.
- No file upload/download/preview.
- No database tables, migrations, object storage, or persistent index writes.
- No paper parsing, PDF parsing, arXiv ingestion, or LLM paper analysis.
- No PDF parsing.
- No arXiv ingestion.
- No LLM paper analysis.
- No strategy generation.
- No strategy code generation.
- No method extraction or strategy extraction.
- No backtesting, optimization, parameter search, walk-forward analysis, or performance claims.
- No optimization.
- No recommendations, action generation, confidence scoring, DecisionObject generation, or readiness-to-trade.
- No broker controls, approvals, overrides, or execution APIs.

Development remains on Mac mini M2 / macOS / Apple Silicon. The target desktop product remains Windows-native Stark Terminal. Execution APIs remain forbidden.

## Prompt 78 API Contract Skeleton Linkage

Prompt 78 adds the Research Artifact Index API contract skeleton and keeps it
read-only and unavailable-by-default. The API skeleton exposes request,
response, reference, unavailable, safety, and health metadata only. It does
not add implementation, indexing, search, ranking, retrieval, embeddings,
vector store, active ingestion/storage, upload/download/preview, paper
parsing, strategy generation, backtesting, recommendations, or execution.

Prompt 79 may add Research Artifact Index Display Contract Skeleton only.

## Prompt 79 Display Contract Skeleton Linkage

Prompt 79 adds the Research Artifact Index Display contract skeleton and keeps
it backend-only, read-only, and unavailable-by-default. The display skeleton
exposes display metadata placeholders, index card placeholders, reference
display placeholders, tag display placeholders, provenance display
placeholders, lifecycle badge placeholders, unavailable display responses,
safety metadata, and health metadata only.

It does not add active UI, frontend implementation, desktop implementation,
indexing, search, ranking, retrieval, embeddings, vector store, active
ingestion/storage, upload/download/preview, paper parsing, strategy
generation, backtesting, recommendations, broker controls, readiness-to-trade,
or execution APIs. Prompt 80 may perform Research Artifact Index Safety
Boundary Audit only.

## Prompt 80 Safety Boundary Audit Confirmation

Prompt 80 audits the Research Artifact Index planning, API, and display
skeleton phase and confirms it remains placeholder-only. No implementation,
active UI/frontend/desktop, indexing/search/ranking/retrieval,
embeddings/vector store, active ingestion/storage, upload/download/preview,
paper parsing, strategy generation, backtesting, recommendations, broker
controls, readiness-to-trade, or execution APIs are introduced.
