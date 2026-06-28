# Research Artifact Index API Unavailable Responses

Prompt 78 unavailable responses are the default for the Research Artifact Index
API contract skeleton. They are read-only, unavailable-by-default, and allowed
only in the `api_contract_skeleton` stage.

Unavailable responses explicitly report:

- indexing_engine_enabled false
- search_engine_enabled false
- ranking_engine_enabled false
- retrieval_engine_enabled false
- embeddings_enabled false
- vector_store_enabled false
- active_ingestion_enabled false
- persistent_storage_enabled false
- file_uploads_enabled false
- file_downloads_enabled false
- file_previews_enabled false
- paper_parsing_enabled false
- strategy_generation_enabled false
- backtesting_enabled false
- recommendations_enabled false
- execution_enabled false

They do not create an indexing engine, search engine, ranking engine,
retrieval engine, embedding pipeline, vector store, ingestion/storage, file
upload/download/preview, paper parsing, strategy generation, backtesting,
recommendations, broker controls, readiness-to-trade, or execution APIs.
