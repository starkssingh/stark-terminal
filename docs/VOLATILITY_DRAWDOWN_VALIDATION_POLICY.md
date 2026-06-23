# Volatility and Drawdown Validation Policy

Prompt 29 validation protects Volatility Analytics and Drawdown Analytics from becoming unsafe or ambiguous analytics.

## Return Vector Validation

- Return vectors must contain finite values.
- Volatility requests require at least two return values.
- Source references are required.
- Sources cannot claim real market data under current settings.
- The request cannot allow trade signals, recommendations, DecisionObject generation, or execution.

## Price and Equity Vector Validation

- Drawdown value vectors must contain at least one finite value.
- Positive values are required by default.
- Source references are required.
- Sources cannot claim real market data under current settings.
- The request cannot allow trade signals, recommendations, DecisionObject generation, or execution.

## Annualization Parameter Validation

Annualized volatility is descriptive-only. It is allowed only when `annualize=true` and `periods_per_year` is supplied as a positive integer.

## Failure Behavior

Validation failures produce safe failed results with sanitized errors. Failures do not produce signals, recommendations, decisions, events, persistence writes, or execution instructions.

## Platform Notes

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The target desktop product remains Windows-native Stark Terminal.
