# Research Artifact Index API No Ingestion Storage Policy

The Research Artifact Index API contract skeleton must not ingest or store
artifacts. API placeholders may describe future metadata shapes only.

Forbidden:

- active artifact ingestion
- persistent artifact index writes
- persistent artifact registry writes
- database tables or migrations
- object storage
- repository writes
- background ingestion jobs
- file reference fetching
- source URI fetching
- local file reads

The API also remains free of indexing/search/ranking/retrieval, embeddings,
vector store, file upload/download/preview, paper parsing, strategy
generation, backtesting, recommendations, broker controls, readiness-to-trade,
and execution APIs.
