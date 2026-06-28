# Research Metadata Graph API Contract Skeleton

Prompt 85 implements the Research Metadata Graph API Contract Skeleton only.

This is a read-only API contract layer for the future Research Metadata Graph.
It defines contract metadata, request placeholders, response placeholders,
reference placeholders, unavailable responses, API safety helpers, health
metadata, and GET-only metadata endpoints. It does not implement an active
graph system.

## Purpose

The API skeleton prepares a future graph API boundary without creating graph
behavior. It exists so later display and audit phases can reason about request,
response, unavailable, and reference contracts before any implementation is
considered.

## API-Contract-Skeleton-Only Posture

Prompt 85 is API-contract-skeleton-only. It adds no graph database, no
persistent graph writes, no graph storage tables, no graph migrations, no
graph traversal engine, no graph query engine, no graph search, no graph
ranking, no graph retrieval, no embeddings, no vector store, no active
ingestion/storage, no upload/download/preview, no paper parsing, no strategy
generation, no backtesting, no recommendations, no broker controls, and no
execution APIs.

## API Contract Summary

`ResearchMetadataGraphApiContract` states:

- service: `stark-terminal-research-metadata-graph-api`
- stage: `api_contract_skeleton`
- read-only: true
- unavailable-by-default: true
- API-contract-skeleton-only: true
- every dangerous graph, ingestion, parsing, strategy, backtest,
  recommendation, and execution flag is false

## Request Placeholder Summary

Request placeholders are metadata-only and read-only. They do not trigger
lookup, traversal, search, retrieval, ranking, graph query, graph database
access, file byte handling, raw paper content handling, market data
recommendation inputs, or strategy-generation instructions.

## Response Placeholder Summary

Response placeholders are unavailable-by-default. They contain no retrieved
graph data, no search results, no rankings, no embeddings, no parsed paper
content, no generated strategies, no backtest results, no recommendations, no
DecisionObject readiness, and no execution controls.

## Reference Placeholder Summary

Reference placeholders are descriptive only. They do not fetch, retrieve,
validate source truth, imply graph persistence, read files, traverse a graph,
search graph content, rank relationships, or expose trusted source claims.

## Unavailable Response Summary

Unavailable responses always state `unavailable: true`, require a reason, use
`api_contract_skeleton` as the allowed stage, and keep all dangerous enabled
flags false.

## Read-Only Endpoint Posture

Prompt 85 adds these GET-only, read-only endpoints:

- `/research-metadata-graph-api/health`
- `/research-metadata-graph-api/contracts`
- `/research-metadata-graph-api/unavailable-template`
- `/research-metadata-graph-api/request-placeholder`
- `/research-metadata-graph-api/response-placeholder`
- `/research-metadata-graph-api/reference-placeholder`

No POST endpoints exist for the Research Metadata Graph API route family.

## Explicit Non-Implementation

- No active graph database.
- No persistent graph writes.
- No graph traversal, graph query, graph search, graph ranking, or graph retrieval.
- No embeddings or vector store.
- No active ingestion/storage/upload/download/preview.
- No paper parsing, PDF parsing, arXiv ingestion, or LLM paper analysis.
- No strategy generation or strategy code generation.
- No backtesting or optimization.
- No recommendations, action generation, confidence scoring, DecisionObject
  generation, or readiness-to-trade.
- No broker controls, approvals, overrides, or execution APIs.

## Grouped Documentation And Testing Policy

Prompt 85 follows the grouped documentation/testing policy. It creates one
main API contract skeleton document and grouped phase/API/boundary tests. It
does not recreate prompt-level micro-audit sprawl.

## Next Phase

Prompt 86 - Research Metadata Graph Display Contract Skeleton.

Prompt 86 adds that Display Contract Skeleton as a backend-only,
read-only, unavailable-by-default display contract layer. The API contract
remains read-only and unavailable-by-default. It still performs no lookup,
traversal, search, retrieval, ranking, graph query, graph database access,
file handling, paper parsing, strategy generation, backtesting,
recommendation generation, broker control, or execution behavior.

Prompt 87 confirms the Safety Boundary Audit for the planning/API/display
skeleton phase. The API contract remains read-only, unavailable-by-default,
and API-contract-skeleton-only. No graph implementation, graph database,
traversal, search, ranking, retrieval, embeddings/vector store,
ingestion/storage, upload/download/preview, paper parsing, strategy
generation, backtesting, recommendations, broker controls, readiness-to-trade,
or execution APIs are unlocked.

Prompt 88 confirms the Milestone Audit for the planning/API/display/safety
phase. The API contract remains read-only, unavailable-by-default, and
API-contract-skeleton-only. The next phase is Research Metadata Graph System
Boundary Hardening only; graph implementation, graph database, traversal,
search, ranking, retrieval, embeddings/vector store, ingestion/storage,
upload/download/preview, paper parsing, strategy generation, backtesting,
recommendations, broker controls, and execution remain forbidden.

Decision candidate is not a trade. No direct signal-to-trade path is allowed.
Execution APIs remain forbidden.
