# Time-Series Diagnostics Foundation

This package contains Prompt 32 descriptive/data-quality-only diagnostics for timestamp series.

Implemented now:

- timestamp series contracts with source references.
- timezone-aware timestamp validation.
- monotonicity diagnostics.
- duplicate timestamp diagnostics.
- fixed-interval gap diagnostics.
- irregular interval and spacing summaries.
- health metadata.

Not implemented now:

- stationarity statistical tests.
- ADF or KPSS tests.
- Hurst exponent or autocorrelation analytics.
- regime detection.
- indicators.
- feature computation.
- signals or recommendations.
- DecisionObject generation.
- execution APIs.

Diagnostics preserve source provenance and are research/data-quality-only. They are not trading interpretations.
