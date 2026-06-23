# Beta Analytics v0

Prompt 31 implements Beta Analytics v0 as descriptive-only research analytics for validated synthetic/local paired return vectors.

## Purpose

Beta Analytics v0 describes a paired return relationship between an asset vector and a benchmark vector. It uses Prompt 27 numerical source/vector contracts and preserves both input source references in the result.

Beta output is descriptive-only. It is not a signal, not a recommendation, not DecisionObject evidence, and not an execution instruction.

## Convention

Prompt 31 supports sample-covariance beta only.

Formula:

`beta = covariance(asset_returns, benchmark_returns) / variance(benchmark_returns)`

Conventions:

- paired return vectors must have equal length.
- paired return vectors must satisfy the configured minimum observations requirement, currently at least two observations.
- vector values must be finite.
- each vector must carry a source reference.
- real market data claims are rejected under current settings.
- sample covariance uses the n-1 denominator.
- sample variance uses the n-1 denominator.
- beta is undefined when benchmark variance is zero.

## Boundaries

Beta Analytics v0 implements no thresholds, regime labels, indicators, factors, feature computation, backtests, signals, recommendations, DecisionObject generation, broker behavior, or execution APIs.

Prompt 31 safety language is explicit: no signals, no recommendations, no DecisionObject generation, and no execution APIs.

The `/relationship-analytics/health` and `/relationship-analytics/contracts` endpoints expose metadata only. They do not accept user-supplied vectors and do not compute analytics for API callers.

## Future Relationship

Future risk diagnostics may reference audited beta metrics as descriptive research artifacts only. Any DecisionObject linkage, feature usage, strategy usage, recommendation output, or execution boundary requires a separate future audit.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The target desktop product remains Windows-native Stark Terminal.
