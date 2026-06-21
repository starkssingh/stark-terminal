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

Prompt 13 adds the Data Quality + Validation Framework to the enriched schema plus persistence, operational time-series, research lake, cache, stream, event backbone, worker, instrument master, provider-contract, analytical warehouse, and feature registry foundations only. It does not implement a live decision engine.

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
- Current Prompt: 13
- Completed Prompts: 13 before this prompt, 14 after completion
- Current Milestone: Post-audit Data Foundation Phase - Data Quality + Validation Framework

## Current Capability Status

- Backend Status: Foundation health surface + data quality health endpoint
- Desktop Status: Skeleton only
- Data Platform Status: Foundations through Event Backbone plus Data Quality Framework implemented
- Infrastructure Status: PostgreSQL, TimescaleDB schema foundation, DuckDB/Parquet, Redis cache, Redis Streams, Worker System, Instrument/Provider Contracts, ClickHouse Warehouse, Feature Registry, Kafka/Redpanda Event Backbone, and Data Quality foundations implemented
- Data Layer Status: Contracts/foundations + validation framework only, no real market ingestion
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
- Paper Lab Status: Not started
- Deployment Status: Not started
- Execution APIs: Forbidden
- Development Environment: Mac mini M2 / macOS / Apple Silicon
- Target Desktop Product: Windows-native Stark Terminal
- Known Blockers: Ambient `python` command missing; use `.venv/bin/python`
- Audit Verdict: Milestone A/B completed; data quality foundation added under Prompt 13 if tests pass

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

Prompt 13 implements the Data Quality + Validation Framework. Prompt 14 should implement Sample Market Data Fixtures + Synthetic OHLCV Contracts. Real market ingestion, production validation pipelines, production event pipelines, production dashboards, Feast integration, feature computation, analytics engines, analytics signals, UI surfaces, execution APIs, and deployment hardening remain deferred to later prompts.

## Prompt Log Rule

Every completed prompt must update `docs/PROMPT_LOG.md`. Product status or structure changes must also update `docs/NORTH_STAR.md` and `PROJECT_MAP.md`.
