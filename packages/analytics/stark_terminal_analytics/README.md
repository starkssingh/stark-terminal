# Stark Terminal Analytics

This package contains the Prompt 26 Quant/Time-Series Analytics Foundation Plan,
the Prompt 27 Numerical Analytics Core Contracts, the Prompt 28 descriptive
Returns and Rolling Window Analytics v0 modules, the Prompt 29 descriptive
Volatility and Drawdown Analytics v0 modules, the Prompt 31 descriptive
Correlation and Beta Analytics v0 modules, the Prompt 32 descriptive
Time-Series Diagnostics Foundation, the Prompt 33 Regime Analytics Planning
and Guardrails package, and the Prompt 34 Regime Feature Preparation Contracts
package.

Implemented now:

- analytics planning contracts.
- descriptive/research-only output contracts.
- analytics safety policy.
- dependency staging metadata.
- analytics roadmap metadata.
- health status helpers.
- numerical source/vector/table contracts.
- numerical validation and dependency gates.
- tiny stdlib descriptive summaries: count, min, max, and mean.
- simple and log returns over validated synthetic/local price vectors.
- right-aligned rolling count, mean, min, and max over validated vectors.
- sample and population standard deviation over validated return vectors.
- optional annualized volatility when explicit periods_per_year is supplied.
- drawdown series, max drawdown, and longest drawdown duration over validated value vectors.
- Pearson correlation over validated paired vectors.
- sample-covariance beta over validated paired return vectors.
- time-series monotonicity, duplicate timestamp, gap, irregular interval, and spacing diagnostics.
- regime label placeholder contracts.
- regime evidence requirements.
- regime safety policy, dependency staging, readiness template, and roadmap metadata.
- regime feature candidate contracts, group plans, provenance requirements,
  evidence mappings, readiness reports, safety policy, and dependency staging.

Not implemented now:

- indicators.
- feature computation.
- feature registry writes.
- regime classification.
- stationarity statistical tests.
- regime detection.
- trading signals.
- recommendations.
- decision generation.
- backtests.
- execution APIs.

Returns, rolling, volatility, drawdown, correlation, beta, and time-series
diagnostic outputs are descriptive/research/data-quality-only. Regime outputs
are planning-only. Regime feature outputs are contracts/preparation-only. They
are not computed feature values, registry writes, signals, recommendations,
decisions, backtests, classified regimes, or execution instructions. Future
analytics modules must require validated inputs, source references, focused
tests, documentation, and safety audits before additional scoped calculations
or feature computation are introduced.
