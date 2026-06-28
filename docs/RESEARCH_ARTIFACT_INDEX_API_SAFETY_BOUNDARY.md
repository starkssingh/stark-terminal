# Research Artifact Index API Safety Boundary

Prompt 78 safety helpers reject/block only. The Research Artifact Index API
remains an API contract skeleton, read-only, unavailable-by-default, and not an
implementation.

## Forbidden Behavior

- No indexing engine.
- No search engine.
- No ranking engine.
- No retrieval engine.
- No embedding pipeline.
- No vector store.
- No semantic search or keyword search.
- No active artifact ingestion/storage.
- No persistent storage, database tables, migrations, object storage, or index writes.
- No file upload/download/preview.
- No paper parsing, PDF parsing, arXiv ingestion, or LLM paper analysis.
- No method extraction or strategy extraction.
- No strategy generation or strategy code generation.
- No backtesting, optimization, parameter search, walk-forward analysis, or performance claims.
- No recommendation generation, action generation, confidence scoring, DecisionObject generation, or readiness-to-trade.
- No broker controls, approvals, overrides, or execution APIs.

Active Decision Architecture Target docs remain preserved. Decision candidate
is not a trade. No direct signal-to-trade path is allowed. Execution APIs
remain forbidden.
