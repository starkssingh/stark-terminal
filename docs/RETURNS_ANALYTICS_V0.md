# Returns Analytics v0

Prompt 28 implements Returns Analytics v0 for Stark Terminal.

## Purpose

Returns Analytics v0 is the first scoped descriptive time-series analytics module. It uses Prompt 27 Numerical Analytics source and vector contracts, requires validated synthetic/local inputs, and preserves source references in outputs.

These outputs are descriptive-only research artifacts. They are not trade calls, not signals, not recommendations, not DecisionObject evidence, and not execution instructions.

## Supported Calculations

Simple returns:

`simple_return[t] = price[t] / price[t - 1] - 1`

Prompt 28 implements simple returns as descriptive-only research values.

Log returns:

`log_return[t] = log(price[t] / price[t - 1])`

Prompt 28 implements log returns as descriptive-only research values. Log returns require positive prices. Prompt 28 performs no annualization.

## Input Requirements

- Price vectors must contain at least two values.
- Price values must be finite.
- Positive prices are required by default and always required for log returns.
- Source references are required.
- Real market data claims are rejected under current settings.
- Synthetic/local/test sources are allowed for deterministic tests.

## Explicit Non-Scope

- no volatility calculations.
- no drawdown calculations.
- no correlation or beta calculations.
- no indicators.
- no feature computation.
- no backtests.
- no regimes.
- no signals.
- no recommendations.
- no DecisionObject generation.
- no execution APIs.

## Future Relationship

Prompt 29 may add descriptive volatility and drawdown analytics using validated return or price vectors. Prompt 28 does not compute those risk metrics.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
