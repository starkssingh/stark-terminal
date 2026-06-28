# Research Artifact Index Tag Placeholders

`ResearchArtifactIndexTagPlaceholder` is a planning-only tag/category contract. It may describe topic, asset-class, market, method, dataset, paper-reference, experiment, status, or safety placeholder tags.

## Safety Contract

- UNKNOWN tag kind is rejected.
- `search_enabled` must remain false.
- `ranking_enabled` must remain false.
- `ranking_weight` must remain None in Prompt 77.
- Tags are not search filters, ranking factors, semantic vectors, embeddings, confidence scores, recommendation signals, action states, or execution controls.

No search engine, ranking engine, retrieval engine, embedding pipeline, vector store, active ingestion/storage, paper parsing, strategy generation, backtesting, recommendations, readiness-to-trade, broker controls, or execution APIs are introduced.
