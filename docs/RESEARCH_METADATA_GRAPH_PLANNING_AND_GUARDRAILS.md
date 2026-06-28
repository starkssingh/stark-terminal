# Research Metadata Graph Planning and Guardrails

Prompt 84 implements Research Metadata Graph Planning and Guardrails only.

This document is the main Prompt 84 phase document. It defines a future
metadata relationship layer for research artifacts, sources, datasets, papers,
hypotheses, experiments, strategy candidates, provenance references, lifecycle
states, dependency references, and review states. It does not implement an
active graph system.

## Purpose

The Research Metadata Graph is intended to become a future descriptive
metadata relationship layer. Prompt 84 only establishes placeholder contracts,
guardrails, readiness metadata, and GET-only planning endpoints so later phases
can add API and display contract skeletons safely.

## Planning-And-Guardrails-Only Posture

Prompt 84 is planning and guardrails only. It adds no graph database, no
persistent graph writes, no graph storage tables, no graph migrations, no graph
traversal engine, no graph query engine, no graph search, no graph ranking, no
graph retrieval, no embeddings, no vector store, no active ingestion/storage,
no upload/download/preview, no paper parsing, no strategy generation, no
backtesting, no recommendations, no broker controls, and no execution APIs.

## Future Role

Future audited phases may describe relationships between:

- research artifacts
- sources
- datasets
- papers
- hypotheses
- experiments
- strategy candidates
- provenance references
- lifecycle states
- dependency references
- review states

These are descriptive planning concepts only. They are not graph records,
database rows, queryable entities, searchable content, ranked relationships,
retrieved artifacts, trusted research claims, strategy outputs, or trading
signals.

## Node Placeholder Summary

Prompt 84 adds node placeholder contracts for:

- research artifacts
- sources
- datasets
- papers
- hypotheses
- experiments
- strategy candidates

Node placeholders are metadata placeholders only. They do not persist nodes,
query a graph database, parse paper content, load source files, extract
methods, generate strategies, run backtests, generate recommendations, or
enable execution.

## Edge Placeholder Summary

Prompt 84 adds edge placeholder contracts for:

- source-to-artifact references
- dataset-to-artifact references
- paper-to-hypothesis references
- hypothesis-to-experiment references
- experiment-to-strategy-candidate references
- artifact dependency references

Edge placeholders are descriptive references only. They do not persist edges,
perform traversal, rank relationships, retrieve artifacts, infer strategy
value, imply recommendations, or create execution readiness.

## Provenance Placeholder Summary

Graph provenance placeholders describe future source and audit references.
They do not validate source truth, fetch external content, read local files,
or imply trusted research status.

## Lifecycle Placeholder Summary

Allowed lifecycle states are PLANNED, REFERENCED, DRAFT, REVIEW_REQUIRED,
BLOCKED, DEFERRED, UNAVAILABLE, and UNKNOWN.

Forbidden lifecycle meanings remain forbidden: INDEXED, SEARCHABLE, RANKED,
EMBEDDED, RETRIEVED, VALIDATED_STRATEGY, BACKTESTED_PROFITABLE, RECOMMENDED,
READY_TO_TRADE, and EXECUTABLE.

## Reference And Dependency Placeholder Summary

Graph reference placeholders and dependency placeholders are descriptive only.
They perform no lookup, retrieval, graph traversal, graph search, graph
ranking, or file access.

## Readiness Summary

The Research Metadata Graph is ready for planning now. It is not ready for an
active graph database, persistent writes, traversal, search, ranking,
retrieval, embeddings, vector store, ingestion, upload/download/preview, paper
parsing, strategy generation, backtesting, recommendations, or execution.

Prompt 85 may add a Research Metadata Graph API Contract Skeleton only after
Prompt 84 passes verification. Graph implementation remains forbidden.

Prompt 85 adds that API Contract Skeleton as a read-only, unavailable-by-
default contract layer. The planning guardrails remain unchanged: no active
graph database, no persistent graph writes, no graph traversal/query/search/
ranking/retrieval, no embeddings/vector store, no ingestion/storage, no
paper parsing, no strategy generation, no backtesting, no recommendations,
and no execution.

Prompt 86 adds the Display Contract Skeleton as a backend-only, read-only,
unavailable-by-default display contract layer. The planning guardrails remain
unchanged: no active UI, no frontend/desktop implementation, no active graph
database, no persistent graph writes, no graph traversal/query/search/ranking/
retrieval, no embeddings/vector store, no ingestion/storage, no paper parsing,
no strategy generation, no backtesting, no recommendations, and no execution.

Prompt 87 confirms the Safety Boundary Audit for the planning/API/display
skeleton phase. The planning guardrails remain unchanged and no graph
implementation, graph database, active UI, traversal, search, retrieval,
storage, vector-store, parsing, strategy, backtesting, recommendation, broker,
or execution capability is unlocked.

Prompt 88 confirms the Milestone Audit for the planning/API/display/safety
phase. Planning guardrails remain unchanged and the phase is ready for
Research Metadata Graph System Boundary Hardening only. Graph implementation,
graph database, traversal, search, retrieval, storage, embeddings/vector
store, parsing, strategy generation, backtesting, recommendations, broker
controls, and execution remain forbidden.

## Read-Only Endpoint Posture

Prompt 84 adds these GET-only, read-only endpoints:

- `/research-metadata-graph/health`
- `/research-metadata-graph/planning`
- `/research-metadata-graph/readiness`
- `/research-metadata-graph/node-placeholder`
- `/research-metadata-graph/edge-placeholder`
- `/research-metadata-graph/provenance-placeholder`
- `/research-metadata-graph/lifecycle-placeholder`
- `/research-metadata-graph/reference-placeholder`

These endpoints return planning metadata and placeholders only. No POST
endpoints exist.

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

Prompt 84 follows the grouped documentation/testing policy. It creates one main
planning-and-guardrails document, one phase document, and grouped phase/API/
boundary tests. It does not recreate prompt-level micro-audit sprawl.

## Next Phase

Prompt 85 - Research Metadata Graph API Contract Skeleton.

Decision candidate is not a trade. No direct signal-to-trade path is allowed.
Execution APIs remain forbidden.
