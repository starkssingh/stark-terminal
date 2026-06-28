# Research Artifact Index API No Indexing Engine Policy

The Research Artifact Index API contract skeleton is not an indexing engine.
Prompt 78 adds placeholders, unavailable responses, safety helpers, and
read-only endpoints only.

The API must not build indexes, run indexing, maintain indexed artifact
records, persist index state, create database tables, create migrations, or
write object storage. Indexing implementation requires future prompts and
audits.

No search engine, ranking engine, retrieval engine, embeddings, vector store,
active ingestion/storage, file upload/download/preview, paper parsing,
strategy generation, backtesting, recommendations, broker controls, or
execution APIs are introduced.
