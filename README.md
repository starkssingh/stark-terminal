# Stark Terminal

Windows-native Indian-market trading research and decision terminal powered by an institutional-grade Oracle Cloud quant backend.

## Product Philosophy

Evidence before decision. Safety before execution. Research before automation. Decision support before trading. Institution-grade infrastructure from day one.

## Current Status

Prompt 53 Retail Dashboard Milestone Audit.

This repository currently contains the verified foundation only: project control documents, institutional architecture documentation, Prompt 11 audit artifacts, Prompt 17 data foundation audit artifacts, Prompt 22 data foundation milestone audit artifacts, Prompt 25 provider adapter milestone audit artifacts, Prompt 26 analytics foundation plan artifacts, Prompt 27 numerical analytics core contract artifacts, Prompt 28 returns/rolling analytics artifacts, Prompt 29 volatility/drawdown analytics artifacts, Prompt 30 analytics milestone audit artifacts, Prompt 31 correlation/beta analytics artifacts, Prompt 32 time-series diagnostics artifacts, Prompt 33 regime analytics planning/guardrail artifacts, Prompt 34 regime feature preparation contract artifacts, Prompt 35 analytics/regime milestone audit artifacts, Prompt 36 Retail Decision Desk planning/guardrail artifacts, Prompt 38 DecisionObject evidence bundle contract artifacts, Prompt 39 Decision Safety and Human-Review Guardrail artifacts, Prompt 40 Decision Desk API Contract Skeleton artifacts, Prompt 41 Decision Desk Milestone Audit artifacts, Prompt 42 Decision Desk Readiness API Skeleton artifacts, Prompt 43 Decision Desk Display Contract Skeleton artifacts, Prompt 44 Decision Desk Evidence Bundle Validation v0 artifacts, Prompt 45 Decision Desk Human Review Workflow Skeleton artifacts, Prompt 46 Decision Desk Milestone Audit 2 artifacts, Prompt 47 Decision Desk System Boundary Hardening artifacts, Prompt 48 Decision Desk API/Display Integration Readiness Audit artifacts, Prompt 49 Retail Dashboard Planning and Guardrails artifacts, Prompt 50 Retail Dashboard API Contract Skeleton artifacts, Prompt 51 Retail Dashboard Display Contract Skeleton artifacts, Prompt 52 Retail Dashboard Safety Boundary Audit artifacts, Prompt 53 Retail Dashboard Milestone Audit artifacts, provider readiness/candidate selection governance, package skeletons, typed configuration, core domain schemas, SQLAlchemy/Alembic metadata persistence foundation, Instrument Metadata Persistence Wiring, Market Data Batch Persistence Contracts, TimescaleDB-oriented operational time-series schema foundation, TimescaleDB Synthetic OHLCV Storage Foundation, Synthetic OHLCV Research Lake Export Contract, Provider Adapter Guardrails, Local Sample Provider Adapter v0, Local File Provider Adapter v0, DuckDB + Parquet research lake foundation, Redis cache foundation, Redis Streams event pipeline foundation, Kafka/Redpanda Event Backbone foundation, Data Quality + Validation Framework, Synthetic Market Data Fixtures, Worker System foundation, Instrument Master/Provider Contracts foundation, ClickHouse Warehouse foundation, Feature Registry foundation, FastAPI health/config/database-health/timeseries-health/research-lake-health/cache-health/streams-health/event-backbone-health/data-quality-health/fixtures-health/instrument-metadata-health/market-data-batches-health/synthetic-ohlcv-storage-health/synthetic-ohlcv-exports-health/provider-guardrails-health/provider-readiness-health/local-sample-provider-health/local-file-provider-health/analytics-foundation-health/numerical-analytics-health/returns-analytics-health/risk-analytics-health/relationship-analytics-health/time-series-diagnostics-health/regime-analytics-health/regime-features-health/decision-desk-health/decision-evidence-health/decision-safety-health/decision-desk-api-health/decision-readiness-api-health/decision-display-health/decision-evidence-validation-health/decision-human-review-health/decision-boundary-health/retail-dashboard-health/retail-dashboard-api-health/retail-dashboard-display-health/workers-health/instrument-health/provider-health/warehouse-health/feature-registry-health surfaces, a minimal PySide6 desktop shell placeholder, an enriched DecisionObject schema placeholder, tests, an audit script, and a verification script.

## High-Level Architecture

Stark Terminal is designed as a cloud-brain plus Windows-native terminal:

- Windows-native desktop client built with PySide6 / Qt 6.
- FastAPI backend designed for Oracle Cloud Free Tier first and scalable cloud upgrades later.
- REST API first; WebSockets only when a later use case requires them.
- Core domain contracts shared by backend, analytics, and future worker pipelines.
- Institutional-grade data and analytics architecture locked in documentation before implementation.

Stark Terminal intentionally targets an institutional-grade stack, including PostgreSQL, TimescaleDB, DuckDB, Parquet, Redis, Redis Streams, Kafka or Redpanda-compatible event replay, data quality gates, synthetic local test fixtures, repository/service persistence layers, worker pipelines, Instrument Master/Provider Contracts, Provider Adapter Guardrails, provider readiness governance, Local Sample Provider Adapter v0, Local File Provider Adapter v0, ClickHouse Warehouse, a custom Stark Feature Registry, and future Feast evaluation. Current prompts implement only controlled foundations, data-foundation milestone audit coverage, provider adapter milestone audit coverage, synthetic-only OHLCV storage, synthetic-only research lake export contracts, provider guardrails, provider candidate selection/risk scoring, a synthetic/local-only provider adapter, a local-file-only test/dev provider adapter, analytics foundation planning contracts, numerical analytics contracts with tiny descriptive count/min/max/mean helpers, descriptive simple/log returns plus rolling count/mean/min/max, descriptive volatility/drawdown metrics, descriptive correlation/beta metrics, descriptive time-series timestamp diagnostics, regime analytics planning/guardrails, regime feature preparation contracts, analytics/regime milestone audit coverage, Retail Decision Desk planning/guardrail contracts, DecisionObject evidence bundle contracts, Decision Safety human-review guardrails, Decision Desk API contract skeleton unavailable responses, Decision Desk milestone audit coverage, Decision Desk Readiness API skeleton unavailable responses, Decision Desk Display contract skeleton unavailable responses, Decision Evidence Validation v0 contract checks, Decision Human Review workflow skeleton placeholders, Decision Boundary hardening contracts, Decision API/display integration readiness audit artifacts, Retail Dashboard planning/guardrail placeholders, Retail Dashboard API contract skeleton placeholders, and Retail Dashboard Display contract skeleton placeholders; production Kafka/Redpanda pipelines, Feast integration, real production workers, real market data ingestion, external provider calls, live provider clients, provider SDKs, scraping, credentials, production approval, arbitrary file read APIs, production OHLCV ingestion, production dashboards, active Retail Dashboard UI, frontend components, desktop UI components, recommendation cards, broker controls, Retail Dashboard implementation, active Decision Desk implementation, active human review workflow, task assignment, reviewer auth, notifications, readiness-to-trade generation, active DecisionObject generation, approvals, overrides, recommendation generation, action generation, confidence scoring, feature computation, feature registry writes, classifier inputs, production validation pipelines, stationarity tests, actual regime classification, regime detection, backtests, computed regimes, and analytics signals remain deferred.

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
