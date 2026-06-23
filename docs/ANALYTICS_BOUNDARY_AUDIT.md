# Analytics Boundary Audit

Prompt 30 documents the analytics milestone boundary after Prompts 26-29.
Prompt 32 extends the current boundary with descriptive time-series diagnostics only.

## What Analytics Code Can Do Today

Current analytics code can:

- define descriptive numerical source, vector, table, request, and result contracts.
- validate finite values, shapes, source references, and no-signal fields.
- calculate tiny standard-library summaries: count, min, max, and mean.
- calculate simple returns and log returns from validated synthetic/local price vectors.
- calculate rolling count, rolling mean, rolling min, and rolling max with right-aligned windows.
- calculate sample standard deviation and population standard deviation from validated return vectors.
- calculate annualized volatility when explicitly parameterized with positive periods_per_year.
- calculate drawdown series using `current_value / running_peak - 1`.
- calculate max drawdown and drawdown duration.
- calculate Pearson correlation using sample covariance and sample variance conventions.
- calculate beta = covariance(asset returns, benchmark returns) / variance(benchmark returns).
- preserve source/provenance references.
- return descriptive-only research results.

## What Analytics Code Cannot Do Today

Current analytics code cannot:

- produce signals.
- produce recommendations.
- generate DecisionObjects.
- execute trades.
- call brokers.
- publish decision or execution events.
- run backtests.
- run regimes.
- compute indicators.
- compute factors or features.
- run ML models.
- assume real market data.
- call external services.
- ingest real market data.

## Boundary Before Future Analytics Modules

Future analytics modules must remain descriptive/research-only until separately audited. Every future module must require validated inputs, source references, deterministic behavior, docs, tests, dependency review, API surface review, and no-signal/no-decision checks.

Stationarity tests, regimes, features, backtests, model outputs, recommendations, and DecisionObject linkage each require future explicit prompts and separate audits. Prompt 32 implements time-series diagnostics only as descriptive/data-quality metrics with no thresholds that imply trade calls, no regime labels, no signals, no recommendations, no DecisionObject generation, and no execution APIs.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The target desktop product remains Windows-native Stark Terminal.
