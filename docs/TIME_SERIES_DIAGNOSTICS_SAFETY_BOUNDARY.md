# Time-Series Diagnostics Safety Boundary

Prompt 32 keeps diagnostics descriptive/data-quality-only.

## Safety Rules

- Gaps are not signals.
- Irregular intervals are not recommendations.
- Data-quality diagnostics are not trade calls.
- No thresholds imply trading action.
- No buy/sell/hold/watch/avoid output is implemented.
- No confidence or action-state trading logic is implemented.
- No DecisionObject generation is implemented.
- No execution APIs are implemented.
- No broker integration is implemented.
- No event publishing to decision or execution systems is implemented.
- No trading interpretation is implemented.

## API Boundary

The `/time-series-diagnostics/health` and `/time-series-diagnostics/contracts`
endpoints expose metadata only. They do not accept user-supplied timestamps and
do not compute diagnostics for API callers.

## Forbidden Scope

Prompt 32 does not implement stationarity tests, ADF, KPSS, Hurst,
autocorrelation analytics, regime detection, indicators, feature computation,
factors, backtesting, signals, recommendations, decisions, real ingestion,
external calls, scraping, credentials, provider SDKs, or execution APIs.

Explicit audit phrases:

- no stationarity tests.
- no regime detection.
- no signals.
- no recommendations.
- no DecisionObject generation.
- no execution APIs.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The target
desktop product remains Windows-native Stark Terminal.

