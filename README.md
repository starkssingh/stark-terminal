# Stark Terminal

Windows-native Indian-market trading research and decision terminal powered by an institutional-grade Oracle Cloud quant backend.

## Product Philosophy

Evidence before decision. Safety before execution. Research before automation. Decision support before trading. Institution-grade infrastructure from day one.

## Current Status

Prompt 25 Provider Adapter Milestone Audit.

This repository currently contains the verified foundation only: project control documents, institutional architecture documentation, Prompt 11 audit artifacts, Prompt 17 data foundation audit artifacts, Prompt 22 data foundation milestone audit artifacts, Prompt 25 provider adapter milestone audit artifacts, provider readiness/candidate selection governance, package skeletons, typed configuration, core domain schemas, SQLAlchemy/Alembic metadata persistence foundation, Instrument Metadata Persistence Wiring, Market Data Batch Persistence Contracts, TimescaleDB-oriented operational time-series schema foundation, TimescaleDB Synthetic OHLCV Storage Foundation, Synthetic OHLCV Research Lake Export Contract, Provider Adapter Guardrails, Local Sample Provider Adapter v0, Local File Provider Adapter v0, DuckDB + Parquet research lake foundation, Redis cache foundation, Redis Streams event pipeline foundation, Kafka/Redpanda Event Backbone foundation, Data Quality + Validation Framework, Synthetic Market Data Fixtures, Worker System foundation, Instrument Master/Provider Contracts foundation, ClickHouse Warehouse foundation, Feature Registry foundation, FastAPI health/config/database-health/timeseries-health/research-lake-health/cache-health/streams-health/event-backbone-health/data-quality-health/fixtures-health/instrument-metadata-health/market-data-batches-health/synthetic-ohlcv-storage-health/synthetic-ohlcv-exports-health/provider-guardrails-health/provider-readiness-health/local-sample-provider-health/local-file-provider-health/workers-health/instrument-health/provider-health/warehouse-health/feature-registry-health surfaces, a minimal PySide6 desktop shell placeholder, an enriched DecisionObject schema placeholder, tests, an audit script, and a verification script.

## High-Level Architecture

Stark Terminal is designed as a cloud-brain plus Windows-native terminal:

- Windows-native desktop client built with PySide6 / Qt 6.
- FastAPI backend designed for Oracle Cloud Free Tier first and scalable cloud upgrades later.
- REST API first; WebSockets only when a later use case requires them.
- Core domain contracts shared by backend, analytics, and future worker pipelines.
- Institutional-grade data and analytics architecture locked in documentation before implementation.

Stark Terminal intentionally targets an institutional-grade stack, including PostgreSQL, TimescaleDB, DuckDB, Parquet, Redis, Redis Streams, Kafka or Redpanda-compatible event replay, data quality gates, synthetic local test fixtures, repository/service persistence layers, worker pipelines, Instrument Master/Provider Contracts, Provider Adapter Guardrails, provider readiness governance, Local Sample Provider Adapter v0, Local File Provider Adapter v0, ClickHouse Warehouse, a custom Stark Feature Registry, and future Feast evaluation. Current prompts implement only controlled foundations, data-foundation milestone audit coverage, provider adapter milestone audit coverage, synthetic-only OHLCV storage, synthetic-only research lake export contracts, provider guardrails, provider candidate selection/risk scoring, a synthetic/local-only provider adapter, and a local-file-only test/dev provider adapter; production Kafka/Redpanda pipelines, Feast integration, real production workers, real market data ingestion, external provider calls, live provider clients, provider SDKs, scraping, credentials, production approval, arbitrary file read APIs, production OHLCV ingestion, production dashboards, feature computation, validation pipelines, and analytics engines remain deferred.

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

Stark Terminal is decision support only. Current foundations include no live trading, no broker execution, no order placement, no real-money routing, no broker credential vaults, no autonomous trading, no real market data ingestion, no scraping, no external provider calls, no provider SDKs, no provider credentials, no production approval, no arbitrary file read API, no automatic ClickHouse table creation, no production OHLCV ingestion, no feature computation, and no analytics signals. Instrument metadata persistence and market data batch persistence are metadata-only and validation-gated. Synthetic OHLCV storage is synthetic-only and validation-gated. Provider guardrails and provider readiness scoring remain fail-closed governance. Local Sample Provider Adapter v0 uses synthetic/local/test data only. Local File Provider Adapter v0 uses explicit local test/dev files under path-safety checks only. Neither adapter approves any real provider. Synthetic fixtures and local file inputs are local-only test/dev data, not real market data and not trading or investment data.
