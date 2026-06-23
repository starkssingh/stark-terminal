# Volatility and Drawdown Safety Boundary

Prompt 29 keeps risk metrics descriptive-only.

## Safety Rules

- Volatility is not a signal.
- Drawdown is not a signal.
- A risk metric is not a recommendation.
- No thresholds or regime labels are implemented.
- No buy/sell/hold/watch/avoid output is implemented.
- No DecisionObject generation is implemented.
- No execution APIs are implemented.
- No trading interpretation is implemented.
- No broker integration is implemented.
- No event publishing to decision or execution systems is implemented.

## API Boundary

The `/risk-analytics/health` and `/risk-analytics/contracts` endpoints expose metadata only. They do not accept user-supplied vectors and do not compute analytics for API callers.

## Forbidden Scope

Prompt 29 does not implement correlation, beta, indicators, features, backtesting, regimes, signals, recommendations, decisions, real ingestion, external calls, scraping, credentials, provider SDKs, or execution APIs.

Explicit audit phrases:

- no correlation.
- no backtesting.
- no regimes.
- no signals.
- no recommendations.
- no DecisionObject generation.
- no execution APIs.

## Platform Notes

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The target desktop product remains Windows-native Stark Terminal.
