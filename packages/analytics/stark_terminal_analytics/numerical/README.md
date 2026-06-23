# Numerical Analytics Core Contracts

Prompt 27 adds numerical analytics core contracts for Stark Terminal.

This package contains:

- source reference contracts.
- vector and table contracts.
- computation request and result contracts.
- finite-value, shape, table, source, and no-signal validation helpers.
- a dependency gate for the current `contracts_and_safe_stdlib` stage.
- tiny descriptive stdlib summary helpers: count, min, max, and mean.

Prompt 27 does not implement returns, rolling windows, volatility, drawdown,
correlation, beta, indicators, features, factors, regimes, model outputs,
backtests, signals, recommendations, DecisionObject generation, broker
integration, or execution APIs.

Outputs are descriptive/research-only and must preserve source references.
Heavy numerical dependencies remain blocked until a future explicit prompt.
