# Research Metadata Graph Display Contract Skeleton

Prompt 86 implements the Research Metadata Graph Display Contract Skeleton
only.

This is a backend display-contract layer for the future Research Metadata
Graph display surface. It defines display contract metadata, node display
placeholders, edge display placeholders, provenance display placeholders,
lifecycle display placeholders, reference display placeholders, unavailable
display responses, display safety helpers, health metadata, and GET-only
display metadata endpoints. It does not implement active UI.

## Purpose

The display skeleton prepares a future graph display boundary without creating
rendered UI, frontend components, desktop components, graph behavior, graph
storage, graph traversal, graph search, graph retrieval, strategy outputs,
recommendations, or execution behavior.

## Display-Contract-Skeleton-Only Posture

Prompt 86 is display-contract-skeleton-only. It adds no active UI, no
frontend implementation, no desktop implementation, no active graph database,
no persistent graph writes, no graph storage tables, no graph migrations, no
graph traversal engine, no graph query engine, no graph search, no graph
ranking, no graph retrieval, no embeddings, no vector store, no active
ingestion/storage, no upload/download/preview, no paper parsing, no strategy
generation, no backtesting, no recommendations, no broker controls, and no
execution APIs.

## Display Contract Summary

`ResearchMetadataGraphDisplayContract` states:

- service: `stark-terminal-research-metadata-graph-display`
- stage: `display_contract_skeleton`
- read-only: true
- unavailable-by-default: true
- display-contract-skeleton-only: true
- active UI, frontend, desktop, graph, ingestion, parsing, strategy,
  backtest, recommendation, and execution flags are false

## Node Display Placeholder Summary

Node display placeholders cover future artifact, source, dataset, paper,
hypothesis, experiment, and strategy-candidate node surfaces. They are display
metadata only. They do not render active UI, query a graph database, retrieve
graph data, display search results, display rankings, display embeddings,
display parsed paper content, display generated strategies, display backtest
results, display recommendations, or display execution controls.

## Edge Display Placeholder Summary

Edge display placeholders cover future source-to-artifact, dataset-to-artifact,
paper-to-hypothesis, hypothesis-to-experiment, experiment-to-strategy-candidate,
and artifact dependency references. They are descriptive only. They do not
perform traversal, rank relationships, retrieve artifacts, infer strategy
value, or imply recommendations.

## Provenance Display Placeholder Summary

Provenance display placeholders are descriptive only. They do not validate
source truth, fetch external content, read local files, or imply trusted
research status.

## Lifecycle Display Placeholder Summary

Allowed lifecycle display meanings are PLANNED, REFERENCED, DRAFT,
REVIEW_REQUIRED, BLOCKED, DEFERRED, UNAVAILABLE, and UNKNOWN.

Forbidden lifecycle display meanings remain forbidden: INDEXED, SEARCHABLE,
RANKED, EMBEDDED, RETRIEVED, VALIDATED_STRATEGY, BACKTESTED_PROFITABLE,
RECOMMENDED, READY_TO_TRADE, and EXECUTABLE.

## Reference Display Placeholder Summary

Reference display placeholders are descriptive only. They perform no lookup,
retrieval, graph traversal, graph search, graph ranking, file access, or
external fetch.

## Unavailable Response Summary

Unavailable display responses always state `unavailable: true`, require a
reason, use `display_contract_skeleton` as the allowed stage, and keep all
dangerous enabled flags false.

## Read-Only Endpoint Posture

Prompt 86 adds these GET-only, read-only endpoints:

- `/research-metadata-graph-display/health`
- `/research-metadata-graph-display/contracts`
- `/research-metadata-graph-display/unavailable-template`
- `/research-metadata-graph-display/node-placeholder`
- `/research-metadata-graph-display/edge-placeholder`
- `/research-metadata-graph-display/provenance-placeholder`
- `/research-metadata-graph-display/lifecycle-placeholder`
- `/research-metadata-graph-display/reference-placeholder`

No POST endpoints exist for the Research Metadata Graph Display route family.

## Explicit Non-Implementation

- No active UI.
- No frontend or desktop implementation.
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

Prompt 86 follows the grouped documentation/testing policy. It creates one
main display contract skeleton document and grouped phase/API/boundary tests.
It does not recreate prompt-level micro-audit sprawl.

## Next Phase

Prompt 87 - Research Metadata Graph Safety Boundary Audit.

Prompt 87 confirms the Safety Boundary Audit for the planning/API/display
skeleton phase. The display contract remains backend-only, read-only,
unavailable-by-default, and display-contract-skeleton-only. No active UI,
frontend, desktop, graph implementation, graph database, traversal, search,
ranking, retrieval, embeddings/vector store, ingestion/storage,
upload/download/preview, paper parsing, strategy generation, backtesting,
recommendations, broker controls, readiness-to-trade, or execution APIs are
unlocked.

Prompt 88 confirms the Milestone Audit for the planning/API/display/safety
phase. The display contract remains backend-only, read-only,
unavailable-by-default, and display-contract-skeleton-only. The next phase is
Research Metadata Graph System Boundary Hardening only; active UI,
frontend/desktop implementation, graph implementation, graph database,
traversal, search, ranking, retrieval, embeddings/vector store,
ingestion/storage, upload/download/preview, paper parsing, strategy
generation, backtesting, recommendations, broker controls, and execution
remain forbidden.

Decision candidate is not a trade. No direct signal-to-trade path is allowed.
Execution APIs remain forbidden.
