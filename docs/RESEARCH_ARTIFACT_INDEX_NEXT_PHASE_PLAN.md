# Research Artifact Index Next Phase Plan

Prompt 83 completes Research Artifact Index API/Display Integration Readiness
Audit after implementation and verification.

Prompt 82 completes Research Artifact Index system boundary hardening after
implementation and verification.

Prompt 81 completes the Research Artifact Index planning/API/display/safety milestone audit if verification passes.

## Current Status

The Research Artifact Index phase is complete through system boundary
hardening and API/display integration readiness audit only:

- Prompt 77 - Planning and Guardrails.
- Prompt 78 - API Contract Skeleton.
- Prompt 79 - Display Contract Skeleton.
- Prompt 80 - Safety Boundary Audit.
- Prompt 81 - Milestone Audit.
- Prompt 82 - System Boundary Hardening.
- Prompt 83 - API/Display Integration Readiness Audit.

Implementation remains forbidden.

## Forbidden Until Future Audited Phases

- no Research Artifact Index implementation
- no active UI, frontend implementation, or desktop implementation
- no indexing engine
- no search engine
- no ranking engine
- no retrieval engine
- no embeddings
- no vector store
- no active ingestion or persistent storage
- no persistent storage
- no file upload, download, or preview
- no paper parsing, PDF parsing, arXiv ingestion, or LLM paper analysis
- no strategy generation or strategy code generation
- no backtesting or optimization
- no recommendations, action generation, confidence scoring, active DecisionObjects, or readiness-to-trade
- no broker controls
- no approvals or overrides
- no execution APIs

## Recommended Next Sequence

1. Prompt 84 - Research Metadata Graph Planning and Guardrails.
2. Prompt 85 - Research Metadata Graph API Contract Skeleton.
3. Prompt 86 - Research Metadata Graph Display Contract Skeleton.
4. Prompt 87 - Research Metadata Graph Safety Boundary Audit.
5. Prompt 88 - Research Metadata Graph Milestone Audit.

Research Metadata Graph implementation, graph storage, graph traversal, indexing, search, ranking, retrieval, embeddings, vector store, ingestion, paper parsing, strategy generation, backtesting, recommendations, broker controls, and execution remain forbidden until future explicit audited phases.

See `docs/RESEARCH_METADATA_GRAPH_READINESS_PLAN.md` for the Prompt 84
planning-only readiness boundary.

## Consolidation Policy

Future prompts should use grouped phase-level docs/tests unless a stronger safety reason requires additional audit files. The preferred current references are `docs/phases/research_artifact_index.md`, `docs/audits/research_artifact_boundaries.md`, and `docs/audits/safety_boundaries.md`.
