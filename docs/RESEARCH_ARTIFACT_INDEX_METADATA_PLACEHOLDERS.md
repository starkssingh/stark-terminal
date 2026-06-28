# Research Artifact Index Metadata Placeholders

`ResearchArtifactIndexMetadataPlaceholder` is a planning-only metadata contract. It may identify an index placeholder and its kind, title, description, schema version, and creation time.

## Safety Contract

- `index_id` cannot be empty.
- `title` cannot be empty.
- UNKNOWN index kind is rejected.
- `planning_only` must remain true.
- indexing_engine_enabled, search_engine_enabled, ranking_engine_enabled, embeddings_enabled, vector_store_enabled, and persistent_storage_enabled must remain false.

Metadata placeholders do not store artifacts, index artifacts, search artifacts, rank artifacts, retrieve artifacts, embed artifacts, parse papers, generate strategies, run backtests, generate recommendations, or execute trades.
