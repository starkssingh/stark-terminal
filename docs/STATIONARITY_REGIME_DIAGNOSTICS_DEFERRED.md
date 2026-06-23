# Stationarity and Regime Diagnostics Deferred

Prompt 32 explicitly defers stationarity and regime analytics. Prompt 33 adds
Regime Analytics planning and guardrails, but stationarity tests and actual
regime classification remain deferred.

## Deferred Diagnostics

- ADF tests are not implemented.
- KPSS tests are not implemented.
- Hurst exponent calculations are not implemented.
- autocorrelation analytics are not implemented.
- regime detection is not implemented.
- regime label placeholders are planning-only and are not assigned.

## Dependency Boundary

ADF and KPSS commonly require future statistical dependencies such as
statsmodels or SciPy. Prompt 32 adds no heavy analytics dependencies and keeps
the current stdlib-only calculation posture.

## Future Guardrails

Before any stationarity test or actual regime classification is added, a future
prompt must define:

- dependency review and installation policy.
- validated input requirements.
- evidence requirements.
- descriptive-only result labels.
- no-signal and no-recommendation safety checks.
- audit coverage proving no hidden decision logic.

Prompt 33 regime planning must not become market state decisions, trading
signals, recommendations, DecisionObjects, broker actions, or execution APIs.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The target
desktop product remains Windows-native Stark Terminal.
