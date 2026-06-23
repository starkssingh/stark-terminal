# Quant Analytics Foundation Plan

Prompt 26 implements the Quant Analytics and Time-Series Analytics foundation plan for Stark Terminal.

## Purpose

The analytics foundation defines module boundaries, contracts, safety gates, dependency staging, and roadmap metadata before any analytics calculation is introduced.

This stage is descriptive/research-only planning. It does not calculate returns, rolling windows, volatility, drawdown, indicators, features, regimes, model outputs, backtests, trading signals, recommendations, decisions, or execution instructions.

Prompt 26 policy phrase: no analytics calculations.

## Implemented Scope

- `packages/analytics/stark_terminal_analytics/foundation/contracts.py` defines planning-level input, output, and module contracts.
- `safety.py` defines the analytics safety policy and blocks signals, recommendations, execution-ready outputs, and real-data assumptions.
- `dependencies.py` documents staged numerical, statistical, ML, GPU, options, and backtesting dependencies without requiring heavy dependencies now.
- `roadmap.py` defines the next analytics prompt sequence.
- `health.py` exposes safe health metadata for the API.
- `/analytics-foundation/health`, `/analytics-foundation/contracts`, and `/analytics-foundation/dependencies` expose metadata only.

## Data Relationship

Future analytics must consume validated input data with source references. Synthetic/local data can be used for deterministic tests, but it remains local/test/dev data and must not be treated as real market data.

Prompt 26 relies on the Data Quality Framework boundary: future analytics modules must validate inputs before computation and preserve source references in outputs.

## Future Decision Desk Relationship

The future Decision Desk may use audited analytics as evidence after later prompts implement validated calculations. Prompt 26 does not create DecisionObject evidence, trade calls, Buy/Sell/Hold/Watch/Avoid outputs, recommendation labels, or execution wiring.

## Safety Boundary

Prompt 26 forbids:

- analytics-as-trade-call.
- indicators-as-signals.
- buy, sell, hold, watch, avoid, or reduce recommendations.
- hidden decision logic.
- execution APIs.
- broker integration.
- real market ingestion.
- external provider calls.
- scraping.
- heavy quant/ML dependency installation.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
