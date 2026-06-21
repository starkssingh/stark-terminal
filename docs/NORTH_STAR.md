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

Prompt 16 adds Market Data Batch Persistence Contracts to the enriched schema plus instrument metadata persistence, operational time-series, research lake, cache, stream, event backbone, data quality, synthetic fixture, worker, instrument master, provider-contract, analytical warehouse, and feature registry foundations only. It does not implement a live decision engine.

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
- Current Prompt: 16
- Completed Prompts: 16 before this prompt, 17 after completion
- Current Milestone: Post-audit Data Foundation Phase - Market Data Batch Persistence Contracts

## Current Capability Status

- Backend Status: Foundation health surface + market data batch metadata health endpoint
- Desktop Status: Skeleton only
- Data Platform Status: Foundations through Instrument Metadata Persistence plus Market Data Batch Persistence Contracts implemented
- Infrastructure Status: PostgreSQL/Alembic foundation implemented and now wired for instrument metadata and batch metadata; TimescaleDB schema foundation, DuckDB/Parquet, Redis cache, Redis Streams, Worker System, Instrument/Provider Contracts, ClickHouse Warehouse, Feature Registry, Kafka/Redpanda Event Backbone, Data Quality, and Synthetic Fixtures implemented
- Data Layer Status: Instrument metadata + batch metadata persistence wiring + contracts/foundations + validation + synthetic fixtures only, no real market ingestion
- Quant Engine Status: Documentation + package placeholder only
- Regime Engine Status: Not started
- Decision Engine Status: Enriched schema + persistence record placeholder only
- Retail Console Status: Not started
- Backtest Engine Status: Not started
- Options Layer Status: Not started
- Risk Engine Status: Not started
- ML Engine Status: Not started
- Feature Engine Status: Registry/contracts only, no feature computation
- Event Backbone Status: Kafka/Redpanda contracts/foundation only, no production pipelines
- Data Quality Status: Validation framework/contracts only, no production ingestion pipeline
- Fixture Status: Synthetic local-only test/dev fixtures implemented; no real market data
- Instrument Persistence Status: Instrument metadata repository/service wiring implemented; no OHLCV persistence
- Market Data Batch Persistence Status: Batch metadata repository/service wiring implemented; no full OHLCV bars persisted
- Paper Lab Status: Not started
- Deployment Status: Not started
- Execution APIs: Forbidden
- Development Environment: Mac mini M2 / macOS / Apple Silicon
- Target Desktop Product: Windows-native Stark Terminal
- Known Blockers: Ambient `python` command missing; use `.venv/bin/python`
- Audit Verdict: Foundation ready for Prompt 17 after Prompt 16 verification passed

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

Prompt 16 implements Market Data Batch Persistence Contracts. Prompt 17 should perform a Data Foundation Audit and Readiness Check. Real market ingestion, full OHLCV production persistence, TimescaleDB data writes, ClickHouse data writes, production validation pipelines, production event pipelines, production dashboards, Feast integration, feature computation, analytics engines, analytics signals, UI surfaces, execution APIs, and deployment hardening remain deferred to later prompts.

## Prompt Log Rule

Every completed prompt must update `docs/PROMPT_LOG.md`. Product status or structure changes must also update `docs/NORTH_STAR.md` and `PROJECT_MAP.md`.
