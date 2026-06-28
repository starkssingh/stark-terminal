# Research Artifact Index Provenance Placeholders

`ResearchArtifactIndexProvenancePlaceholder` is a descriptive planning-only provenance contract. It may record placeholder registry references, source references, and audit notes for future index planning.

## Safety Contract

- Provenance is descriptive only.
- `source_validated` must remain false.
- No external validation.
- No external fetch.
- No source URI fetch.
- No persistent writes.
- No real data trust claim.
- No paper parsing, PDF parsing, arXiv ingestion, LLM paper analysis, method extraction, strategy extraction, strategy generation, backtesting, recommendations, readiness-to-trade, broker controls, or execution APIs.
