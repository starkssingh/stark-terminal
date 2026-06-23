# Returns Analytics

Prompt 28 implements descriptive returns analytics v0.

Allowed calculations are simple returns and log returns over validated synthetic/local price vectors with source references. Log returns require positive prices. Results are descriptive-only research artifacts and keep signal, recommendation, DecisionObject, and execution flags false.

This package does not implement volatility, drawdown, correlation, indicators, feature computation, backtests, regimes, recommendations, decisions, broker integration, or execution APIs.
