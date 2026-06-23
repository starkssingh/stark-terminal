# Beta Analytics

Prompt 31 implements descriptive beta analytics only.

The convention is:

`beta = covariance(asset_returns, benchmark_returns) / variance(benchmark_returns)`

Both covariance and benchmark variance use the sample n-1 denominator. Paired
return vectors must be finite, equal length, source referenced, and must contain
at least two observations. Beta is undefined when benchmark variance is zero.

Beta results are descriptive/research-only. They are not thresholds, regime
labels, signals, recommendations, DecisionObject evidence, or execution
instructions.

