# Correlation Analytics v0

Prompt 31 implements Correlation Analytics v0 as descriptive-only research analytics for validated synthetic/local paired vectors.

## Purpose

Correlation Analytics v0 describes the linear relationship between two numerical vectors. It uses Prompt 27 numerical source/vector contracts and preserves both input source references in the result.

Correlation output is descriptive-only. It is not a signal, not a recommendation, not DecisionObject evidence, and not an execution instruction.

## Convention

Prompt 31 supports Pearson correlation only.

Conventions:

- paired vectors must have equal length.
- paired vectors must satisfy the configured minimum observations requirement, currently at least two observations.
- vector values must be finite.
- each vector must carry a source reference.
- real market data claims are rejected under current settings.
- sample covariance uses the n-1 denominator.
- sample variance uses the n-1 denominator.
- Pearson correlation is `covariance(x, y) / sqrt(variance(x) * variance(y))`.
- correlation is undefined when either vector has zero variance.

## Boundaries

Correlation Analytics v0 implements no thresholds, regime labels, indicators, factors, feature computation, backtests, signals, recommendations, DecisionObject generation, broker behavior, or execution APIs.

Prompt 31 safety language is explicit: no signals, no recommendations, no DecisionObject generation, and no execution APIs.

The `/relationship-analytics/health` and `/relationship-analytics/contracts` endpoints expose metadata only. They do not accept user-supplied vectors and do not compute analytics for API callers.

## Future Relationship

Future diagnostics and regime analytics may reference audited correlation metrics as descriptive research artifacts only. Any DecisionObject linkage, feature usage, strategy usage, recommendation output, or execution boundary requires a separate future audit.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The target desktop product remains Windows-native Stark Terminal.
