# Stark Terminal

Windows-native Indian-market trading research and decision terminal powered by an institutional-grade Oracle Cloud quant backend.

## Product Philosophy

Evidence before decision. Safety before execution. Research before automation. Decision support before trading. Institution-grade infrastructure from day one.

## Active Decision Architecture Target

Stark Terminal now documents the future active decision architecture target:
Market data -> Data quality + provenance layer -> Timeseries engine -> Feature
/ regime / state engine -> Deterministic quant engine -> Decision candidate ->
Verifier layer -> Human review / paper-trade gate -> Audit log + journal.
This is documentation only. Decision candidate is not a trade, and execution
APIs remain forbidden.

## Documentation/Test Consolidation

The repo now has a phase-based documentation and test policy. Grouped docs in
`docs/phases/`, grouped audits in `docs/audits/`, and grouped tests in
`tests/phases/` and `tests/boundaries/` are the preferred navigation layer for
future work. Historical prompt-level audit files remain preserved for
traceability, but new prompts should avoid unnecessary audit sprawl. Safety
before execution remains mandatory.

Archive Pass 1 moved obvious superseded Research Artifact Index Prompt 80
micro-audit docs/tests into `docs/archive/prompt_audits/` and
`tests/archive/prompt_audits/`. Archived tests are historical references and
are not collected by pytest.

Archive Pass 2 moves older Strategy Research Workspace and Research Artifact
Registry `NO_*` micro-audit docs/tests into phase-specific archive folders.
No product capability is added; grouped phase and boundary docs/tests remain
the active safety coverage.

The aggressive grouped report cleanup creates `docs/reports/` and deletes
previously archived superseded micro-audit files after preserving their details
in grouped reports. Future prompts should continue with phase-level docs/tests
and focused product behavior tests.

## Current Status

Prompt 107 Retail Decision Console Internal Preview Milestone Closure.

Prompt 107 closes the Retail Decision Console internal preview milestone. The
milestone now includes the productization plan, UI shell skeleton, demo/static
state model, desktop state wiring, local preview runbook, manual smoke test,
visual layout pass, static interaction placeholders, preview snapshot export,
local QA bundle, manual acceptance checklist, shareable internal preview
package, and smoke verification. The preview remains static/demo,
unavailable, local-only, read-only, and safe for internal local preview only.
It is not production ready, not trading ready, not recommendation ready, and
not execution ready. It adds no live data, recommendations, action generation,
confidence scoring, active DecisionObjects, broker controls, order buttons,
execution paths, production package, Windows installer, signed binary, or
deployment automation. Commit/push is recommended before Prompt 108 - Retail
Decision Console Post-Preview UX Backlog and Next Product Phase Selection.

Prompt 106 Retail Decision Console Internal Preview Package Smoke Verification.

Prompt 106 smoke-verifies the Retail Decision Console internal preview
package. It adds a local smoke verification helper, a safe smoke verification
script, grouped tests, and status documentation only. The smoke verification
checks required internal preview artifacts, manifest safety/readiness markers,
README clarity, runbook/checklist/template inclusion, snapshot artifacts,
no-GUI output, and safety summary content. It adds no live data,
recommendations, action generation, confidence scoring, active DecisionObjects,
broker controls, order buttons, execution paths, production package, Windows
installer, signed binary, or deployment automation. Prompt 107 - Retail
Decision Console Internal Preview Milestone Closure is the next recommended
prompt.

Prompt 105 Retail Decision Console Shareable Internal Preview Package.

Prompt 105 creates a safe local internal preview package structure for the
Retail Decision Console static/demo product surface. It adds an internal
preview package manifest/builder, an internal preview runbook, an internal
review notes template, and grouped tests only. The package collects the preview
runbook, manual smoke test, local QA bundle runbook, manual acceptance
checklist, preview snapshot artifacts, no-GUI summary, safety summary, README,
and review notes. It is not production ready, not trading ready, not
recommendation ready, and not execution ready. It adds no live data,
recommendations, action generation, confidence scoring, active DecisionObjects,
broker controls, order buttons, execution paths, production packaging, or
Windows installer. Prompt 106 - Retail Decision Console Internal Preview
Package Smoke Verification is the next recommended prompt.

Prompt 104 Retail Decision Console Manual Acceptance Checklist.

Prompt 104 defines the human acceptance checklist for the current Retail
Decision Console static/demo product surface before internal sharing or local
review. It adds a manual acceptance checklist runbook and grouped tests only.
The acceptance scope is local demo preview only. It is not production
acceptance, not trading-readiness acceptance, not recommendation-readiness
acceptance, and not execution-readiness acceptance. It adds no live data,
recommendations, action generation, confidence scoring, active DecisionObjects,
broker controls, order buttons, execution paths, production packaging, or live
market-data integration. Prompt 105 - Retail Decision Console Shareable
Internal Preview Package is the next recommended prompt.

Prompt 103 Retail Decision Console Local QA Bundle.

Prompt 103 creates a safe local QA bundle for the Retail Decision Console
static/demo product surface. The bundle writes a manifest, preview snapshot
JSON, preview snapshot Markdown, no-GUI preview text, safety summary, and
runbook copies under a local output directory. The bundle remains demo-only,
unavailable, local-only, read-only, and non-executive. It contains no
secrets, credentials, live data, recommendations, confidence scores, active
DecisionObjects, broker controls, order buttons, or execution paths. Prompt
104 - Retail Decision Console Manual Acceptance Checklist is the next
recommended prompt.

Prompt 102 Retail Decision Console Preview Snapshot Export.

Prompt 102 adds safe local-only preview snapshot export for the Retail
Decision Console static/demo shell. It supports stdout snapshots and local
JSON, Markdown, and text files generated from the static shell view-model.
Snapshots remain demo-only, unavailable, local-only, read-only, and
non-executive. They contain no secrets, credentials, live data,
recommendations, confidence scores, active DecisionObjects, broker controls,
order buttons, or execution paths. Prompt 103 - Retail Decision Console Local
QA Bundle is the next recommended prompt.

Prompt 101 Retail Decision Console Static Interaction Placeholders.

Prompt 101 adds local-only static interaction descriptors, view-model
exposure, desktop placeholder display, and clearer preview output for the
Retail Decision Console static/demo shell. Interactions remain demo-only,
unavailable, read-only, local-only, and non-executive. They add no live data,
generated recommendations, confidence scores, active DecisionObjects, broker
controls, order buttons, or execution path.

Prompt 100 Retail Decision Console Visual Polish and Section Layout Pass.

Prompt 100 improves the Retail Decision Console static/demo shell layout with
visual layout descriptors, section grouping, card ordering metadata, and
clearer preview output. The shell remains demo/static, unavailable, and
non-executive. It adds no live data, generated recommendations, confidence
scores, active DecisionObjects, broker controls, order buttons, or execution
path.

Prompt 99 Retail Decision Console Local Preview Runbook and Manual Smoke Test.

Prompt 99 makes the Retail Decision Console static/demo shell safely
previewable locally through runbooks, a manual smoke test checklist, and a
safe preview helper script. The preview remains demo/static, unavailable, and
non-executive.

Prompt 98 Retail Decision Console Static State Wiring into Desktop Shell.

Prompt 98 wires deterministic demo/static state into a safe shell view-model
and desktop fallback/rendering path. The shell remains demo-only,
unavailable, read-only, and non-executive.

Prompt 96 Retail Decision Console UI Shell Skeleton.

Prompt 96 adds a static Retail Decision Console desktop shell skeleton with
testable UI descriptors and safe placeholder sections. The shell is
skeleton/demo only and shows no live data, generated recommendations,
confidence scores, active DecisionObjects, broker controls, order buttons, or
execution path.

Prompt 95 Retail Decision Console Productization Plan and UI Shell Boundary.

Prompt 95 creates the canonical
`docs/phases/retail_decision_console.md` phase doc, the
`stark_terminal_core.retail_decision_console` product surface package, and
GET-only read-only Retail Decision Console metadata endpoints. This is a
productization plan and UI shell boundary only. It adds no live decisions,
active recommendations, action generation, confidence scoring, active
DecisionObject generation, live market-data claims, broker controls, order
buttons, or execution APIs. Prompt 96 - Retail Decision Console UI Shell
Skeleton is the next recommended prompt.

Prompt 94 Product Surface Reorientation and Development Plan.

Prompt 94 creates the canonical
`docs/phases/product_surface_reorientation.md` plan and moves the roadmap
toward Prompt 95 - Retail Decision Console Productization Plan and UI Shell
Boundary. It adds no product runtime capability, API route, package, active UI,
broker control, recommendation, confidence score, active DecisionObject,
strategy generation, backtesting, live market-data ingestion, or execution
API.

Research Knowledge Map planning/guardrails, API contract skeleton, display
contract skeleton, safety boundary audit, and phase closure are complete as
read-only, unavailable-by-default planning/contract/audit layers only. No
active knowledge map, active UI, frontend/desktop components, database,
tables, migrations, persistent writes, traversal, query, search, ranking,
retrieval, embeddings/vector store, ingestion/storage, upload/download/
preview, paper parsing, strategy generation, backtesting, recommendations,
broker controls, or execution APIs exist.

Research Artifact Index planning, API contract skeleton, display contract
skeleton, safety boundary audit, milestone audit, system boundary hardening,
and API/display integration readiness audit are complete as read-only
planning/contract/audit layers. Prompt 84 added Research Metadata Graph
planning contracts, graph node/edge/provenance/lifecycle/reference
placeholders, guardrails, readiness metadata, and GET-only planning endpoints.
Prompt 85 adds a read-only Research Metadata Graph API contract skeleton with
request placeholders, response placeholders, reference placeholders,
unavailable responses, safety helpers, health metadata, and GET-only API
metadata endpoints. Prompt 86 adds a backend-only Research Metadata Graph
Display Contract Skeleton with node, edge, provenance, lifecycle, reference,
unavailable, safety, health, and GET-only display metadata endpoints. Prompt
87 performs the grouped Research Metadata Graph Safety Boundary Audit only.
Prompt 88-B closes the Research Metadata Graph phase in the canonical phase
doc and enforces phase-level docs/tests for future work. This adds no active
UI, no frontend/desktop implementation, no active graph implementation, no
graph database, no graph traversal/search/ranking/retrieval, no
embeddings/vector store, no ingestion/storage, no upload/download/preview, no
paper parsing, no strategy generation, no backtesting, no recommendations, no
broker controls, and no execution APIs.

This repository currently contains the verified foundation only: project control documents, institutional architecture documentation, Prompt 11 audit artifacts, Prompt 17 data foundation audit artifacts, Prompt 22 data foundation milestone audit artifacts, Prompt 25 provider adapter milestone audit artifacts, Prompt 26 analytics foundation plan artifacts, Prompt 27 numerical analytics core contract artifacts, Prompt 28 returns/rolling analytics artifacts, Prompt 29 volatility/drawdown analytics artifacts, Prompt 30 analytics milestone audit artifacts, Prompt 31 correlation/beta analytics artifacts, Prompt 32 time-series diagnostics artifacts, Prompt 33 regime analytics planning/guardrail artifacts, Prompt 34 regime feature preparation contract artifacts, Prompt 35 analytics/regime milestone audit artifacts, Prompt 36 Retail Decision Desk planning/guardrail artifacts, Prompt 38 DecisionObject evidence bundle contract artifacts, Prompt 39 Decision Safety and Human-Review Guardrail artifacts, Prompt 40 Decision Desk API Contract Skeleton artifacts, Prompt 41 Decision Desk Milestone Audit artifacts, Prompt 42 Decision Desk Readiness API Skeleton artifacts, Prompt 43 Decision Desk Display Contract Skeleton artifacts, Prompt 44 Decision Desk Evidence Bundle Validation v0 artifacts, Prompt 45 Decision Desk Human Review Workflow Skeleton artifacts, Prompt 46 Decision Desk Milestone Audit 2 artifacts, Prompt 47 Decision Desk System Boundary Hardening artifacts, Prompt 48 Decision Desk API/Display Integration Readiness Audit artifacts, Prompt 49 Retail Dashboard Planning and Guardrails artifacts, Prompt 50 Retail Dashboard API Contract Skeleton artifacts, Prompt 51 Retail Dashboard Display Contract Skeleton artifacts, Prompt 52 Retail Dashboard Safety Boundary Audit artifacts, Prompt 53 Retail Dashboard Milestone Audit artifacts, Prompt 54 Retail Dashboard System Boundary Hardening artifacts, Prompt 55 Retail Dashboard API/Display Integration Readiness Audit artifacts, Prompt 56 Retail Trader Experience Planning and Guardrails artifacts, Prompt 57 Retail Trader Experience API Contract Skeleton artifacts, Prompt 58 Retail Trader Experience Display Contract Skeleton artifacts, Prompt 59 Retail Trader Experience Safety Boundary Audit artifacts, Prompt 60 Retail Trader Experience Milestone Audit artifacts, Prompt 61 Retail Trader Experience System Boundary Hardening artifacts, Prompt 62 Retail Trader Experience API/Display Integration Readiness Audit artifacts, Prompt 63 Strategy Research Workspace Planning and Guardrails artifacts, Prompt 64 Strategy Research Workspace API Contract Skeleton artifacts, Prompt 65 Strategy Research Workspace Display Contract Skeleton artifacts, Prompt 66 Strategy Research Workspace Safety Boundary Audit artifacts, Prompt 67 Strategy Research Workspace Milestone Audit artifacts, Prompt 68 Strategy Research Workspace System Boundary Hardening artifacts, Prompt 69 Strategy Research Workspace API/Display Integration Readiness Audit artifacts, Prompt 70 Research Artifact Registry Planning and Guardrails artifacts, Prompt 71 Research Artifact Registry API Contract Skeleton artifacts, Prompt 72 Research Artifact Registry Display Contract Skeleton artifacts, Prompt 73 Research Artifact Registry Safety Boundary Audit artifacts, Prompt 74 Research Artifact Registry Milestone Audit artifacts, Prompt 75 Research Artifact Registry System Boundary Hardening artifacts, Prompt 76 Research Artifact Registry API/Display Integration Readiness Audit artifacts, Prompt 77 Research Artifact Index Planning and Guardrails artifacts, Prompt 78 Research Artifact Index API Contract Skeleton artifacts, Prompt 79 Research Artifact Index Display Contract Skeleton artifacts, Prompt 80 Research Artifact Index Safety Boundary Audit artifacts, provider readiness/candidate selection governance, package skeletons, typed configuration, core domain schemas, SQLAlchemy/Alembic metadata persistence foundation, Instrument Metadata Persistence Wiring, Market Data Batch Persistence Contracts, TimescaleDB-oriented operational time-series schema foundation, TimescaleDB Synthetic OHLCV Storage Foundation, Synthetic OHLCV Research Lake Export Contract, Provider Adapter Guardrails, Local Sample Provider Adapter v0, Local File Provider Adapter v0, DuckDB + Parquet research lake foundation, Redis cache foundation, Redis Streams event pipeline foundation, Kafka/Redpanda Event Backbone foundation, Data Quality + Validation Framework, Synthetic Market Data Fixtures, Worker System foundation, Instrument Master/Provider Contracts foundation, ClickHouse Warehouse foundation, Feature Registry foundation, FastAPI health/config/database-health/timeseries-health/research-lake-health/cache-health/streams-health/event-backbone-health/data-quality-health/fixtures-health/instrument-metadata-health/market-data-batches-health/synthetic-ohlcv-storage-health/synthetic-ohlcv-exports-health/provider-guardrails-health/provider-readiness-health/local-sample-provider-health/local-file-provider-health/analytics-foundation-health/numerical-analytics-health/returns-analytics-health/risk-analytics-health/relationship-analytics-health/time-series-diagnostics-health/regime-analytics-health/regime-features-health/decision-desk-health/decision-evidence-health/decision-safety-health/decision-desk-api-health/decision-readiness-api-health/decision-display-health/decision-evidence-validation-health/decision-human-review-health/decision-boundary-health/retail-dashboard-health/retail-dashboard-api-health/retail-dashboard-display-health/retail-dashboard-boundary-health/retail-trader-experience-health/retail-trader-experience-api-health/retail-trader-experience-display-health/retail-trader-experience-boundary-health/strategy-research-workspace-health/strategy-research-workspace-api-health/strategy-research-workspace-display-health/strategy-research-workspace-boundary-health/research-artifact-registry-health/research-artifact-registry-api-health/research-artifact-registry-display-health/research-artifact-registry-boundary-health/research-artifact-index-health/research-artifact-index-api-health/research-artifact-index-display-health/workers-health/instrument-health/provider-health/warehouse-health/feature-registry-health surfaces, a minimal PySide6 desktop shell placeholder, an enriched DecisionObject schema placeholder, tests, an audit script, and a verification script.

## High-Level Architecture

Stark Terminal is designed as a cloud-brain plus Windows-native terminal:

- Windows-native desktop client built with PySide6 / Qt 6.
- FastAPI backend designed for Oracle Cloud Free Tier first and scalable cloud upgrades later.
- REST API first; WebSockets only when a later use case requires them.
- Core domain contracts shared by backend, analytics, and future worker pipelines.
- Institutional-grade data and analytics architecture locked in documentation before implementation.

Stark Terminal intentionally targets an institutional-grade stack, including PostgreSQL, TimescaleDB, DuckDB, Parquet, Redis, Redis Streams, Kafka or Redpanda-compatible event replay, data quality gates, synthetic local test fixtures, repository/service persistence layers, worker pipelines, Instrument Master/Provider Contracts, Provider Adapter Guardrails, provider readiness governance, Local Sample Provider Adapter v0, Local File Provider Adapter v0, ClickHouse Warehouse, a custom Stark Feature Registry, and future Feast evaluation. Current prompts implement only controlled foundations, data-foundation milestone audit coverage, provider adapter milestone audit coverage, synthetic-only OHLCV storage, synthetic-only research lake export contracts, provider guardrails, provider candidate selection/risk scoring, a synthetic/local-only provider adapter, a local-file-only test/dev provider adapter, analytics foundation planning contracts, numerical analytics contracts with tiny descriptive count/min/max/mean helpers, descriptive simple/log returns plus rolling count/mean/min/max, descriptive volatility/drawdown metrics, descriptive correlation/beta metrics, descriptive time-series timestamp diagnostics, regime analytics planning/guardrails, regime feature preparation contracts, analytics/regime milestone audit coverage, Retail Decision Desk planning/guardrail contracts, DecisionObject evidence bundle contracts, Decision Safety human-review guardrails, Decision Desk API contract skeleton unavailable responses, Decision Desk milestone audit coverage, Decision Desk Readiness API skeleton unavailable responses, Decision Desk Display contract skeleton unavailable responses, Decision Evidence Validation v0 contract checks, Decision Human Review workflow skeleton placeholders, Decision Boundary hardening contracts, Decision API/display integration readiness audit artifacts, Retail Dashboard planning/guardrail placeholders, Retail Dashboard API contract skeleton placeholders, Retail Dashboard Display contract skeleton placeholders, Retail Dashboard boundary hardening contracts, Retail Dashboard API/display integration readiness audit artifacts, and Retail Trader Experience planning/guardrail placeholders; production Kafka/Redpanda pipelines, Feast integration, real production workers, real market data ingestion, external provider calls, live provider clients, provider SDKs, scraping, credentials, production approval, arbitrary file read APIs, production OHLCV ingestion, production dashboards, active Retail Dashboard UI, active Retail Trader Experience UI, frontend components, desktop UI components, suitability profiling, recommendation cards, broker controls, Retail Dashboard implementation, Retail Trader Experience implementation, active Decision Desk implementation, active human review workflow, task assignment, reviewer auth, notifications, readiness-to-trade generation, active DecisionObject generation, approvals, overrides, recommendation generation, action generation, confidence scoring, feature computation, feature registry writes, classifier inputs, production validation pipelines, stationarity tests, actual regime classification, regime detection, backtests, computed regimes, and analytics signals remain deferred.

## Local Development

Create and activate a Python 3.11+ virtual environment, then install the project in editable mode:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Run the API health endpoint:

```bash
uvicorn stark_terminal_api.main:app --app-dir apps/api --reload
```

Run tests:

```bash
pytest
```

Run foundation verification:

```bash
python scripts/verify_foundation.py
```

Run the milestone audit:

```bash
python scripts/audit_foundation.py
```

Optional desktop shell dependency:

```bash
python -m pip install -e ".[desktop]"
python apps/desktop/stark_terminal_desktop/main.py
```

## Safety Note

Stark Terminal is decision support only. Current foundations include no live trading, no broker execution, no order placement, no real-money routing, no broker credential vaults, no autonomous trading, no real market data ingestion, no scraping, no external provider calls, no provider SDKs, no provider credentials, no production approval, no arbitrary file read API, no automatic ClickHouse table creation, no production OHLCV ingestion, no feature computation, no backtests, no computed regimes, no analytics signals, no active DecisionObject generation, no approvals, no overrides, no confidence scoring, no action generation, and no recommendations. Instrument metadata persistence and market data batch persistence are metadata-only and validation-gated. Synthetic OHLCV storage is synthetic-only and validation-gated. Provider guardrails and provider readiness scoring remain fail-closed governance. Local Sample Provider Adapter v0 uses synthetic/local/test data only. Local File Provider Adapter v0 uses explicit local test/dev files under path-safety checks only. Analytics foundation contracts are descriptive/research-only planning artifacts. Numerical analytics contracts allow only descriptive count/min/max/mean helpers. Returns and rolling analytics v0 allows descriptive simple/log returns and rolling count/mean/min/max only. Volatility and drawdown analytics v0 allows descriptive standard deviation, annualized volatility with explicit periods_per_year, drawdown series, max drawdown, and drawdown duration only. Correlation and beta analytics v0 allows descriptive Pearson correlation and sample-covariance beta only. Time-Series Diagnostics Foundation allows descriptive/data-quality-only timestamp order, duplicate timestamp, gap, irregular interval, and spacing diagnostics only. Regime Analytics Planning and Guardrails allows planning-only label placeholders, evidence requirements, safety policy, readiness templates, dependency staging, and roadmap metadata only; it does not classify regimes or market states. Retail Decision Desk Planning and Guardrails allows planning-only action placeholders, evidence requirements, human-review guardrails, display boundaries, readiness templates, and safety policy only; it does not generate recommendations, action states, confidence scores, DecisionObjects, UI, broker behavior, or execution APIs. DecisionObject Evidence Bundle Contracts allow contracts-only evidence items, provenance maps, validation checklists, human-review attachments, readiness templates, and safety policy only; they do not generate recommendations, action states, confidence scores, active DecisionObjects, UI, broker behavior, or execution APIs. Decision Safety and Human-Review Guardrails allow guardrails-only safety contracts, human-review gates, approval placeholders, override prohibition contracts, blocked output policies, and readiness templates only; they do not grant approvals, allow overrides, generate recommendations, action states, confidence scores, active DecisionObjects, UI, broker behavior, or execution APIs. Decision Desk API Contract Skeleton endpoints return unavailable/planning-only metadata only; they do not accept market data, generate recommendations, action states, confidence scores, active DecisionObjects, approvals, overrides, UI, broker behavior, or execution APIs. Decision Desk Readiness API Skeleton endpoints return unavailable/planning-only metadata only; they do not accept market data, generate readiness-to-trade, generate recommendations, action states, confidence scores, active DecisionObjects, approvals, overrides, UI, broker behavior, or execution APIs. Decision Desk Display Contract Skeleton endpoints return unavailable/planning-only display metadata only; they do not create active UI, recommendation cards, readiness-to-trade displays, recommendations, action states, confidence scores, active DecisionObjects, approvals, overrides, broker behavior, or execution APIs. Decision Evidence Validation v0 endpoints return validation-only metadata and built-in contract validation examples only; validation pass is not a recommendation, not approval, not readiness-to-trade, not DecisionObject readiness, and not execution readiness. Decision Human Review Workflow Skeleton endpoints return unavailable/workflow-placeholder metadata only; they do not create active workflows, assign tasks, authenticate reviewers, send notifications, grant approvals, allow overrides, generate recommendations, generate action states, compute confidence scores, generate active DecisionObjects, generate readiness-to-trade, or expose execution APIs. Synthetic fixtures and local file inputs are local-only test/dev data, not real market data and not trading or investment data.

Decision Boundary Hardening endpoints return boundary-hardening-only registry,
endpoint policy, module policy, and invariant metadata. They do not generate
recommendations, action states, confidence scores, active DecisionObjects,
approvals, overrides, active UI, active workflow, readiness-to-trade, broker
behavior, or execution APIs.

Decision API/Display Integration Readiness Audit artifacts confirm the
Decision API, readiness API, display contracts, evidence validation, human
review workflow, and boundary hardening layers are ready for Retail Dashboard
Planning and Guardrails only. They do not build Retail Dashboard UI,
recommendation cards, trading controls, broker linkage, readiness-to-trade, or
execution APIs.

Retail Dashboard Safety Boundary Audit artifacts confirm the Retail Dashboard
planning, API skeleton, and display skeleton remain contract/skeleton/audit
layers only. They do not create active UI, frontend components, desktop UI
components, active widgets, recommendation cards, action generation,
confidence scoring, active DecisionObject display or generation,
readiness-to-trade, broker controls, approvals, overrides, real market data
display, or execution APIs.

Retail Dashboard Milestone Audit artifacts confirm the Retail Dashboard
planning phase is ready for system boundary hardening only. They do not create
active UI, frontend components, desktop UI components, active widgets,
recommendation cards, action generation, confidence scoring, active
DecisionObject display or generation, readiness-to-trade, broker controls,
approvals, overrides, real market data display, or execution APIs.

Retail Dashboard API/Display Integration Readiness Audit artifacts confirm the
Retail Dashboard planning, API, display, safety, milestone, and boundary
layers are ready for Retail Trader Experience Planning and Guardrails only.
They do not create active UI, frontend components, desktop UI components,
active widgets, recommendation cards, action generation, confidence scoring,
active DecisionObject display or generation, readiness-to-trade, broker
controls, approvals, overrides, real market data display, API-to-display
recommendation paths, display-to-decision paths, boundary bypass paths, or
execution APIs.

Retail Trader Experience Planning and Guardrails artifacts are planning-only
contracts, placeholders, safety policies, readiness templates, and read-only
endpoint metadata. They do not create active UI, frontend components, desktop
components, recommendation cards, action generation, confidence scoring,
active DecisionObject display or generation, readiness-to-trade, suitability
profiling, broker controls, approvals, overrides, real market data display,
or execution APIs.

Retail Trader Experience API Contract Skeleton artifacts are read-only,
unavailable-by-default API contracts, request placeholders, response
placeholders, persona/journey/dashboard/decision/safety reference placeholders,
unavailable responses, metadata, and health surfaces. They do not create active
UI, frontend components, desktop components, recommendation cards, action
generation, confidence scoring, active DecisionObject display or generation,
readiness-to-trade, suitability profiling, broker controls, approvals,
overrides, real market data display, or execution APIs.

Retail Trader Experience Display Contract Skeleton artifacts are read-only,
unavailable-by-default display contracts, persona visual placeholders, journey
visual placeholders, visual sections, widgets, badges, unavailable display
responses, metadata, and health surfaces. They do not create active UI,
frontend components, desktop components, recommendation cards or widgets,
action generation, confidence scoring, active DecisionObject display or
generation, readiness-to-trade, suitability profiling, broker controls,
approvals, overrides, real market data display, or execution APIs.

Retail Trader Experience Safety Boundary Audit artifacts confirm the Retail
Trader Experience planning, API skeleton, and display skeleton remain
contract/skeleton/audit layers only. They do not create active UI, frontend
components, desktop components, recommendation cards or widgets, action
generation, confidence scoring, active DecisionObject display or generation,
readiness-to-trade, suitability profiling, broker controls, approvals,
overrides, real market data display, external calls, or execution APIs.

Retail Trader Experience Milestone Audit artifacts confirm the Retail Trader
Experience planning phase is ready for system boundary hardening only. They do
not create active UI, frontend components, desktop components, recommendation
cards or widgets, action generation, confidence scoring, active DecisionObject
display or generation, readiness-to-trade, suitability profiling, broker
controls, approvals, overrides, real market data display, external calls, or
execution APIs.

Retail Trader Experience System Boundary Hardening artifacts add a forbidden
behavior registry, endpoint policies, module policies, cross-module
invariants, and read-only boundary metadata endpoints only. They do not create
active UI, frontend components, desktop components, recommendation cards or
widgets, action generation, confidence scoring, active DecisionObject display
or generation, readiness-to-trade, suitability profiling, broker controls,
approvals, overrides, real market data display, external calls, or execution
APIs.

Retail Trader Experience API/Display Integration Readiness Audit artifacts
confirm the Retail Trader Experience planning, API, display, safety, milestone,
and boundary hardening layers are ready for Strategy Research Workspace
Planning and Guardrails only. They do not create active UI, frontend
components, desktop components, recommendation cards or widgets, action
generation, confidence scoring, active DecisionObject display or generation,
readiness-to-trade, suitability profiling, broker controls, approvals,
overrides, API-to-display recommendation paths, display-to-decision paths,
persona-to-suitability-profile paths, journey-to-trading-advice paths,
boundary bypass paths, real market data display, external calls, or execution
APIs.

Strategy Research Workspace API Contract Skeleton artifacts are read-only,
unavailable-by-default API contracts, request placeholders, response
placeholders, workspace/artifact/paper/hypothesis/dataset/experiment/safety
reference placeholders, unavailable responses, metadata, and health surfaces.
They do not create active UI, frontend components, desktop components, paper
ingestion, paper parsing, strategy generation, strategy code generation,
backtesting, optimization, recommendation generation, action generation,
confidence scoring, active DecisionObject generation or display,
readiness-to-trade, broker controls, approvals, overrides, real market data
display, broker behavior, or execution APIs.

Strategy Research Workspace Display Contract Skeleton artifacts are read-only,
unavailable-by-default display contracts, workspace visual placeholders,
artifact visual placeholders, paper visual placeholders, hypothesis visual
placeholders, dataset visual placeholders, experiment visual placeholders,
badge placeholders, unavailable display responses, display safety helpers,
metadata, and health surfaces. They do not create active UI, frontend
components, desktop components, paper ingestion, paper parsing, strategy
generation, strategy code generation, backtesting, optimization,
recommendation generation, action generation, confidence scoring, active
DecisionObject generation or display, readiness-to-trade, broker controls,
approvals, overrides, real market data display, broker behavior, or execution
APIs.

Strategy Research Workspace Safety Boundary Audit artifacts confirm the
Strategy Research Workspace planning, API skeleton, and display skeleton
remain contract/skeleton/audit layers only. They do not create active UI,
frontend components, desktop components, paper ingestion, paper parsing,
strategy generation, strategy code generation, backtesting, optimization,
recommendation generation, action generation, confidence scoring, active
DecisionObject generation or display, readiness-to-trade, broker controls,
approvals, overrides, real market data display, external calls, or execution
APIs.

Strategy Research Workspace Milestone Audit artifacts confirm the planning, API skeleton, display skeleton, and safety boundary audit are complete as a contract/skeleton/audit phase only. They do not create active UI, frontend components, desktop components, paper ingestion, paper parsing, strategy generation, strategy code generation, backtesting, optimization, recommendation generation, action generation, confidence scoring, active DecisionObject generation or display, readiness-to-trade, broker controls, approvals, overrides, real market data display, external calls, or execution APIs. Prompt 67 is ready for Strategy Research Workspace System Boundary Hardening only.

Strategy Research Workspace System Boundary Hardening artifacts add forbidden
behavior registry contracts, endpoint boundary policies, module boundary
policies, cross-module invariants, rejection helpers, boundary health
metadata, and read-only boundary endpoints only. They do not create active UI,
frontend components, desktop components, paper ingestion, paper parsing,
arXiv ingestion, LLM paper analysis, strategy generation, strategy code
generation, signal/factor/alpha generation, backtesting, optimization,
recommendation generation, action generation, confidence scoring, active
DecisionObject generation or display, readiness-to-trade, broker controls,
approvals, overrides, real market data display, external calls, or execution
APIs. Prompt 68 is ready for Strategy Research Workspace API/Display
Integration Readiness Audit only.

Strategy Research Workspace API/Display Integration Readiness Audit artifacts
confirm the Strategy Research Workspace planning, API, display, safety,
milestone, and boundary hardening layers are ready for Research Artifact
Registry Planning and Guardrails only. They do not create active UI, frontend
components, desktop components, Research Artifact Registry implementation,
active artifact ingestion/storage, paper ingestion, paper parsing, strategy
generation, backtesting, recommendations, action generation, confidence
scoring, DecisionObject generation, readiness-to-trade, broker controls,
approvals, overrides, API-to-display strategy paths, API-to-display backtest
paths, API-to-display recommendation paths, parsed-paper display paths,
research-to-execution paths, real market data display, external calls, or
execution APIs.
Integration Readiness Audit only.

Research Artifact Registry Planning and Guardrails artifacts add planning
contracts, artifact metadata placeholders, artifact reference placeholders,
artifact provenance placeholders, lifecycle placeholders, forbidden
interaction contracts, safety/readiness helpers, health metadata, and read-only
planning endpoints only. They do not create active artifact ingestion/storage,
persistent artifact storage, file upload/download, paper parsing, PDF parsing,
arXiv ingestion, LLM paper analysis, strategy generation, backtesting,
recommendations, confidence scoring, DecisionObjects, readiness-to-trade,
broker controls, approvals, overrides, or execution APIs. Prompt 70 is ready
for Research Artifact Registry API Contract Skeleton only.

Research Artifact Registry API Contract Skeleton artifacts add read-only API
contracts, request placeholders, response placeholders, metadata reference
placeholders, provenance reference placeholders, lifecycle reference
placeholders, unavailable responses, safety helpers, health metadata, and
read-only API contract endpoints only. They do not create active artifact
ingestion/storage, persistent artifact storage, file upload/download, paper
parsing, PDF parsing, arXiv ingestion, LLM paper analysis, strategy
generation, strategy code generation, backtesting, recommendations,
confidence scoring, DecisionObjects, readiness-to-trade, broker controls,
approvals, overrides, or execution APIs. Prompt 71 is ready for Research
Artifact Registry Display Contract Skeleton only.

Research Artifact Registry Display Contract Skeleton artifacts add backend-only
display contracts, display metadata placeholders, artifact card placeholders,
reference display placeholders, provenance display placeholders, lifecycle
badge placeholders, unavailable display responses, display safety helpers,
health metadata, and read-only display contract endpoints only. They do not
create active UI, frontend components, desktop components, file previews,
active artifact ingestion/storage, persistent storage, file upload/download,
paper parsing, strategy generation, backtesting, recommendations, confidence
scoring, DecisionObjects, readiness-to-trade, broker controls, approvals,
overrides, or execution APIs.

Research Artifact Registry Safety Boundary Audit artifacts confirm planning,
API, and display skeletons remain placeholder-only, read-only,
unavailable-by-default, and audit-bounded. They do not create active
ingestion/storage, upload/download, active UI, frontend/desktop
implementation, paper parsing, strategy generation, backtesting,
recommendations, broker controls, approvals/overrides, readiness-to-trade, or
execution APIs.

Research Artifact Registry Milestone Audit artifacts confirm the
planning/API/display/safety phase is complete as an audit-only phase. They do
not create implementation, active ingestion/storage, persistent storage,
database tables, migrations, object storage, upload/download, active UI,
paper parsing, strategy generation, backtesting, recommendations, broker
controls, approvals/overrides, readiness-to-trade, or execution APIs.

Research Artifact Registry System Boundary Hardening artifacts add forbidden
behavior registry contracts, endpoint boundary policies, module boundary
policies, cross-module invariants, rejection helpers, boundary health
metadata, and read-only boundary endpoints only. They do not create
implementation, active ingestion/storage, upload/download, file previews,
active UI, frontend/desktop implementation, paper parsing, strategy
generation, backtesting, recommendations, broker controls, approvals/
overrides, readiness-to-trade, or execution APIs.

Research Artifact Registry API/Display Integration Readiness Audit artifacts
confirm planning, API, display, safety, milestone, and boundary layers are
ready for Research Artifact Index Planning and Guardrails only. They do not
create Research Artifact Registry implementation, Research Artifact Index
implementation, indexing, search, ranking, embeddings/vector stores,
retrieval, active ingestion/storage, upload/download, file previews, active
UI, frontend/desktop implementation, paper parsing, strategy generation,
backtesting, recommendations, confidence scoring, DecisionObjects,
readiness-to-trade, broker controls, approvals/overrides, or execution APIs.

Research Artifact Index Planning and Guardrails artifacts add planning-only
metadata, key, reference, tag, provenance, lifecycle, forbidden interaction,
safety, readiness, and health contracts plus read-only planning endpoints
only. They do not create Research Artifact Index implementation, indexing,
search, ranking, retrieval, embeddings/vector stores, ingestion/storage,
upload/download, file previews, paper parsing, strategy generation,
backtesting, recommendations, broker controls, readiness-to-trade, or
execution APIs.

Research Artifact Index API Contract Skeleton artifacts add read-only API
contracts, request placeholders, response placeholders, reference
placeholders, unavailable responses, safety helpers, health metadata, and
read-only API contract endpoints only. They do not create Research Artifact
Index implementation, indexing, search, ranking, retrieval,
embeddings/vector stores, active ingestion/storage, persistent storage,
upload/download, file previews, paper parsing, strategy generation,
backtesting, recommendations, confidence scoring, DecisionObjects,
readiness-to-trade, broker controls, approvals/overrides, or execution APIs.
