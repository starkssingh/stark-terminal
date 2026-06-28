# North Star

## Product Goal

Stark Terminal is a Windows-native Indian-market trading research and decision terminal powered by an institutional-grade Oracle Cloud quant backend. It helps retail traders, quant traders, quant researchers, and market analysts evaluate markets with evidence, risk context, reproducible research workflows, and decision support.

## Product Philosophy

Evidence before decision. Safety before execution. Research before automation. Decision support before trading. Institution-grade infrastructure from day one.

## Institutional-Grade Architecture Principle

Stark Terminal must be built as a serious trading research and decision platform, not a minimal prototype. Robust infrastructure is intentional, not overkill. The target architecture must support market-data ingestion, time-series storage, feature computation, event replay, research reproducibility, backtesting, risk analytics, options analytics, paper-to-strategy research, and future scaling.

## Target Users

- Retail Trader: Wants simplified decision support such as Buy Bias, Sell Bias, Hold, Watch, Avoid, or Reduce with confidence, risk, invalidation, horizon, and plain-English evidence.
- Quant Trader: Wants regime diagnostics, time-series analysis, strategy testing, signal validation, and backtest evidence.
- Quant Researcher / Analyst: Wants research workflows, statistical modeling, feature engineering, reproducible experiment artifacts, and later paper-to-strategy conversion.

## Core Product Surfaces

- Decision Desk
- Quant Lab
- Options Desk
- Backtest Lab
- Risk Lab
- Data Lab
- Paper Lab
- Journal
- Settings
- System Health / Infrastructure Console

## Flagship Surface

The flagship surface is the Retail Decision Console / Decision Desk. It compresses deeper quant, time-series, regime, options, risk, and backtest machinery into action states:

- Strong Buy Bias
- Buy Bias
- Watch
- Hold
- Reduce / Caution
- Avoid
- Sell Bias
- Strong Sell Bias

## Central Contract: DecisionObject

The DecisionObject is the central object of Stark Terminal. Every visible recommendation, state label, or action state must eventually be backed by instrument, market/exchange, segment, timeframe, regime, state, action state, confidence, risk, evidence, invalidation, horizon, generated timestamp, source data reference, model or rule version, and audit ID.

## Active Decision Architecture Target

Future target: Data -> Quality/Provenance -> Timeseries -> Feature/Regime/State -> Deterministic Quant -> Decision Candidate -> Verifier -> Human/Paper Gate -> Audit Log/Journal.

Decision candidate is not a trade. The verifier layer is the hard safety gate,
human review / paper-trade gate must come before anything execution-like, and
execution APIs remain forbidden. This is target architecture documentation
only; the current system remains contract/skeleton/audit/boundary-first.

## Documentation/Test Policy

Stark Terminal is shifting from prompt-level audit sprawl to phase-level audit
consolidation. Prompt logs remain the chronological source of record, but
future development should prefer grouped phase docs, grouped safety audits, and
grouped tests by phase or boundary. This is a documentation/test consolidation
interlude only and does not add product capability.

Status phrase: phase-level audit consolidation.

Prompt 81 is complete. Archive Pass 1 moved obvious superseded Research
Artifact Index Prompt 80 micro-audit docs/tests into `docs/archive/` and
`tests/archive/` while preserving grouped phase/boundary safety coverage. The
next mainline prompt remains Prompt 82 - Research Artifact Index System
Boundary Hardening. Execution APIs remain forbidden.

Archive Pass 2 is complete before Prompt 82. It archives
older Strategy Research Workspace and Research Artifact Registry `NO_*`
micro-audit docs/tests into phase-specific archive folders while preserving
grouped phase/boundary safety coverage. It does not add product capability,
execution APIs, broker controls, active UI, ingestion/storage, indexing/search/
ranking/retrieval, embeddings/vector store, paper parsing, strategy generation,
backtesting, recommendations, readiness-to-trade, or execution behavior.

Archive status marker: Prompt 81 - Research Artifact Index Milestone Audit is
complete; Archive Pass 1 and Archive Pass 2 are complete before Prompt 82.

Aggressive grouped report cleanup is complete before Prompt 82. Deleted
micro-audit details are preserved under `docs/reports/`. This cleanup adds no
product capability and does not change execution safety: execution APIs remain
forbidden.

Current Prompt: 107
Completed Prompts: 108 after completion
Current Milestone: Retail Decision Console Internal Preview - Closed
Next Action: commit/push before starting next phase
Next Focus: Retail Decision Console Post-Preview UX Backlog and Next Product Phase Selection
Retail Decision Console Status: internal preview milestone closed; static/demo/unavailable/read-only only; no live data, recommendations, confidence scoring, active DecisionObjects, broker controls, order buttons, or execution
Audit Verdict: Retail Decision Console Internal Preview Milestone Closure complete; ready for commit/push before Prompt 108 only if tests pass.
Execution APIs: Forbidden
Documentation/Test Policy: phase-level docs/tests only
Prompt 107 implements Retail Decision Console Internal Preview Milestone Closure.
Verifier lock: Retail Decision Console Status: internal preview milestone closed; static/demo/unavailable/read-only only; not production ready; not trading ready; not recommendation ready; not execution ready; no live data, no generated recommendations, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs.
Historical verifier reference: Current Prompt: 106
Historical verifier reference: Completed Prompts: 107 after completion
Historical verifier reference: Current Milestone: Retail Decision Console Productization - Internal Preview Smoke Verification
Historical verifier reference: Next Focus: Retail Decision Console Internal Preview Milestone Closure
Historical verifier reference: Retail Decision Console Status: internal preview package smoke-verified; still static/demo/unavailable only; no live data, recommendations, confidence scoring, active DecisionObjects, broker controls, order buttons, or execution
Historical verifier reference: Audit Verdict: Retail Decision Console Internal Preview Package Smoke Verification complete; ready for Retail Decision Console Internal Preview Milestone Closure only if tests pass.
Prompt 106 implements Retail Decision Console Internal Preview Package Smoke Verification.
Verifier lock: Retail Decision Console Status: internal preview package smoke-verified; still static/demo/unavailable only; no live data, no generated recommendations, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs.
Historical verifier reference: Current Prompt: 105
Historical verifier reference: Completed Prompts: 106 after completion
Historical verifier reference: Current Milestone: Retail Decision Console Productization - Shareable Internal Preview Package
Historical verifier reference: Next Focus: Retail Decision Console Internal Preview Package Smoke Verification
Historical verifier reference: Retail Decision Console Status: static/demo shell with layout, local placeholder interactions, snapshot export, local QA bundle, manual acceptance checklist, and shareable internal preview package
Historical verifier reference: Audit Verdict: Retail Decision Console Shareable Internal Preview Package complete; ready for Retail Decision Console Internal Preview Package Smoke Verification only if tests pass.
Prompt 105 implements Retail Decision Console Shareable Internal Preview Package.
Verifier lock: Retail Decision Console Status: static/demo shell with layout, local placeholder interactions, snapshot export, local QA bundle, manual acceptance checklist, and shareable internal preview package; no live data, no generated recommendations, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs.
Historical verifier reference: Current Prompt: 104
Historical verifier reference: Completed Prompts: 105 after completion
Historical verifier reference: Current Milestone: Retail Decision Console Productization - Manual Acceptance Checklist
Historical verifier reference: Next Focus: Retail Decision Console Shareable Internal Preview Package
Historical verifier reference: Retail Decision Console Status: static/demo shell with layout, local placeholder interactions, snapshot export, local QA bundle, and manual acceptance checklist; no live data, recommendations, confidence scoring, active DecisionObjects, broker controls, order buttons, or execution
Historical verifier reference: Audit Verdict: Retail Decision Console Manual Acceptance Checklist complete; ready for Retail Decision Console Shareable Internal Preview Package only if tests pass.
Prompt 104 implements Retail Decision Console Manual Acceptance Checklist.
Verifier lock: Retail Decision Console Status: static/demo shell with layout, local placeholder interactions, snapshot export, local QA bundle, and manual acceptance checklist; no live data, no generated recommendations, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs.
Historical verifier reference: Current Prompt: 103
Historical verifier reference: Completed Prompts: 104 after completion
Historical verifier reference: Current Milestone: Retail Decision Console Productization - Local QA Bundle
Historical verifier reference: Next Focus: Retail Decision Console Manual Acceptance Checklist
Historical verifier reference: Retail Decision Console Status: static/demo shell with layout, local placeholder interactions, snapshot export, and local QA bundle; no live data, recommendations, confidence scoring, active DecisionObjects, broker controls, order buttons, or execution
Historical verifier reference: Audit Verdict: Retail Decision Console Local QA Bundle complete; ready for Retail Decision Console Manual Acceptance Checklist only if tests pass.
Prompt 103 implements Retail Decision Console Local QA Bundle.
Verifier lock: Retail Decision Console Status: static/demo shell with layout, local placeholder interactions, snapshot export, and local QA bundle; no live data, no generated recommendations, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs.
Historical verifier reference: Current Prompt: 102
Historical verifier reference: Completed Prompts: 103 after completion
Historical verifier reference: Current Milestone: Retail Decision Console Productization - Preview Snapshot Export
Historical verifier reference: Next Focus: Retail Decision Console Local QA Bundle
Historical verifier reference: Retail Decision Console Status: static/demo shell with layout, local placeholder interactions, and safe local snapshot export; no live data, recommendations, confidence scoring, active DecisionObjects, broker controls, order buttons, or execution
Historical verifier reference: Audit Verdict: Retail Decision Console Preview Snapshot Export complete; ready for Retail Decision Console Local QA Bundle only if tests pass.
Prompt 102 implements Retail Decision Console Preview Snapshot Export.
Verifier lock: Retail Decision Console Status: static/demo shell with layout, local placeholder interactions, and safe local snapshot export; no live data, no generated recommendations, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs.
Historical verifier reference: Current Prompt: 101
Historical verifier reference: Completed Prompts: 102 after completion
Historical verifier reference: Current Milestone: Retail Decision Console Productization - Static Interaction Placeholders
Historical verifier reference: Next Focus: Retail Decision Console Preview Snapshot Export
Historical verifier reference: Retail Decision Console Status: static/demo shell with polished layout and local-only placeholder interactions; no live data, recommendations, confidence scoring, active DecisionObjects, broker controls, order buttons, or execution
Historical verifier reference: Audit Verdict: Retail Decision Console Static Interaction Placeholders complete; ready for Retail Decision Console Preview Snapshot Export only if tests pass.
Prompt 101 implements Retail Decision Console Static Interaction Placeholders.
Verifier lock: Retail Decision Console Status: static/demo shell with polished layout and local-only placeholder interactions; no live data, no generated recommendations, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs.
Historical verifier reference: Current Prompt: 100
Historical verifier reference: Completed Prompts: 101 after completion
Historical verifier reference: Current Milestone: Retail Decision Console Productization - Visual Layout Pass
Historical verifier reference: Next Focus: Retail Decision Console Static Interaction Placeholders
Historical verifier reference: Retail Decision Console Status: static/demo shell with polished layout; no live data, recommendations, confidence scoring, active DecisionObjects, broker controls, order buttons, or execution
Historical verifier reference: Audit Verdict: Retail Decision Console Visual Polish and Section Layout Pass complete; ready for Retail Decision Console Static Interaction Placeholders only if tests pass.
Prompt 100 implements Retail Decision Console Visual Polish and Section Layout Pass.
Verifier lock: Retail Decision Console Status: static/demo shell with polished layout; no live data, no generated recommendations, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs.
Historical verifier reference: Current Prompt: 99
Historical verifier reference: Completed Prompts: 100 after completion
Historical verifier reference: Current Milestone: Retail Decision Console Productization - Local Preview and Smoke Test
Historical verifier reference: Next Focus: Retail Decision Console Visual Polish and Section Layout Pass
Historical verifier reference: Retail Decision Console Status: static/demo shell previewable locally; no live data, recommendations, confidence scoring, active DecisionObjects, broker controls, order buttons, or execution
Historical verifier reference: Audit Verdict: Retail Decision Console Local Preview Runbook and Manual Smoke Test complete; ready for Retail Decision Console Visual Polish and Section Layout Pass only if tests pass.
Prompt 99 implements Retail Decision Console Local Preview Runbook and Manual Smoke Test.
Verifier lock: Retail Decision Console Status: static/demo shell previewable locally; no live data, no generated recommendations, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs.
Historical verifier reference: Current Prompt: 98
Historical verifier reference: Completed Prompts: 99 after completion
Historical verifier reference: Current Milestone: Retail Decision Console Productization - Static State Wired into Desktop Shell
Historical verifier reference: Next Focus: Retail Decision Console Local Preview Runbook and Manual Smoke Test
Historical verifier reference: Retail Decision Console Status: UI shell skeleton with demo/static state wired; no live data, recommendations, confidence scoring, active DecisionObjects, broker controls, order buttons, or execution
Historical verifier reference: Audit Verdict: Retail Decision Console Static State Wiring into Desktop Shell complete; ready for Retail Decision Console Local Preview Runbook and Manual Smoke Test only if tests pass.
Prompt 98 implements Retail Decision Console Static State Wiring into Desktop Shell.
Verifier lock: Retail Decision Console Status: UI shell skeleton with demo/static state wired; no live data, no generated recommendations, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs.
Historical verifier reference: Current Prompt: 97
Historical verifier reference: Completed Prompts: 98 after completion
Historical verifier reference: Current Milestone: Retail Decision Console Productization - Demo Static State
Historical verifier reference: Next Focus: Retail Decision Console Static State Wiring into Desktop Shell
Historical verifier reference: Retail Decision Console Status: UI shell skeleton plus demo/static state only; no live data, recommendations, confidence scoring, active DecisionObjects, broker controls, order buttons, or execution
Historical verifier reference: Audit Verdict: Retail Decision Console Demo Data Contract and Static State Model complete; ready for Retail Decision Console Static State Wiring into Desktop Shell only if tests pass.
Prompt 97 implements Retail Decision Console Demo Data Contract and Static State Model.
Verifier lock: Retail Decision Console Status: UI shell skeleton plus demo/static state only; no live data, no generated recommendations, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs.
Historical verifier reference: Current Prompt: 96
Historical verifier reference: Completed Prompts: 97 after completion
Historical verifier reference: Current Milestone: Retail Decision Console Productization - UI Shell Skeleton
Historical verifier reference: Next Focus: Retail Decision Console Demo Data Contract and Static State Model
Historical verifier reference: Retail Decision Console Status: UI shell skeleton only; no live data, recommendations, confidence scoring, active DecisionObjects, broker controls, or execution
Historical verifier reference: Audit Verdict: Retail Decision Console UI Shell Skeleton complete; ready for Retail Decision Console Demo Data Contract and Static State Model only if tests pass.
Prompt 96 implements Retail Decision Console UI Shell Skeleton.
Verifier lock: Retail Decision Console Status: UI shell skeleton only; no live data, no generated recommendations, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs.
Historical verifier reference: Current Prompt: 95
Historical verifier reference: Completed Prompts: 96 after completion
Historical verifier reference: Current Milestone: Retail Decision Console Productization
Historical verifier reference: Next Focus: Retail Decision Console UI Shell Skeleton
Historical verifier reference: Retail Decision Console Status: productization plan and UI shell boundary only
Historical verifier reference: Audit Verdict: Retail Decision Console Productization Plan and UI Shell Boundary complete; ready for Retail Decision Console UI Shell Skeleton only if tests pass
Prompt 95 implements Retail Decision Console Productization Plan and UI Shell Boundary.
Verifier lock: Retail Decision Console Status: productization plan and UI shell boundary only; no live decisions, no active recommendations, no action generation, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs.
Historical verifier reference: Current Prompt: 94
Historical verifier reference: Completed Prompts: 95 after completion
Historical verifier reference: Current Milestone: Product Surface Reorientation
Historical verifier reference: Next Focus: Retail Decision Console / Decision Desk productization
Historical verifier reference: Audit Verdict: Product Surface Reorientation complete; ready for Retail Decision Console Productization Plan and UI Shell Boundary only if tests pass
Historical verifier reference: Prompt 94 performs Product Surface Reorientation and Development Plan
Historical verifier reference: Current Prompt: 93
Historical verifier reference: Completed Prompts: 94 after completion
Historical verifier reference: Current Milestone: Research Knowledge Map Planning Phase - Phase Closure
Historical verifier reference: Research Knowledge Map Status: phase closed; planning/API/display/safety only
Historical verifier reference: Audit Verdict: Research Knowledge Map Phase Closure complete; ready for Product Surface Reorientation and Development Plan only if tests pass
Historical verifier reference: Current Prompt: 92
Historical verifier reference: Completed Prompts: 93 after completion
Historical verifier reference: Current Milestone: Research Knowledge Map Planning Phase - Safety Boundary Audit
Historical verifier reference: Research Knowledge Map Status: planning/guardrails, API contract skeleton, display contract skeleton, and safety boundary audit complete
Historical verifier reference: Audit Verdict: Research Knowledge Map Safety Boundary Audit complete; ready for Research Knowledge Map Phase Closure only if tests pass
Historical verifier reference: Current Prompt: 91
Historical verifier reference: Completed Prompts: 92 after completion
Historical verifier reference: Current Milestone: Research Knowledge Map Planning Phase - Display Contract Skeleton
Historical verifier reference: Research Knowledge Map Status: planning/guardrails, API contract skeleton, and display contract skeleton only
Historical verifier reference: Audit Verdict: Research Knowledge Map Display Contract Skeleton complete; ready for Research Knowledge Map Safety Boundary Audit only if tests pass.
Historical verifier reference: Current Prompt: 90
Historical verifier reference: Completed Prompts: 91 after completion
Historical verifier reference: Current Milestone: Research Knowledge Map Planning Phase - API Contract Skeleton
Historical verifier reference: Research Knowledge Map Status: planning/guardrails and API contract skeleton only
Historical verifier reference: Audit Verdict: Research Knowledge Map API Contract Skeleton complete; ready for Research Knowledge Map Display Contract Skeleton only if tests pass.
Historical verifier reference: Current Milestone: Research Knowledge Map Planning Phase - Planning and Guardrails
Historical verifier reference: Current Prompt: 87
Historical verifier reference: Completed Prompts: 88 after completion
Historical verifier reference: Current Milestone: Research Metadata Graph Planning Phase - Safety Boundary Audit
Historical verifier reference: Research Metadata Graph Status: planning/guardrails, API contract skeleton, display contract skeleton, and safety boundary audit complete
Historical verifier reference: Audit Verdict: ready for Research Metadata Graph Milestone Audit only if tests pass
Historical verifier reference: Current Prompt: 86
Historical verifier reference: Completed Prompts: 87 after completion
Historical verifier reference: Current Milestone: Research Metadata Graph Planning Phase - Display Contract Skeleton
Historical verifier reference: Research Metadata Graph Status: planning/guardrails, API contract skeleton, and display contract skeleton only
Historical verifier reference: Audit Verdict: ready for Research Metadata Graph Safety Boundary Audit only if tests pass
Historical verifier reference: Current Prompt: 85
Historical verifier reference: Completed Prompts: 86 after completion
Historical verifier reference: Current Milestone: Research Metadata Graph Planning Phase - API Contract Skeleton
Historical verifier reference: Research Metadata Graph Status: planning/guardrails and API contract skeleton only
Historical verifier reference: Audit Verdict: ready for Research Metadata Graph Display Contract Skeleton only if tests pass
Historical verifier reference: Current Prompt: 84
Historical verifier reference: Completed Prompts: 85 after completion
Historical verifier reference: Current Milestone: Research Metadata Graph Planning Phase - Planning and Guardrails
Historical verifier reference: Prompt 84 implements Research Metadata Graph Planning and Guardrails
Historical verifier reference: Current Prompt: 83
Historical verifier reference: Completed Prompts: 84 after completion
Historical verifier reference: Current Milestone: Research Artifact Index Planning Phase - API/Display Integration Readiness Audit
Historical verifier reference: Audit Verdict: ready for Research Metadata Graph Planning and Guardrails only if tests pass.
Historical verifier reference: Research Metadata Graph Status: ready for planning and guardrails only.
Historical verifier reference: Current Prompt: 82
Historical verifier reference: Completed Prompts: 83 after completion
Historical verifier reference: Current Prompt: 81
Historical verifier reference: Completed Prompts: 82 after completion
Historical verifier reference: Current Milestone: Research Artifact Index Planning Phase - System Boundary Hardening
Historical verifier reference: Audit Verdict: ready for Research Artifact Index API/Display Integration Readiness Audit only if tests pass.
Current Milestone: Product Surface Reorientation
Research Artifact Index Status: planning/guardrails, API contract skeleton,
display contract skeleton, safety boundary audit, milestone audit, and system
boundary hardening, and API/display integration readiness audit complete; no
active implementation, no active UI, no frontend/desktop, no
indexing/search/ranking/retrieval, no embeddings/vector store, no
ingestion/storage, no upload/download/preview, no paper parsing, no strategy
generation, no backtesting, no recommendations, no execution.
Research Artifact Index system boundary hardening complete.
Research Artifact Index API/display integration readiness audit complete.
Research Metadata Graph Status: planning/guardrails, API contract skeleton,
display contract skeleton, and safety boundary audit complete; phase closed in
the canonical phase doc; no graph implementation, graph database, traversal,
search, retrieval, embeddings/vector store, storage, parsing, strategy,
backtesting, recommendations, or execution.
Research Knowledge Map Status: phase closed; planning/API/display/safety only;
no active implementation, active knowledge map, active UI, frontend/desktop
implementation, database, persistent writes, traversal, search, ranking,
retrieval, embeddings/vector store, paper parsing, strategy generation,
backtesting, recommendations, broker controls, or execution.
Verifier lock: Research Knowledge Map Status: planning/guardrails, API contract skeleton, display contract skeleton, and safety boundary audit complete.
Verifier lock: Research Metadata Graph Status: planning/guardrails, API contract skeleton, display contract skeleton, and safety boundary audit complete; phase closed.
Documentation/Test Policy: phase-based docs/tests only.
Active Decision Architecture Target: documented as future target only; decision candidate is not a trade; execution APIs remain forbidden.
Execution APIs: Forbidden
Development environment: Mac mini M2 / macOS / Apple Silicon
Target desktop product: Windows-native Stark Terminal
Next Focus: Retail Decision Console / Decision Desk productization
Audit Verdict: Product Surface Reorientation complete; ready for Retail Decision Console Productization Plan and UI Shell Boundary only if tests pass.

Prompt 94 performs Product Surface Reorientation and Development Plan. It
creates `docs/phases/product_surface_reorientation.md`, chooses Retail Decision
Console / Decision Desk productization as the next concrete product surface,
and reinforces phase-based docs/tests only. Prompt 94 adds no product runtime
capability, route, package, active UI, broker controls, active
recommendations, confidence scoring, active DecisionObject generation, live
market-data ingestion, or execution APIs.
Verifier lock: Prompt 94 performs Product Surface Reorientation and Development Plan.

Prompt 93 performs Research Knowledge Map Phase Closure. It closes the phase in
`docs/phases/research_knowledge_map.md`, reinforces phase-based docs/tests
only, and adds one grouped phase-closure test. It does not add active
knowledge map implementation, active UI, frontend components, desktop
components, database, persistent writes, traversal, query, search, ranking,
retrieval, embeddings/vector store, ingestion/storage, upload/download/
preview, paper parsing, strategy generation, backtesting, recommendations,
broker controls, approvals/overrides, readiness-to-trade, or execution APIs.
Verifier lock: Prompt 93 performs Research Knowledge Map Phase Closure.

Prompt 92 performs Research Knowledge Map Safety Boundary Audit. It audits the
planning/guardrails, API contract skeleton, display contract skeleton, and
GET-only route families. It does not add active knowledge map implementation,
active UI, frontend components, desktop components, database, persistent
writes, traversal, query, search, ranking, retrieval, embeddings/vector store,
ingestion/storage, upload/download/preview, paper parsing, strategy
generation, backtesting, recommendations, broker controls, approvals/
overrides, readiness-to-trade, or execution APIs.
Verifier lock: Prompt 92 performs Research Knowledge Map Safety Boundary Audit.

Prompt 91 implements Research Knowledge Map Display Contract Skeleton. It adds
backend display contract metadata, item display placeholders, relationship
display placeholders, evidence display placeholders, provenance display
placeholders, lifecycle display placeholders, unavailable display responses,
display safety helpers, health metadata, and GET-only display metadata
endpoints. It does not add active knowledge map implementation, active UI,
frontend components, desktop components, database, persistent writes,
traversal, query, search, ranking, retrieval, embeddings/vector store,
ingestion/storage, upload/download/preview, paper parsing, strategy
generation, backtesting, recommendations, broker controls,
approvals/overrides, readiness-to-trade, or execution APIs.
Verifier lock: Prompt 91 implements Research Knowledge Map Display Contract Skeleton.

Prompt 90 implements Research Knowledge Map API Contract Skeleton. It adds API
contract metadata, request placeholders, response placeholders, reference
placeholders, unavailable responses, API safety helpers, health metadata, and
GET-only API contract endpoints. It does not add active knowledge map
implementation, database, persistent writes, traversal, query, search,
ranking, retrieval, embeddings/vector store, active UI, ingestion/storage,
upload/download/preview, paper parsing, strategy generation, backtesting,
recommendations, broker controls, approvals/overrides, readiness-to-trade, or
execution APIs.
Verifier lock: Prompt 90 implements Research Knowledge Map API Contract Skeleton.

Prompt 89 implements Research Knowledge Map Planning and Guardrails. It adds
planning contracts, knowledge item placeholders, relationship placeholders,
evidence placeholders, provenance placeholders, lifecycle placeholders,
guardrails, readiness metadata, health metadata, and read-only planning
endpoints. It does not add active knowledge map implementation, database,
persistent writes, traversal, query, search, ranking, retrieval, embeddings/
vector store, active UI, ingestion/storage, upload/download/preview, paper
parsing, strategy generation, backtesting, recommendations, broker controls,
approvals/overrides, readiness-to-trade, or execution APIs.
Verifier lock: Prompt 89 implements Research Knowledge Map Planning and Guardrails.

Prompt 88-B performs Research Metadata Graph Phase Closure and Forward
Transition. It closes the phase in `docs/phases/research_metadata_graph.md`,
enforces phase-based docs/tests for future prompts, and adds one grouped
phase-closure test only. It does not add active UI, frontend components,
desktop components, graph implementation, graph database, persistent graph
writes, graph traversal, graph query, graph search, graph ranking, graph
retrieval, embeddings/vector store, ingestion/storage, upload/download/
preview, paper parsing, strategy generation, backtesting, recommendations,
broker controls, approvals/overrides, readiness-to-trade, or execution APIs.
The next phase is Research Knowledge Map Planning and Guardrails.
Verifier lock: Prompt 88-B performs Research Metadata Graph Phase Closure and Forward Transition.

Prompt 87 performs Research Metadata Graph Safety Boundary Audit. It audits the
planning/guardrails, API contract skeleton, display contract skeleton, and
GET-only route families. It does not add active UI, frontend components,
desktop components, graph implementation, graph database, persistent graph
writes, graph traversal, graph query, graph search, graph ranking, graph
retrieval, embeddings/vector store, ingestion/storage, upload/download/preview,
paper parsing, strategy generation, backtesting, recommendations, broker
controls, approvals/overrides, readiness-to-trade, or execution APIs.

Prompt 86 implements Research Metadata Graph Display Contract Skeleton. It
adds backend display contract metadata, node display placeholders, edge display
placeholders, provenance display placeholders, lifecycle display placeholders,
reference display placeholders, unavailable display responses, display safety
helpers, health metadata, and GET-only display metadata endpoints. It does not
add active UI, frontend components, desktop components, graph implementation,
graph database, persistent graph writes, graph traversal, graph query, graph
search, graph ranking, graph retrieval, embeddings/vector store,
ingestion/storage, upload/download/preview, paper parsing, strategy
generation, backtesting, recommendations, broker controls, approvals/
overrides, readiness-to-trade, or execution APIs.

Prompt 85 implements Research Metadata Graph API Contract Skeleton. It adds
API contract metadata, request placeholders, response placeholders, reference
placeholders, unavailable responses, API safety helpers, health metadata, and
GET-only API contract endpoints. It does not add graph implementation, graph
database, persistent graph writes, graph traversal, graph query, graph search,
graph ranking, graph retrieval, embeddings/vector store, ingestion/storage,
upload/download/preview, paper parsing, strategy generation, backtesting,
recommendations, broker controls, approvals/overrides, readiness-to-trade, or
execution APIs.

Prompt 84 implements Research Metadata Graph Planning and Guardrails. It adds
planning contracts, node placeholders, edge placeholders, provenance
placeholders, lifecycle placeholders, reference/dependency placeholders,
guardrails, readiness metadata, and read-only planning endpoints. It does not
add graph implementation, graph database, persistent graph writes, graph
traversal, graph query, graph search, graph ranking, graph retrieval,
embeddings/vector store, ingestion/storage, upload/download/preview, paper
parsing, strategy generation, backtesting, recommendations, broker controls,
approvals/overrides, readiness-to-trade, or execution APIs.

Prompt 83 performs Research Artifact Index API/Display Integration Readiness
Audit. It audits planning, API, display, safety, milestone, boundary
hardening, cross-endpoint consistency, and cross-module invariants. It does
not add active UI, frontend/desktop implementation, indexing/search/ranking/
retrieval, embeddings/vector store, ingestion/storage, upload/download/preview,
paper parsing, strategy generation, backtesting, recommendations, broker
controls, approvals/overrides, readiness-to-trade, or execution APIs.

Prompt 82 implements Research Artifact Index System Boundary Hardening. It adds
forbidden behavior registry contracts, endpoint boundary policies, module
boundary policies, cross-module invariant helpers, boundary health metadata,
and read-only boundary endpoints. It does not add active UI,
frontend/desktop implementation, indexing/search/ranking/retrieval,
embeddings/vector store, ingestion/storage, upload/download/preview, paper
parsing, strategy generation, backtesting, recommendations, broker controls,
approvals/overrides, readiness-to-trade, or execution APIs.

Prompt 40 implements the Decision Desk API Contract Skeleton. It adds request placeholders, response placeholders, evidence bundle reference placeholders, decision safety reference placeholders, unavailable response schemas, contract metadata, fail-closed settings, and read-only metadata endpoints. It does not accept market data, generate recommendations, action states, confidence scores, active DecisionObjects, approvals, overrides, trading decisions, signals, broker behavior, or execution APIs.

Prompt 41 performs the Decision Desk Milestone Audit. It audits Retail Decision Desk planning and guardrails, DecisionObject evidence bundle contracts, Decision Safety human-review guardrails, and the Decision Desk API contract skeleton. It adds audit docs, status consolidation, audit/verifier coverage, and tests. It does not add recommendations, action generation, confidence scoring, active DecisionObject generation, approvals, overrides, UI, broker behavior, real market ingestion, external calls, or execution APIs.

Prompt 42 implements the Decision Desk Readiness API Skeleton. It adds readiness request placeholders, readiness response placeholders, evidence/safety/human-review/blocked-output reference placeholders, unavailable readiness responses, contract metadata, fail-closed settings, and read-only metadata endpoints. It does not generate readiness-to-trade, recommendations, action states, confidence scores, active DecisionObjects, approvals, overrides, trading decisions, signals, broker behavior, or execution APIs.

Prompt 43 implements the Decision Desk Display Contract Skeleton. It adds display contract metadata, card placeholders, section placeholders, badge placeholders, evidence/safety display references, unavailable display responses, fail-closed settings, and read-only metadata endpoints. It does not build active UI, active recommendation cards, readiness-to-trade displays, recommendations, action states, confidence scores, active DecisionObjects, approvals, overrides, trading decisions, signals, broker behavior, or execution APIs.

Prompt 44 implements Decision Desk Evidence Bundle Validation v0. It adds validation-only request contracts, issue/failure reason schemas, validation result schemas, deterministic evidence/provenance/checklist/human-review validators, safety policy helpers, fail-closed settings, and read-only metadata endpoints. It does not generate recommendations, action states, confidence scores, active DecisionObjects, approvals, overrides, readiness-to-trade, trading decisions, signals, broker behavior, real ingestion, external calls, or execution APIs.

Prompt 45 implements the Decision Desk Human Review Workflow Skeleton. It adds workflow contracts, review task placeholders, reviewer role placeholders, review queue placeholders, status placeholders, unavailable workflow responses, no-approval safety contracts, fail-closed settings, and read-only metadata endpoints. It does not create active workflows, assign tasks, authenticate reviewers, send notifications, grant approvals, grant overrides, generate recommendations, action states, confidence scores, active DecisionObjects, readiness-to-trade, broker behavior, or execution APIs.

Prompt 46 performs Decision Desk Milestone Audit 2. It audits the Decision Desk Readiness API Skeleton, Decision Desk Display Contract Skeleton, Decision Evidence Bundle Validation v0, and Decision Human Review Workflow Skeleton. It adds audit docs, status consolidation, audit/verifier coverage, and tests only. It does not build active UI, active workflows, task assignment, reviewer auth, notifications, approvals, overrides, readiness-to-trade, recommendations, action states, confidence scoring, active DecisionObjects, broker behavior, real ingestion, external calls, or execution APIs.

Prompt 47 implements Decision Desk System Boundary Hardening. It adds forbidden behavior registry contracts, endpoint boundary policies, module boundary policies, cross-module invariant helpers, read-only boundary-hardening endpoints, stricter audit/verifier coverage, and tests. It does not build active UI, active workflows, task assignment, reviewer auth, notifications, approvals, overrides, readiness-to-trade, recommendations, action states, confidence scoring, active DecisionObjects, broker behavior, real ingestion, external calls, or execution APIs.

Prompt 48 performs the Decision Desk API/Display Integration Readiness Audit. It audits the Decision Desk API Contract Skeleton, Decision Desk Readiness API Skeleton, Decision Desk Display Contract Skeleton, Decision Evidence Bundle Validation v0, Decision Human Review Workflow Skeleton, Decision Desk System Boundary Hardening, cross-endpoint consistency, and API/display boundary readiness. It does not build Retail Dashboard UI, active UI, active workflows, task assignment, reviewer auth, notifications, approvals, overrides, readiness-to-trade, recommendations, action states, confidence scoring, active DecisionObjects, broker behavior, real ingestion, external calls, or execution APIs.

Prompt 49 implements Retail Dashboard Planning and Guardrails. It adds planning contracts, dashboard section placeholders, dashboard card placeholders, data-source reference placeholders, decision-reference placeholders, forbidden interaction contracts, safety policy helpers, readiness templates, fail-closed settings, and read-only planning endpoints. It does not build active Retail Dashboard UI, recommendation cards, action cards, confidence displays, active DecisionObject displays, readiness-to-trade displays, broker controls, approvals, overrides, real market data display, broker behavior, or execution APIs.

Prompt 50 implements the Retail Dashboard API Contract Skeleton. It adds request placeholders, response placeholders, data reference placeholders, decision reference placeholders, safety reference placeholders, unavailable response schemas, contract metadata helpers, fail-closed settings, and read-only API skeleton endpoints. It does not build active Retail Dashboard UI, frontend components, recommendation cards, action generation, confidence scoring, active DecisionObject generation or display, readiness-to-trade, broker controls, approvals, overrides, real market data display, broker behavior, or execution APIs.

Prompt 51 implements the Retail Dashboard Display Contract Skeleton. It adds display contract metadata, layout placeholders, widget placeholders, visual section placeholders, badge/status placeholders, unavailable display responses, display safety helpers, fail-closed settings, and read-only display skeleton endpoints. It does not build active Retail Dashboard UI, frontend components, desktop UI components, recommendation cards or widgets, action generation, confidence scoring, active DecisionObject generation or display, readiness-to-trade displays, broker controls, approvals, overrides, real market data display, broker behavior, or execution APIs.

Prompt 52 performs the Retail Dashboard Safety Boundary Audit. It audits Retail Dashboard Planning and Guardrails, Retail Dashboard API Contract Skeleton, and Retail Dashboard Display Contract Skeleton. It adds audit artifacts, status consolidation, verifier coverage, and safety-boundary invariant tests only. It does not build active Retail Dashboard UI, frontend components, desktop UI components, recommendation cards, action generation, confidence scoring, active DecisionObject generation or display, readiness-to-trade, broker controls, approvals, overrides, real market data display, broker behavior, or execution APIs.

Prompt 53 performs the Retail Dashboard Milestone Audit. It audits Retail Dashboard Planning and Guardrails, Retail Dashboard API Contract Skeleton, Retail Dashboard Display Contract Skeleton, and Retail Dashboard Safety Boundary Audit. It adds milestone audit artifacts, next-phase readiness documentation, verifier coverage, and milestone invariant tests only. It does not build active Retail Dashboard UI, frontend components, desktop UI components, recommendation cards, action generation, confidence scoring, active DecisionObject generation or display, readiness-to-trade, broker controls, approvals, overrides, real market data display, broker behavior, or execution APIs.

Prompt 54 implements Retail Dashboard System Boundary Hardening. It adds a Retail Dashboard forbidden behavior registry, endpoint boundary policies, module boundary policies, cross-module invariant helpers, boundary health checks, read-only boundary-hardening endpoints, stricter audit/verifier coverage, and tests. It does not build active Retail Dashboard UI, frontend components, desktop components, recommendation cards, action generation, confidence scoring, active DecisionObject generation or display, readiness-to-trade, broker controls, approvals, overrides, real market data display, broker behavior, or execution APIs.

Prompt 55 performs the Retail Dashboard API/Display Integration Readiness Audit. It audits Retail Dashboard planning/guardrails, API contract skeleton, display contract skeleton, safety boundary audit, milestone audit, system boundary hardening, cross-endpoint consistency, and cross-module no-active-UI/no-recommendation/no-execution invariants. It does not build active Retail Dashboard UI, frontend components, desktop components, recommendation cards, action generation, confidence scoring, active DecisionObject generation or display, readiness-to-trade, broker controls, approvals, overrides, real market data display, broker behavior, or execution APIs.

Prompt 56 implements Retail Trader Experience Planning and Guardrails. It adds planning contracts, persona placeholders, journey placeholders, experience section placeholders, experience card placeholders, dashboard/decision/safety reference placeholders, forbidden interaction contracts, safety helpers, readiness templates, health metadata, and read-only planning endpoints. It does not build active Retail Trader Experience UI, active Retail Dashboard UI, frontend components, desktop components, recommendation cards, action generation, confidence scoring, active DecisionObject generation or display, readiness-to-trade, broker controls, approvals, overrides, suitability profiling, real market data display, broker behavior, or execution APIs.

Prompt 57 implements the Retail Trader Experience API Contract Skeleton. It adds request placeholders, response placeholders, persona reference placeholders, journey reference placeholders, dashboard reference placeholders, decision reference placeholders, safety reference placeholders, unavailable response schemas, contract metadata, fail-closed settings, and read-only API skeleton endpoints. It does not build active Retail Trader Experience UI, active Retail Dashboard UI, frontend components, desktop components, recommendation cards, action generation, confidence scoring, active DecisionObject generation or display, readiness-to-trade, broker controls, approvals, overrides, suitability profiling, real market data display, broker behavior, or execution APIs.

Prompt 58 implements the Retail Trader Experience Display Contract Skeleton. It adds display contract metadata, persona visual placeholders, journey visual placeholders, visual section placeholders, widget placeholders, badge/status placeholders, unavailable display responses, display safety helpers, fail-closed settings, and read-only display skeleton endpoints. It does not build active Retail Trader Experience UI, active Retail Dashboard UI, frontend components, desktop components, recommendation cards or widgets, action generation, confidence scoring, active DecisionObject generation or display, readiness-to-trade, broker controls, approvals, overrides, suitability profiling, real market data display, broker behavior, or execution APIs.

Prompt 59 performs the Retail Trader Experience Safety Boundary Audit. It audits Retail Trader Experience Planning and Guardrails, Retail Trader Experience API Contract Skeleton, Retail Trader Experience Display Contract Skeleton, no-active-UI invariants, no-recommendation invariants, no-suitability-profiling invariants, no-broker-control invariants, and no-execution invariants. It does not build active Retail Trader Experience UI, active Retail Dashboard UI, frontend components, desktop components, recommendation cards or widgets, action generation, confidence scoring, active DecisionObject generation or display, readiness-to-trade, broker controls, approvals, overrides, suitability profiling, real market data display, broker behavior, or execution APIs.

Prompt 60 performs the Retail Trader Experience Milestone Audit. It audits Retail Trader Experience Planning and Guardrails, Retail Trader Experience API Contract Skeleton, Retail Trader Experience Display Contract Skeleton, Retail Trader Experience Safety Boundary Audit, no-active-UI invariants, no-recommendation invariants, no-suitability-profiling invariants, no-broker-control invariants, no-approval/override invariants, and no-execution invariants. It does not build active Retail Trader Experience UI, active Retail Dashboard UI, frontend components, desktop components, recommendation cards or widgets, action generation, confidence scoring, active DecisionObject generation or display, readiness-to-trade, broker controls, approvals, overrides, suitability profiling, real market data display, broker behavior, or execution APIs.

Prompt 61 implements Retail Trader Experience System Boundary Hardening. It adds a Retail Trader Experience forbidden behavior registry, endpoint boundary policies, module boundary policies, cross-module invariant helpers, read-only boundary-hardening endpoints, stricter audit/verifier coverage, and tests. It does not build active Retail Trader Experience UI, active Retail Dashboard UI, frontend components, desktop components, recommendation cards or widgets, action generation, confidence scoring, active DecisionObject generation or display, readiness-to-trade, suitability profiling, broker controls, approvals, overrides, real market data display, broker behavior, or execution APIs.

Prompt 62 performs Retail Trader Experience API/Display Integration Readiness Audit. It audits Retail Trader Experience Planning and Guardrails, Retail Trader Experience API Contract Skeleton, Retail Trader Experience Display Contract Skeleton, Retail Trader Experience Safety Boundary Audit, Retail Trader Experience Milestone Audit, Retail Trader Experience System Boundary Hardening, cross-endpoint consistency, cross-module consistency, API/display boundary integrity, and Strategy Research Workspace Planning and Guardrails readiness. It does not build active Retail Trader Experience UI, active Retail Dashboard UI, frontend components, desktop components, recommendation cards or widgets, action generation, confidence scoring, active DecisionObject generation or display, readiness-to-trade, suitability profiling, broker controls, approvals, overrides, real market data display, broker behavior, Strategy Research Workspace implementation, or execution APIs.

Prompt 63 implements Strategy Research Workspace Planning and Guardrails. It adds planning contracts, research workspace placeholders, research artifact placeholders, paper reference placeholders, strategy hypothesis placeholders, dataset reference placeholders, experiment plan placeholders, forbidden interaction contracts, safety helpers, readiness templates, health metadata, and read-only planning endpoints. It does not build active Strategy Research Workspace UI, active Retail Trader Experience UI, frontend components, desktop components, paper ingestion, paper parsing, strategy generation, strategy code generation, backtesting, optimization, recommendations, action generation, confidence scoring, active DecisionObject generation or display, readiness-to-trade, broker controls, approvals, overrides, real market data display, broker behavior, or execution APIs.

Prompt 64 implements the Strategy Research Workspace API Contract Skeleton. It adds request placeholders, response placeholders, workspace/artifact/paper/hypothesis/dataset/experiment/safety reference placeholders, unavailable responses, contract metadata, health metadata, and read-only API skeleton endpoints. It does not build active UI, frontend components, desktop components, paper ingestion, paper parsing, strategy generation, strategy code generation, backtesting, optimization, recommendations, action generation, confidence scoring, active DecisionObject generation or display, readiness-to-trade, broker controls, approvals, overrides, real market data display, broker behavior, or execution APIs.

Prompt 65 implements the Strategy Research Workspace Display Contract Skeleton. It adds display contract metadata, workspace visual placeholders, artifact visual placeholders, paper visual placeholders, hypothesis visual placeholders, dataset visual placeholders, experiment visual placeholders, badge placeholders, unavailable display responses, display safety helpers, health metadata, and read-only display skeleton endpoints. It does not build active UI, frontend components, desktop components, paper ingestion, paper parsing, strategy generation, strategy code generation, backtesting, optimization, recommendations, action generation, confidence scoring, active DecisionObject generation or display, readiness-to-trade, broker controls, approvals, overrides, real market data display, broker behavior, or execution APIs.

Prompt 66 performs the Strategy Research Workspace Safety Boundary Audit. It audits Strategy Research Workspace Planning and Guardrails, API Contract Skeleton, Display Contract Skeleton, no-active-UI, no-paper-ingestion/parsing, no-strategy-generation, no-backtesting, no-recommendation, no-broker-control, and no-execution invariants. It adds audit docs, tests, verifier coverage, audit coverage, and status consolidation only. It does not implement active UI, frontend components, desktop components, paper ingestion, paper parsing, strategy generation, strategy code generation, backtesting, optimization, recommendations, action generation, confidence scoring, active DecisionObject generation or display, readiness-to-trade, broker controls, approvals, overrides, real market data display, broker behavior, or execution APIs.

Prompt 67 performs the Strategy Research Workspace Milestone Audit. It audits Strategy Research Workspace Planning and Guardrails, API Contract Skeleton, Display Contract Skeleton, Safety Boundary Audit, phase no-active-UI, no-paper-ingestion/parsing, no-strategy-generation, no-backtesting, no-recommendation, no-broker-control, and no-execution invariants. It adds milestone audit docs, tests, verifier coverage, audit coverage, next-phase readiness documentation, and status consolidation only. It does not implement active UI, frontend components, desktop components, paper ingestion, paper parsing, strategy generation, strategy code generation, backtesting, optimization, recommendations, action generation, confidence scoring, active DecisionObject generation or display, readiness-to-trade, broker controls, approvals, overrides, real market data display, broker behavior, or execution APIs.

Prompt 68 implements Strategy Research Workspace System Boundary Hardening. It adds a forbidden behavior registry, endpoint boundary policies, module boundary policies, cross-module invariant helpers, rejection helpers, boundary health metadata, read-only boundary-hardening endpoints, stricter audit/verifier coverage, tests, and status consolidation only. It does not implement active UI, frontend components, desktop components, paper ingestion, paper parsing, arXiv ingestion, LLM paper analysis, strategy generation, strategy code generation, signal/factor/alpha generation, backtesting, optimization, recommendations, action generation, confidence scoring, active DecisionObject generation or display, readiness-to-trade, broker controls, approvals, overrides, real market data display, broker behavior, or execution APIs.

Prompt 69 performs the Strategy Research Workspace API/Display Integration Readiness Audit. It audits Strategy Research Workspace planning and guardrails, API contract skeleton, display contract skeleton, safety boundary audit, milestone audit, system boundary hardening, cross-endpoint consistency, API/display boundary integration, and Research Artifact Registry planning readiness. It does not implement active UI, frontend components, desktop components, Research Artifact Registry implementation, active ingestion/storage, paper ingestion, paper parsing, arXiv ingestion, LLM paper analysis, strategy generation, strategy code generation, signal/factor/alpha generation, backtesting, optimization, recommendations, action generation, confidence scoring, active DecisionObject generation or display, readiness-to-trade, broker controls, approvals, overrides, real market data display, broker behavior, or execution APIs.

Prompt 70 implements Research Artifact Registry Planning and Guardrails. It adds planning contracts, artifact metadata placeholders, artifact reference placeholders, artifact provenance placeholders, lifecycle placeholders, forbidden interaction contracts, safety/readiness helpers, health metadata, and read-only planning endpoints. It does not implement Research Artifact Registry implementation, active artifact ingestion/storage, persistent storage, file upload/download, paper ingestion, paper parsing, PDF parsing, arXiv ingestion, LLM paper analysis, strategy generation, strategy code generation, signal/factor/alpha generation, backtesting, optimization, recommendations, action generation, confidence scoring, active DecisionObject generation or display, readiness-to-trade, broker controls, approvals, overrides, real market data display, broker behavior, or execution APIs.

Prompt 71 implements Research Artifact Registry API Contract Skeleton. It adds
read-only API contract metadata, request placeholders, response placeholders,
metadata reference placeholders, provenance reference placeholders, lifecycle
reference placeholders, unavailable responses, API safety helpers, health
metadata, and read-only API contract endpoints. It does not implement Research
Artifact Registry implementation, active artifact ingestion/storage,
persistent storage, file upload/download, paper ingestion, paper parsing, PDF
parsing, arXiv ingestion, LLM paper analysis, strategy generation, strategy
code generation, signal/factor/alpha generation, backtesting, optimization,
recommendations, action generation, confidence scoring, active DecisionObject
generation or display, readiness-to-trade, broker controls, approvals,
overrides, real market data display, broker behavior, or execution APIs.

Prompt 72 implements Research Artifact Registry Display Contract Skeleton. It
adds backend-only display contract metadata, artifact card placeholders,
reference display placeholders, provenance display placeholders, lifecycle
badge placeholders, unavailable display responses, display safety helpers,
health metadata, and read-only display contract endpoints. It does not
implement active UI, frontend components, desktop components, file previews,
Research Artifact Registry implementation, active artifact ingestion/storage,
persistent storage, file upload/download, paper ingestion, paper parsing, PDF
parsing, arXiv ingestion, LLM paper analysis, strategy generation, strategy
code generation, signal/factor/alpha generation, backtesting, optimization,
recommendations, action generation, confidence scoring, active DecisionObject
generation or display, readiness-to-trade, broker controls, approvals,
overrides, real market data display, broker behavior, or execution APIs.

Prompt 73 audits Research Artifact Registry Planning and Guardrails, Research
Artifact Registry API Contract Skeleton, and Research Artifact Registry
Display Contract Skeleton. It adds safety boundary audit docs, API/display
boundary audit docs, no-active-ingestion/no-persistent-storage/no-upload-
download/no-active-UI/no-paper-parsing/no-strategy-generation/no-backtesting/
no-recommendation/no-execution audit docs, milestone readiness docs, tests,
audit coverage, verifier coverage, and status consolidation only. It does not
implement Research Artifact Registry functionality, active UI, frontend
components, desktop components, active artifact ingestion/storage, persistent
storage, file upload/download, paper parsing, PDF parsing, arXiv ingestion,
LLM paper analysis, strategy generation, backtesting, recommendations, broker
controls, approvals/overrides, readiness-to-trade, or execution APIs.

Prompt 74 audits Research Artifact Registry Planning and Guardrails, Research
Artifact Registry API Contract Skeleton, Research Artifact Registry Display
Contract Skeleton, and Research Artifact Registry Safety Boundary Audit. It
adds milestone audit docs, planning/API/display/safety milestone audit docs,
phase no-active-ingestion/storage, no-upload/download, no-active-UI,
no-paper-parsing, no-strategy-generation, no-backtesting, and
no-recommendation/no-execution audit docs, next-phase readiness docs, tests,
audit coverage, verifier coverage, and status consolidation only. It does not
implement Research Artifact Registry functionality, active UI, frontend
components, desktop components, active artifact ingestion/storage, persistent
storage, file upload/download, paper parsing, PDF parsing, arXiv ingestion,
LLM paper analysis, strategy generation, backtesting, recommendations, broker
controls, approvals/overrides, readiness-to-trade, or execution APIs.

Prompt 75 implements Research Artifact Registry System Boundary Hardening. It
adds artifact forbidden behavior registry contracts, endpoint boundary
policies, module boundary policies, cross-module invariant helpers, rejection
helpers, boundary health metadata, read-only boundary endpoints, stricter
audit/verifier coverage, tests, and status consolidation only. It does not
implement Research Artifact Registry functionality, active UI, frontend
components, desktop components, active artifact ingestion/storage, persistent
storage, file upload/download, file previews, paper parsing, PDF parsing,
arXiv ingestion, LLM paper analysis, strategy generation, backtesting,
recommendations, broker controls, approvals/overrides, readiness-to-trade, or
execution APIs.

Prompt 76 performs Research Artifact Registry API/Display Integration
Readiness Audit. It audits Research Artifact Registry planning and guardrails,
API contract skeleton, display contract skeleton, safety boundary audit,
milestone audit, system boundary hardening, cross-endpoint consistency,
API/display boundary integration, boundary integration, and Research Artifact
Index planning readiness. It does not implement Research Artifact Registry
functionality, Research Artifact Index functionality, active ingestion/storage,
upload/download, file previews, active UI, frontend components, desktop
components, paper parsing, PDF parsing, arXiv ingestion, LLM paper analysis,
strategy generation, backtesting, recommendations, broker controls,
approvals/overrides, readiness-to-trade, or execution APIs.

Prompt 39 implements Decision Safety and Human-Review Guardrails. It adds guardrails-only safety contracts, human-review gates, approval placeholders, override prohibition contracts, blocked output policy contracts, readiness templates, fail-closed settings, and read-only metadata endpoints. It does not generate recommendations, action states, confidence scores, active DecisionObjects, approvals, overrides, trading decisions, signals, broker behavior, or execution APIs.

Prompt 38 implements DecisionObject Evidence Bundle Contracts. It adds contracts-only evidence bundle schemas, evidence item contracts, source/provenance contracts, validation checklist contracts, human-review attachment contracts, readiness templates, fail-closed settings, and read-only metadata endpoints. It does not generate recommendations, action states, confidence scores, active DecisionObjects, trading decisions, signals, broker behavior, or execution APIs.

Prompt 36 implements Retail Decision Desk Planning and Guardrails. It adds planning contracts, action placeholders, evidence requirements, human-review guardrails, display boundaries, readiness templates, fail-closed settings, and read-only metadata endpoints. It does not generate recommendations, action states, confidence scores, DecisionObjects, trading decisions, signals, broker behavior, or execution APIs.

Prompt 33 Regime Analytics Planning and Guardrails remains planning/governance-only.

Prompt 32 Time-Series Diagnostics Foundation remains implemented and audited as a descriptive/data-quality-only layer.

## Architecture Direction

Stark Terminal is a cloud-brain plus Windows-native terminal:

- PySide6 / Qt 6 desktop client.
- FastAPI backend.
- REST API first.
- WebSockets later only if needed.
- Service-layer architecture separating UI, API, domain contracts, data platform, analytics engines, and infrastructure integrations.
- Oracle Cloud Free Tier first, with architecture that can scale to upgraded cloud resources.

## Infrastructure Stack Direction

Target infrastructure includes PostgreSQL, TimescaleDB, DuckDB, Parquet, Redis, Redis Streams, Kafka or Redpanda-compatible event bus, ClickHouse, Feast or custom Stark Feature Registry, worker pipelines, audit logs, and event logs.

## Analytical Stack Direction

Target analytics includes NumPy, SciPy, pandas, Polars, Numba, JAX, CuPy, statistical and time-series models, ML libraries, optimization, QuantLib and options analytics, risk analytics, backtesting engines, NLP, and research-paper understanding.

## Current Project Stats

- Target Version: v1.0
- Estimated Full Build: 110-150 prompts
- Current Prompt: 81
- Completed Prompts: 82 after completion
- Historical verifier reference: Current Prompt: 80
- Historical verifier reference: Completed Prompts: 81 after completion
- Historical verifier reference: Current Prompt: 79
- Historical verifier reference: Completed Prompts: 80 after completion
- Historical verifier reference: Current Prompt: 78
- Historical verifier reference: Completed Prompts: 79 after completion
- Historical verifier reference: Research Artifact Index Status: planning/guardrails and API contract skeleton only
- Completed Prompts: 56 before this prompt, 57 after completion
- Completed Prompts: 58 after completion
- Completed Prompts: 59 after completion
- Historical verifier reference: Completed Prompts: 60 after completion
- Completed Prompts: 61 after completion
- Completed Prompts: 62 after completion
- Historical verifier reference: Completed Prompts: 77 after completion
- Historical verifier reference: Completed Prompts: 76 after completion
- Historical verifier reference: Completed Prompts: 75 after completion
- Historical verifier reference: Completed Prompts: 74 after completion
- Historical verifier reference: Completed Prompts: 73 after completion
- Historical verifier reference: Completed Prompts: 72 after completion
- Historical verifier reference: Current Prompt: 68
- Historical verifier reference: Completed Prompts: 69 after completion
- Historical verifier reference: Current Prompt: 66
- Historical verifier reference: Completed Prompts: 67 after completion
- Historical verifier reference: Current Prompt: 65
- Historical verifier reference: Completed Prompts: 66 after completion
- Historical verifier reference: Current Prompt: 64
- Historical verifier reference: Completed Prompts: 65 after completion
- Historical verifier reference: Current Prompt: 63
- Historical verifier reference: Current Prompt: 62
- Historical verifier reference: Completed Prompts: 63 after completion
- Historical verifier reference: Current Prompt: 61
- Historical verifier reference: Current Prompt: 60
- Historical verifier reference: Current Prompt: 54
- Historical verifier reference: Completed Prompts: 54 before this prompt, 55 after completion
- Historical verifier reference: Completed Prompts: 55 after completion
- Historical verifier reference: Current Prompt: 53
- Historical verifier reference: Completed Prompts: 53 before this prompt, 54 after completion
- Historical verifier reference: Completed Prompts: 54 after completion
- Historical verifier reference: Current Prompt: 52
- Historical verifier reference: Completed Prompts: 52 before this prompt, 53 after completion
- Historical verifier reference: Completed Prompts: 53 after completion
- Historical verifier reference: Current Prompt: 51
- Historical verifier reference: Completed Prompts: 51 before this prompt, 52 after completion
- Historical verifier reference: Completed Prompts: 52 after completion
- Historical verifier reference: Current Prompt: 50
- Historical verifier reference: Completed Prompts: 50 before this prompt, 51 after completion
- Historical verifier reference: Completed Prompts: 51 after completion
- Historical verifier reference: Current Prompt: 49
- Historical verifier reference: Completed Prompts: 49 before this prompt, 50 after completion
- Historical verifier reference: Completed Prompts: 50 after completion
- Historical verifier reference: Current Prompt: 48
- Historical verifier reference: Completed Prompts: 48 before this prompt, 49 after completion
- Historical verifier reference: Completed Prompts: 49 after completion
- Historical verifier reference: Current Prompt: 47
- Historical verifier reference: Completed Prompts: 47 before this prompt, 48 after completion
- Historical verifier reference: Completed Prompts: 48 after completion
- Historical verifier reference: Current Prompt: 46
- Historical verifier reference: Completed Prompts: 46 before this prompt, 47 after completion
- Historical verifier reference: Completed Prompts: 47 after completion
- Historical verifier reference: Current Prompt: 45
- Historical verifier reference: Completed Prompts: 45 before this prompt, 46 after completion
- Historical verifier reference: Completed Prompts: 46 after completion
- Historical verifier reference: Current Prompt: 44
- Historical verifier reference: Completed Prompts: 44 before this prompt, 45 after completion
- Historical verifier reference: Completed Prompts: 45 after completion
- Historical verifier reference: Current Prompt: 43
- Historical verifier reference: Completed Prompts: 43 before this prompt, 44 after completion
- Historical verifier reference: Completed Prompts: 44 after completion
- Historical verifier reference: Current Prompt: 42
- Historical verifier reference: Completed Prompts: 42 before this prompt, 43 after completion
- Historical verifier reference: Completed Prompts: 43 after completion
- Historical verifier reference: Current Prompt: 41
- Historical verifier reference: Completed Prompts: 41 before this prompt, 42 after completion
- Historical verifier reference: Completed Prompts: 42 after completion
- Historical verifier reference: Current Prompt: 40
- Historical verifier reference: Completed Prompts: 40 before this prompt, 41 after completion
- Historical verifier reference: Completed Prompts: 41 after completion
- Historical verifier reference: Current Prompt: 39
- Historical verifier reference: Completed Prompts: 39 before this prompt, 40 after completion
- Historical verifier reference: Completed Prompts: 40 after completion
- Historical verifier reference: Current Prompt: 38
- Historical verifier reference: Completed Prompts: 38 before this prompt, 39 after completion
- Historical verifier reference: Current Prompt: 36
- Historical verifier reference: Completed Prompts: 36 before this prompt, 37 after completion
- Historical verifier reference: Completed Prompts: 35 before this prompt, 36 after completion
- Historical verifier reference: Completed Prompts: 26 before this prompt, 27 after completion
- Historical verifier reference: Completed Prompts: 27 before this prompt, 28 after completion
- Historical Milestone Reference: Quant/Time-Series Analytics Foundation Phase - Numerical Core Contracts
- Historical Milestone Reference: Returns and Rolling Window Analytics v0
- Historical Milestone Reference: Regime Analytics Planning Phase - Planning and Guardrails
- Historical Milestone Reference: Analytics/Regime Milestone Audit completed
- Current Milestone: Research Artifact Index Planning Phase - Safety Boundary Audit
- Historical Milestone Reference: Research Artifact Registry Planning Phase - API/Display Integration Readiness Audit completed
- Historical Milestone Reference: Research Artifact Registry Planning Phase - System Boundary Hardening
- Historical Milestone Reference: Research Artifact Registry Planning Phase - API Contract Skeleton
- Historical Milestone Reference: Strategy Research Workspace Planning Phase - Safety Boundary Audit
- Historical Milestone Reference: Strategy Research Workspace Planning Phase - Display Contract Skeleton
- Historical Milestone Reference: Strategy Research Workspace Planning Phase - API Contract Skeleton
- Historical Milestone Reference: Retail Trader Experience Planning Phase - System Boundary Hardening
- Historical Milestone Reference: Retail Trader Experience Planning Phase - Milestone Audit completed
- Historical Milestone Reference: Retail Dashboard Planning Phase - System Boundary Hardening
- Historical Milestone Reference: Retail Dashboard Planning Phase - Milestone Audit completed
- Historical Milestone Reference: Retail Dashboard Planning Phase - Safety Boundary Audit
- Historical Milestone Reference: Retail Dashboard Planning Phase - Display Contract Skeleton
- Historical Milestone Reference: Retail Dashboard Planning Phase - API Contract Skeleton
- Historical Milestone Reference: Retail Dashboard Planning Phase - Planning and Guardrails
- Historical Milestone Reference: Retail Decision Desk Planning Phase - API/Display Integration Readiness Audit completed
- Historical Milestone Reference: Retail Decision Desk Planning Phase - Decision Desk System Boundary Hardening
- Historical Milestone Reference: Retail Decision Desk Planning Phase - Decision Desk Milestone Audit 2 completed
- Historical Milestone Reference: Retail Decision Desk Planning Phase - Decision Desk Human Review Workflow Skeleton
- Historical Milestone Reference: Retail Decision Desk Planning Phase - Decision Desk Evidence Bundle Validation v0
- Historical Milestone Reference: Retail Decision Desk Planning Phase - Decision Desk Display Contract Skeleton
- Historical Milestone Reference: Retail Decision Desk Planning Phase - Decision Desk Readiness API Skeleton
- Historical Milestone Reference: Retail Decision Desk Planning Phase - Decision Desk Milestone Audit completed
- Historical Milestone Reference: Retail Decision Desk Planning Phase - Decision Desk API Contract Skeleton
- Historical Milestone Reference: Retail Decision Desk Planning Phase - Decision Safety and Human-Review Guardrails
- Historical Milestone Reference: Retail Decision Desk Planning Phase - DecisionObject Evidence Bundle Contracts
- Historical Milestone Reference: Retail Decision Desk Planning Phase - Planning and Guardrails
- Historical Milestone Reference: Quant/Time-Series Analytics Foundation Phase - Planning and Guardrails

## Current Capability Status

- Backend Status: Foundation health surface + Research Artifact Index planning/guardrails, API contract skeleton, display contract skeleton, and safety boundary audit complete
- Desktop Status: Skeleton only; no active Research Artifact Registry UI or Research Artifact Index UI implemented
- Data Platform Status: synthetic/local data and provider foundations complete; no real market ingestion
- Infrastructure Status: Existing foundations intact; analytics modules are pure compute layers only
- Data Layer Status: Validated synthetic/local fixtures + metadata persistence + synthetic/local provider responses/storage/export only; no real market ingestion
- Provider Status: Local Sample Provider and Local File Provider implemented; real provider implementation not started; no external calls
- Provider Adapter Status: Local Sample Provider and Local File Provider implemented and audited; real provider implementation not started; no external calls
- Historical Provider Status: Guardrails, readiness/candidate selection, local sample provider, and local file provider implemented and audited; no real provider implementation; no external calls
- Quant Engine Status: Descriptive analytics and regime planning complete; no signals, recommendations, decisions, backtests, or execution
- Regime Engine Status: Planning/guardrails only; no classification
- Decision Engine Status: decision desk planning/contracts/safety/API/readiness/display/evidence/human-review/boundary/integration complete; no active decisions or execution
- Retail Dashboard Status: complete through API/display integration readiness; no active UI, recommendations, broker controls, or execution
- Retail Trader Experience Status: complete through API/display integration readiness; no active UI, recommendations, suitability profiling, broker controls, or execution
- Strategy Research Workspace Status: planning/API/display/safety/milestone/boundary/integration readiness complete; no active UI, no paper parsing, no strategy generation, no backtesting, no recommendations, no execution
- Research Artifact Registry Status: planning/guardrails, API/display contract skeletons, safety/milestone audits, system boundary hardening, and API/display integration readiness audit complete; no implementation, no active ingestion/storage, no upload/download, no active UI, no frontend/desktop, no paper parsing, no strategy generation, no backtesting, no recommendations, no execution
- Research Artifact Index Status: planning/guardrails, API contract skeleton, display contract skeleton, and safety boundary audit complete; no implementation, no active UI, no frontend/desktop, no indexing/search/ranking/retrieval, no embeddings/vector store, no ingestion/storage, no upload/download/preview, no paper parsing, no strategy generation, no backtesting, no recommendations, no execution
- Historical Strategy Research Workspace Status: planning/guardrails, API/display contract skeletons, safety/milestone audits, and system boundary hardening implemented; no active UI, no paper ingestion/parsing, no strategy generation, no backtesting, no recommendations, no broker controls, no execution
- Historical Strategy Research Workspace Status: Planning/guardrails, API/display contract skeletons, and safety boundary audit complete; no active UI, no paper ingestion/parsing, no strategy generation, no backtesting, no recommendations, no broker controls, no execution
- Historical Strategy Research Workspace Status: Planning/guardrails, API contract skeleton, and display contract skeleton implemented; no active UI, no paper ingestion/parsing, no strategy generation, no backtesting, no recommendations, no broker controls, no execution
- Historical Strategy Research Workspace Status: Planning/guardrails and API contract skeleton implemented; no active UI, no paper ingestion/parsing, no strategy generation, no backtesting, no recommendations, no broker controls, no execution
- Historical Strategy Research Workspace Status: Planning and guardrails implemented; no active UI, no paper ingestion/parsing, no strategy generation, no backtesting, no recommendations, no broker controls, no execution
- Historical Retail Trader Experience Status: Planning/guardrails, API contract skeleton, and display contract skeleton implemented; no active UI, no frontend/desktop implementation, no recommendations, no suitability profiling, no broker controls, no execution
- Historical Retail Trader Experience Status: Ready for planning and guardrails only; no implementation yet
- Historical Retail Dashboard Status: Planning/guardrails, API/display contract skeletons, safety/milestone audits, and system boundary hardening implemented; no active UI, no recommendation cards, no broker controls, no execution
- Historical Retail Dashboard Status: Planning/guardrails, API contract skeleton, display contract skeleton, safety boundary audit, and milestone audit complete; no active UI, no recommendation cards, no broker controls, no execution
- Historical Retail Dashboard Status: Planning/guardrails, API contract skeleton, display contract skeleton, and safety boundary audit complete; no active UI, no recommendation cards, no broker controls, no execution
- Historical Retail Dashboard Status: Planning/guardrails, API contract skeleton, and display contract skeleton implemented; no active UI, no recommendation cards, no broker controls, no execution
- Historical Retail Dashboard Status: Planning/guardrails and API contract skeleton implemented; no active UI, no recommendation cards, no broker controls, no execution
- Historical Retail Dashboard Status: Planning and guardrails implemented; no active UI, no recommendation cards, no broker controls, no execution
- Historical Decision Engine Status: Decision Desk planning/guardrails, evidence contracts, safety guardrails, API/readiness/display skeletons, evidence validation v0, human review workflow skeleton, and system boundary hardening implemented; no recommendations, no confidence scoring, no active DecisionObject generation, no readiness-to-trade, no approvals, no overrides, no active UI, no active workflow, no execution
- Historical Decision Engine Status: Decision Desk planning/guardrails, evidence contracts, safety guardrails, API/readiness/display skeletons, evidence validation v0, and human review workflow skeleton implemented and audited; no recommendations, no confidence scoring, no active DecisionObject generation, no readiness-to-trade, no approvals, no overrides, no active workflow, no execution
- Historical Decision Engine Status: Decision Desk planning/guardrails, DecisionObject evidence bundle contracts, decision safety/human-review guardrails, Decision Desk API/readiness/display skeletons, evidence bundle validation v0, and human review workflow skeleton implemented; no recommendations, no confidence scoring, no active DecisionObject generation, no readiness-to-trade, no approvals, no overrides, no active workflow, no execution
- Historical Decision Engine Status: Decision Desk planning/guardrails, DecisionObject evidence bundle contracts, decision safety/human-review guardrails, Decision Desk API/readiness/display skeletons, and evidence bundle validation v0 implemented; no recommendations, no confidence scoring, no active DecisionObject generation, no readiness-to-trade, no approvals, no overrides, no execution
- Historical Decision Engine Status: Decision Desk planning/guardrails, DecisionObject evidence bundle contracts, decision safety/human-review guardrails, Decision Desk API skeleton, Decision Desk readiness API skeleton, and display contract skeleton implemented; no recommendations, no confidence scoring, no active DecisionObject generation, no readiness-to-trade, no approvals, no overrides, no execution
- Historical Decision Engine Status: Decision Desk planning/guardrails, DecisionObject evidence bundle contracts, decision safety/human-review guardrails, Decision Desk API skeleton, and Decision Desk readiness API skeleton implemented; no recommendations, no confidence scoring, no active DecisionObject generation, no readiness-to-trade, no approvals, no overrides, no execution
- Historical Decision Engine Status: Decision Desk planning/guardrails, DecisionObject evidence bundle contracts, decision safety/human-review guardrails, and Decision Desk API skeleton implemented and audited; no recommendations, no confidence scoring, no active DecisionObject generation, no approvals, no overrides, no execution
- Historical Decision Engine Status: Decision Desk planning/guardrails, DecisionObject evidence bundle contracts, decision safety/human-review guardrails, and Decision Desk API skeleton implemented; no recommendations, no confidence scoring, no active DecisionObject generation, no approvals, no overrides, no execution
- Historical Decision Engine Status: Decision Desk planning/guardrails, DecisionObject evidence bundle contracts, and Decision Safety human-review guardrails implemented; no recommendations, no confidence scoring, no active DecisionObject generation, no approvals, no overrides, no execution
- Historical Decision Engine Status: Decision Desk planning/guardrails and DecisionObject evidence bundle contracts implemented; no recommendations, no confidence scoring, no active DecisionObject generation, no execution
- Historical Decision Engine Status: Decision Desk planning and guardrails implemented; no recommendations, no confidence scoring, no DecisionObject generation, no execution
- Retail Console Status: Not started
- Historical Retail Dashboard Status: Ready for planning and guardrails only; no implementation yet
- Backtest Engine Status: Not started
- Options Layer Status: Not started
- Risk Engine Status: Not started
- ML Engine Status: Not started
- Feature Engine Status: Registry/contracts only; regime feature preparation contracts exist but no feature computation or registry writes
- Event Backbone Status: Kafka/Redpanda contracts/foundation only, no production pipelines
- Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence/safety/API/readiness/display/validation/human-review/boundary-hardening/dashboard/retail-trader-experience/strategy-research boundaries
- Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence/safety/API/readiness/display/validation/human-review/boundary-hardening/dashboard/API/display/safety-audit boundaries
- Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence/safety/API/readiness/display/validation/human-review/boundary-hardening/dashboard/API/display boundaries
- Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence/safety/API/readiness/display/validation/human-review/boundary-hardening/dashboard/API boundaries
- Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence/safety/API/readiness/display/validation/human-review/boundary-hardening/dashboard boundaries
- Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence/safety/API/readiness/display/validation/human-review/boundary-hardening boundaries
- Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence/safety/API/readiness/display/validation/human-review boundaries
- Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence/safety/API/readiness/display/validation boundaries
- Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence/safety/API/readiness/display boundaries
- Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence/safety/API/readiness boundaries
- Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence/safety/API boundaries
- Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence/safety boundaries
- Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence boundaries
- Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision-desk planning boundaries
- Historical Data Quality Status: Validation framework active for synthetic/local provider boundaries
- Fixture Status: Synthetic local-only test/dev fixtures implemented and audited
- Instrument Persistence Status: Instrument metadata repository/service wiring implemented
- Market Data Batch Persistence Status: Batch metadata repository/service wiring implemented; no production ingestion
- Synthetic OHLCV Storage Status: Synthetic-only repository/service wiring implemented; no real market data
- Synthetic OHLCV Export Status: Synthetic-only Parquet export contract with DatasetManifest linkage implemented; no real market data
- Paper Lab Status: Not started
- Deployment Status: Not started
- Execution APIs: Forbidden
- Development Environment: Mac mini M2 / macOS / Apple Silicon
- Target Desktop Product: Windows-native Stark Terminal
- Known Blockers: Ambient `python` command missing; use `.venv/bin/python`. Editable install may require local setuptools/build backend availability in restricted environments.
- Audit Verdict: ready for Research Artifact Index Milestone Audit only if tests pass
- Historical Audit Verdict: Research Artifact Index API Contract Skeleton implemented; ready for Research Artifact Index Display Contract Skeleton only if tests pass
- Historical Audit Verdict: Research Artifact Registry system boundary hardening implemented; ready for Research Artifact Registry API/Display Integration Readiness Audit only if tests pass
- Historical Audit Verdict: Research Artifact Registry milestone audit complete; ready for Research Artifact Registry System Boundary Hardening only if tests pass
- Historical Audit Verdict: Research Artifact Registry Safety Boundary Audit complete; ready for Research Artifact Registry Milestone Audit only if tests pass
- Historical Audit Verdict: Research Artifact Registry Display Contract Skeleton implemented; ready for Safety Boundary Audit only if tests pass
- Historical Audit Verdict: Strategy Research Workspace system boundary hardening implemented; ready for API/display integration readiness audit only if tests pass
- Historical Audit Verdict: Strategy Research Workspace Safety Boundary Audit complete; ready for Strategy Research Workspace Milestone Audit if tests pass
- Historical Audit Verdict: Strategy Research Workspace Display Contract Skeleton implemented; ready for Safety Boundary Audit if tests pass
- Historical Audit Verdict: Strategy Research Workspace API Contract Skeleton implemented; ready for Display Contract Skeleton if tests pass
- Historical Audit Verdict: Strategy Research Workspace Planning and Guardrails implemented; ready for API contract skeleton if tests pass
- Historical Audit Verdict: Ready for Strategy Research Workspace Planning and Guardrails only if tests pass
- Historical Audit Verdict: Retail Trader Experience Safety Boundary Audit complete; ready for Retail Trader Experience Milestone Audit if tests pass
- Historical Audit Verdict: Retail Trader Experience Display Contract Skeleton implemented; ready for Retail Trader Experience Safety Boundary Audit if tests pass
- Historical Audit Verdict: Ready for Retail Trader Experience Planning and Guardrails only if tests pass
- Historical Audit Verdict: Retail Dashboard System Boundary Hardening implemented; ready for API/display integration readiness audit if tests pass
- Historical Audit Verdict: Retail Dashboard planning phase ready for system boundary hardening if tests pass
- Historical Audit Verdict: Retail Dashboard Safety Boundary Audit complete; ready for Retail Dashboard Milestone Audit if tests pass
- Historical Audit Verdict: Retail Dashboard Display Contract Skeleton implemented; ready for Retail Dashboard Safety Boundary Audit if tests pass
- Historical Audit Verdict: Retail Dashboard API Contract Skeleton implemented; ready for Retail Dashboard Display Contract Skeleton if tests pass
- Historical Audit Verdict: Retail Dashboard Planning and Guardrails implemented; ready for Retail Dashboard API Contract Skeleton if tests pass
- Historical Audit Verdict: Ready for Retail Dashboard Planning and Guardrails only if tests pass
- Historical Audit Verdict: Decision Desk System Boundary Hardening implemented; ready for API/display integration readiness audit if tests pass
- Historical Audit Verdict: Decision Desk skeleton phase ready for system boundary hardening if tests pass
- Historical Audit Verdict: Decision Desk Human Review Workflow Skeleton implemented; ready for Decision Desk Milestone Audit 2 if tests pass
- Historical Audit Verdict: Decision Desk Evidence Bundle Validation v0 implemented; ready for Decision Desk Human Review Workflow Skeleton if tests pass
- Historical Audit Verdict: Decision Desk Display Contract Skeleton implemented; ready for Decision Desk Evidence Bundle Validation v0 if tests pass
- Historical Audit Verdict: Decision Desk Readiness API Skeleton implemented; ready for Decision Desk Display Contract Skeleton if tests pass
- Historical Audit Verdict: Decision Desk planning foundation ready for next read-only skeleton phase if tests pass
- Historical Audit Verdict: Decision Desk API Contract Skeleton implemented; ready for Decision Desk Milestone Audit if tests pass
- Historical Audit Verdict: Decision Safety and Human-Review Guardrails implemented; ready for Decision Desk API Contract Skeleton if tests pass
- Historical Audit Verdict: DecisionObject evidence bundle contracts implemented; ready for Decision Safety and Human-Review Guardrails if tests pass
- Historical Audit Verdict: Retail Decision Desk planning and guardrails implemented; ready for DecisionObject evidence bundle contracts if tests pass

## Hard Exclusions

- Live order placement
- Broker execution
- Auto-trading
- Real-money routing
- Broker credential vaults
- Hidden background trading
- Autonomous LLM trading
- High-frequency trading execution systems
- Payment systems
- Social/community features
- Production secrets
- Real API keys
- Scraping code that violates provider terms

## Current Milestone Plan

Prompt 63 completes Strategy Research Workspace Planning and Guardrails. Prompt 64 implements the Strategy Research Workspace API Contract Skeleton only. Prompt 65 implements the Strategy Research Workspace Display Contract Skeleton only. Prompt 66 performs the Strategy Research Workspace Safety Boundary Audit only. Prompt 67 performs the Strategy Research Workspace Milestone Audit only. Prompt 68 implements Strategy Research Workspace System Boundary Hardening only. Prompt 69 performs Strategy Research Workspace API/Display Integration Readiness Audit only. Prompt 70 implements Research Artifact Registry Planning and Guardrails only. Prompt 71 implements Research Artifact Registry API Contract Skeleton only. Prompt 72 implements Research Artifact Registry Display Contract Skeleton only. Prompt 73 performs Research Artifact Registry Safety Boundary Audit only. Prompt 74 performs Research Artifact Registry Milestone Audit only. Prompt 75 implements Research Artifact Registry System Boundary Hardening only. Prompt 76 performs Research Artifact Registry API/Display Integration Readiness Audit only. Prompt 77 implements Research Artifact Index Planning and Guardrails only. Prompt 78 implements Research Artifact Index API Contract Skeleton only. Prompt 79 implements Research Artifact Index Display Contract Skeleton only. Prompt 80 performs Research Artifact Index Safety Boundary Audit only. Prompt 81 should perform Research Artifact Index Milestone Audit only. Real market ingestion, provider-specific live clients, provider SDKs, credentials, scraping, ClickHouse writes, production validation pipelines, production event pipelines, production dashboards, active Retail Dashboard UI, active Retail Trader Experience UI, active Strategy Research Workspace UI, active Research Artifact Index UI, frontend components, desktop UI components, Research Artifact Registry implementation, Research Artifact Index implementation, indexing, search, ranking, retrieval, embeddings, vector stores, active ingestion/storage, persistent storage, file upload/download/preview, recommendation cards, broker controls, suitability profiling, Feast integration, feature computation, indicators, actual regime classification, recommendation generation, strategy generation, backtesting engines, action-state generation, confidence scoring, DecisionObject generation, active UI surfaces, active human-review workflows, approvals, overrides, readiness-to-trade, execution APIs, and deployment hardening remain deferred to later prompts.

## Prompt 77 Research Artifact Index Status

Current Milestone: Research Artifact Index Planning Phase - Planning and Guardrails.

Research Artifact Registry Status: planning/guardrails, API/display contract skeletons, safety/milestone audits, system boundary hardening, and API/display integration readiness audit complete; no implementation.

Research Artifact Index Status: planning and guardrails only; no implementation, no indexing/search/ranking/retrieval, no embeddings/vector store, no ingestion/storage, no paper parsing, no strategy generation, no backtesting, no recommendations, no execution.

Active Decision Architecture Target: documented as future target only; decision candidate is not a trade; execution APIs remain forbidden.

Execution APIs: Forbidden.

Development environment: Mac mini M2 / macOS / Apple Silicon.

Target desktop product: Windows-native Stark Terminal.

Audit Verdict: ready for Research Artifact Index API Contract Skeleton only if tests pass.

## Prompt 78 Research Artifact Index API Status

Current Milestone: Research Artifact Index Planning Phase - API Contract Skeleton.

Research Artifact Index Status: planning/guardrails and API contract skeleton
only; no implementation, no indexing/search/ranking/retrieval, no
embeddings/vector store, no ingestion/storage, no upload/download/preview, no
paper parsing, no strategy generation, no backtesting, no recommendations, no
execution.

Active Decision Architecture Target: documented as future target only;
decision candidate is not a trade; execution APIs remain forbidden.

Execution APIs: Forbidden.

Development environment: Mac mini M2 / macOS / Apple Silicon.

Target desktop product: Windows-native Stark Terminal.

Audit Verdict: ready for Research Artifact Index Display Contract Skeleton
only if tests pass.

## Prompt 79 Research Artifact Index Display Status

Current Milestone: Research Artifact Index Planning Phase - Display Contract Skeleton.

Research Artifact Index Status: planning/guardrails, API contract skeleton, and display contract skeleton only; no implementation, no active UI, no frontend/desktop, no indexing/search/ranking/retrieval, no embeddings/vector store, no ingestion/storage, no upload/download/preview, no paper parsing, no strategy generation, no backtesting, no recommendations, no execution.

Active Decision Architecture Target: documented as future target only; decision candidate is not a trade; execution APIs remain forbidden.

Execution APIs: Forbidden.

Development environment: Mac mini M2 / macOS / Apple Silicon.

Target desktop product: Windows-native Stark Terminal.

Audit Verdict: ready for Research Artifact Index System Boundary Hardening only if tests pass.

## Prompt 81 Research Artifact Index Milestone Audit Status

Current Milestone: Research Artifact Index Planning Phase - Milestone Audit completed.

Research Artifact Index Status: planning/guardrails, API contract skeleton,
display contract skeleton, safety boundary audit, and milestone audit complete;
no implementation, no active UI, no frontend/desktop, no
indexing/search/ranking/retrieval, no embeddings/vector store, no
ingestion/storage, no upload/download/preview, no paper parsing, no strategy
generation, no backtesting, no recommendations, no execution.

Verifier status phrase: Research Artifact Index Status: planning/guardrails, API contract skeleton, display contract skeleton, safety boundary audit, and milestone audit complete; no implementation, no active UI, no frontend/desktop, no indexing/search/ranking/retrieval, no embeddings/vector store, no ingestion/storage, no upload/download/preview, no paper parsing, no strategy generation, no backtesting, no recommendations, no execution.

Documentation/Test Policy: phase-level docs/tests preferred over prompt-level audit sprawl.

Active Decision Architecture Target: documented as future target only; decision candidate is not a trade; execution APIs remain forbidden.

Execution APIs: Forbidden.

Development environment: Mac mini M2 / macOS / Apple Silicon.

Target desktop product: Windows-native Stark Terminal.

Audit Verdict: ready for Research Artifact Index System Boundary Hardening only if tests pass.

Next Recommended Prompt: Prompt 82 - Research Artifact Index System Boundary Hardening.

## Prompt 80 Research Artifact Index Safety Boundary Audit Status

Current Milestone: Research Artifact Index Planning Phase - Safety Boundary Audit.

Research Artifact Index Status: planning/guardrails, API contract skeleton, display contract skeleton, and safety boundary audit complete; no implementation, no active UI, no frontend/desktop, no indexing/search/ranking/retrieval, no embeddings/vector store, no ingestion/storage, no upload/download/preview, no paper parsing, no strategy generation, no backtesting, no recommendations, no execution.

Active Decision Architecture Target: documented as future target only; decision candidate is not a trade; execution APIs remain forbidden.

Execution APIs: Forbidden.

Development environment: Mac mini M2 / macOS / Apple Silicon.

Target desktop product: Windows-native Stark Terminal.

Audit Verdict: ready for Research Artifact Index Milestone Audit only if tests pass.

## Prompt Log Rule

Every completed prompt must update `docs/PROMPT_LOG.md`. Product status or structure changes must also update `docs/NORTH_STAR.md` and `PROJECT_MAP.md`.
