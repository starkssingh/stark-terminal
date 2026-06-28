# Docs Consolidated Report

Status: aggressive grouped documentation/test report consolidation and verified deletion.

This report preserves the details of superseded granular prompt-level audit
documents selected for direct deletion after Archive Pass 1 and Archive Pass 2.
The deleted documents were already historical archive files, not active product
documentation. Grouped phase docs, grouped audit docs, and this report are now
the authoritative references for their content.

## Grouped Replacement Docs

- `docs/phases/research_artifact_index.md`
- `docs/phases/research_artifact_registry.md`
- `docs/phases/strategy_research_workspace.md`
- `docs/audits/safety_boundaries.md`
- `docs/audits/no_execution.md`
- `docs/audits/research_artifact_boundaries.md`
- `docs/testing/CONSOLIDATION_MAP.md`
- `docs/reports/DOCS_CONSOLIDATED_REPORT.md`
- `docs/reports/DELETED_FILES_REPORT.md`
- `docs/reports/SAFETY_COVERAGE_REPORT.md`

## Decision Desk

No Decision Desk docs are deleted in this pass. Decision Desk granular docs
remain active or historical because this pass does not revalidate the full
Decision Desk prompt family. Details remain in active Decision Desk docs,
`docs/phases/decision_desk.md` if present in a future pass, `docs/audits/no_execution.md`,
`docs/audits/safety_boundaries.md`, and `docs/PROMPT_LOG.md`.

## Retail Dashboard

No Retail Dashboard docs are deleted in this pass. Retail Dashboard granular
audit docs remain active pending a dedicated grouped replacement pass. Details
remain in active Retail Dashboard docs, `docs/phases/retail_dashboard.md` if
present in a future pass, `docs/audits/safety_boundaries.md`, and
`docs/PROMPT_LOG.md`.

## Retail Trader Experience

No Retail Trader Experience docs are deleted in this pass. Retail Trader
Experience granular audit docs remain active pending a dedicated grouped
replacement pass. Details remain in active Retail Trader Experience docs,
`docs/phases/retail_trader_experience.md` if present in a future pass,
`docs/audits/safety_boundaries.md`, and `docs/PROMPT_LOG.md`.

## Strategy Research Workspace

Deleted archived docs:

- `docs/archive/prompt_audits/strategy_research_workspace/STRATEGY_RESEARCH_WORKSPACE_NO_ACTIVE_UI_AUDIT.md`
- `docs/archive/prompt_audits/strategy_research_workspace/STRATEGY_RESEARCH_WORKSPACE_NO_PAPER_PARSING_AUDIT.md`
- `docs/archive/prompt_audits/strategy_research_workspace/STRATEGY_RESEARCH_WORKSPACE_NO_STRATEGY_GENERATION_AUDIT.md`
- `docs/archive/prompt_audits/strategy_research_workspace/STRATEGY_RESEARCH_WORKSPACE_NO_BACKTESTING_AUDIT.md`
- `docs/archive/prompt_audits/strategy_research_workspace/STRATEGY_RESEARCH_WORKSPACE_NO_RECOMMENDATION_AUDIT.md`
- `docs/archive/prompt_audits/strategy_research_workspace/STRATEGY_RESEARCH_WORKSPACE_NO_EXECUTION_AUDIT.md`

Coverage preserved:

- no active UI, frontend, or desktop implementation
- no paper ingestion or paper parsing
- no strategy generation or strategy code generation
- no backtesting or optimization
- no recommendations, action generation, confidence scoring, or DecisionObject generation
- no broker controls, readiness-to-trade, or execution APIs

Details are now preserved in `docs/phases/strategy_research_workspace.md`,
`docs/audits/safety_boundaries.md`, `docs/audits/no_execution.md`,
`docs/testing/CONSOLIDATION_MAP.md`, and this report.

## Research Artifact Registry

Deleted archived docs:

- `docs/archive/prompt_audits/research_artifact_registry/RESEARCH_ARTIFACT_REGISTRY_NO_ACTIVE_INGESTION_AUDIT.md`
- `docs/archive/prompt_audits/research_artifact_registry/RESEARCH_ARTIFACT_REGISTRY_NO_PERSISTENT_STORAGE_AUDIT.md`
- `docs/archive/prompt_audits/research_artifact_registry/RESEARCH_ARTIFACT_REGISTRY_NO_UPLOAD_DOWNLOAD_AUDIT.md`
- `docs/archive/prompt_audits/research_artifact_registry/RESEARCH_ARTIFACT_REGISTRY_NO_ACTIVE_UI_AUDIT.md`
- `docs/archive/prompt_audits/research_artifact_registry/RESEARCH_ARTIFACT_REGISTRY_NO_PAPER_PARSING_AUDIT.md`
- `docs/archive/prompt_audits/research_artifact_registry/RESEARCH_ARTIFACT_REGISTRY_NO_STRATEGY_GENERATION_AUDIT.md`
- `docs/archive/prompt_audits/research_artifact_registry/RESEARCH_ARTIFACT_REGISTRY_NO_BACKTESTING_AUDIT.md`
- `docs/archive/prompt_audits/research_artifact_registry/RESEARCH_ARTIFACT_REGISTRY_NO_RECOMMENDATION_AUDIT.md`
- `docs/archive/prompt_audits/research_artifact_registry/RESEARCH_ARTIFACT_REGISTRY_NO_EXECUTION_AUDIT.md`

Coverage preserved:

- no active artifact ingestion or persistent artifact storage
- no upload/download or file preview
- no active UI, frontend, or desktop implementation
- no paper parsing, PDF parsing, arXiv ingestion, or LLM paper analysis
- no strategy generation or strategy code generation
- no backtesting or optimization
- no recommendations, action generation, confidence scoring, or DecisionObject generation
- no broker controls, readiness-to-trade, approvals/overrides, or execution APIs

Details are now preserved in `docs/phases/research_artifact_registry.md`,
`docs/audits/research_artifact_boundaries.md`,
`docs/audits/safety_boundaries.md`, `docs/audits/no_execution.md`,
`docs/testing/CONSOLIDATION_MAP.md`, and this report.

## Research Artifact Index

Deleted archived docs:

- `docs/archive/prompt_audits/RESEARCH_ARTIFACT_INDEX_API_BOUNDARY_AUDIT.md`
- `docs/archive/prompt_audits/RESEARCH_ARTIFACT_INDEX_DISPLAY_BOUNDARY_AUDIT.md`
- `docs/archive/prompt_audits/RESEARCH_ARTIFACT_INDEX_NO_ACTIVE_UI_AUDIT.md`
- `docs/archive/prompt_audits/RESEARCH_ARTIFACT_INDEX_NO_INDEXING_SEARCH_RANKING_AUDIT.md`
- `docs/archive/prompt_audits/RESEARCH_ARTIFACT_INDEX_NO_RETRIEVAL_AUDIT.md`
- `docs/archive/prompt_audits/RESEARCH_ARTIFACT_INDEX_NO_EMBEDDINGS_VECTOR_STORE_AUDIT.md`
- `docs/archive/prompt_audits/RESEARCH_ARTIFACT_INDEX_NO_ACTIVE_INGESTION_STORAGE_AUDIT.md`
- `docs/archive/prompt_audits/RESEARCH_ARTIFACT_INDEX_NO_UPLOAD_DOWNLOAD_PREVIEW_AUDIT.md`
- `docs/archive/prompt_audits/RESEARCH_ARTIFACT_INDEX_NO_PAPER_PARSING_AUDIT.md`
- `docs/archive/prompt_audits/RESEARCH_ARTIFACT_INDEX_NO_STRATEGY_GENERATION_AUDIT.md`
- `docs/archive/prompt_audits/RESEARCH_ARTIFACT_INDEX_NO_BACKTESTING_AUDIT.md`
- `docs/archive/prompt_audits/RESEARCH_ARTIFACT_INDEX_NO_RECOMMENDATION_EXECUTION_AUDIT.md`

Coverage preserved:

- API and display contract boundary audits
- no active UI, frontend, or desktop implementation
- no indexing, search, ranking, or retrieval
- no embeddings or vector store
- no ingestion/storage/upload/download/preview
- no paper parsing, PDF parsing, arXiv ingestion, or LLM paper analysis
- no strategy generation or strategy code generation
- no backtesting or optimization
- no recommendations, action generation, confidence scoring, DecisionObject generation, readiness-to-trade, broker controls, or execution APIs

Details are now preserved in `docs/phases/research_artifact_index.md`,
`docs/audits/research_artifact_boundaries.md`,
`docs/audits/safety_boundaries.md`, `docs/audits/no_execution.md`,
`docs/testing/CONSOLIDATION_MAP.md`, and this report.

## Active Decision Architecture

No Active Decision Architecture docs are deleted. The target architecture docs
remain active and protected:

- `docs/ACTIVE_DECISION_ARCHITECTURE_TARGET.md`
- `docs/DECISION_CANDIDATE_PIPELINE_TARGET.md`
- `docs/VERIFIER_LAYER_TARGET_ARCHITECTURE.md`
- `docs/HUMAN_REVIEW_PAPER_TRADE_GATE_TARGET.md`
- `docs/AUDIT_LOG_JOURNAL_TARGET.md`
- `docs/phases/active_decision_architecture.md`

Decision candidate is not a trade. Execution APIs remain forbidden.

## What Remains Active

Active product docs, source docs, API surface inventory, safety audit, data
policy, infrastructure stack, grouped phase docs, grouped audit docs, active
decision architecture docs, and behavior-oriented docs remain active.

## What Was Not Deleted And Why

Active granular docs for Decision Desk, Retail Dashboard, Retail Trader
Experience, Strategy Research Workspace integration/boundary/milestone docs,
Research Artifact Registry integration/boundary/milestone docs, and all product
behavior docs remain active because this deletion pass only removes previously
archived superseded micro-audit files.
