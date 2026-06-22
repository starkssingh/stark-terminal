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

Prompt 25 completes the Provider Adapter Milestone Audit. It audits Provider Adapter Guardrails, Real Provider Readiness and Candidate Selection, Local Sample Provider Adapter v0, and Local File Provider Adapter v0. It confirms no live provider clients, external provider calls, scraping, credentials, provider SDKs, real market ingestion, production approval, arbitrary file read API behavior, analytics signals, decisions, or execution APIs are implemented.

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
- Current Prompt: 25
- Completed Prompts: 25 before this prompt, 26 after completion
- Current Milestone: Provider Adapter Milestone Audit completed

## Current Capability Status

- Backend Status: Foundation health surface + provider endpoints audited
- Desktop Status: Skeleton only
- Data Platform Status: Synthetic/local data foundation complete; Local Sample Provider and Local File Provider implemented and audited; real provider implementation not started
- Infrastructure Status: Existing foundations intact; provider adapter milestone audited before analytics planning
- Data Layer Status: Validated synthetic/local fixtures + metadata persistence + synthetic/local provider responses/storage/export only; no real market ingestion
- Provider Status: Guardrails, readiness/candidate selection, local sample provider, and local file provider implemented and audited; no real provider implementation; no external calls
- Quant Engine Status: Documentation + package placeholder only; ready for analytics foundation planning
- Regime Engine Status: Not started
- Decision Engine Status: Enriched schema + persistence record placeholder only
- Retail Console Status: Not started
- Backtest Engine Status: Not started
- Options Layer Status: Not started
- Risk Engine Status: Not started
- ML Engine Status: Not started
- Feature Engine Status: Registry/contracts only, no feature computation
- Event Backbone Status: Kafka/Redpanda contracts/foundation only, no production pipelines
- Data Quality Status: Validation framework active for synthetic/local provider boundaries
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
- Known Blockers: Ambient `python` command missing; use `.venv/bin/python`
- Audit Verdict: Provider foundation ready for next analytics-planning phase if tests pass

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

Prompt 25 audits provider guardrails, provider readiness, Local Sample Provider, Local File Provider, no external calls, no scraping, no credentials, no SDKs, no real ingestion, no production approval, no arbitrary file read API, and no execution APIs. Prompt 26 should plan the quant/time-series analytics foundation without computing indicators, features, signals, decisions, recommendations, or backtests. Real market ingestion, provider-specific live clients, provider SDKs, credentials, scraping, ClickHouse writes, production validation pipelines, production event pipelines, production dashboards, Feast integration, feature computation, analytics engines, analytics signals, UI surfaces, execution APIs, and deployment hardening remain deferred to later prompts.

## Prompt Log Rule

Every completed prompt must update `docs/PROMPT_LOG.md`. Product status or structure changes must also update `docs/NORTH_STAR.md` and `PROJECT_MAP.md`.
