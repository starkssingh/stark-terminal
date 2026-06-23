# Time-Series Diagnostics Foundation

Prompt 32 implements the Time-Series Diagnostics Foundation for Stark Terminal.
The scope is descriptive, data-quality, and research-only timestamp inspection
using stdlib-only logic and existing numerical source-reference contracts.

## Purpose

Time-Series Diagnostics inspects timestamp quality before future analytics use a
series. It does not ingest real market data, call external services, scrape,
read arbitrary files, publish events, generate recommendations, generate
DecisionObject instances, or expose execution APIs.

## Supported Diagnostics

- monotonicity diagnostics for timestamp order as provided.
- duplicate timestamp diagnostics with unique duplicate timestamps reported once.
- missing timestamp and gap diagnostics for a positive expected interval.
- irregular interval diagnostics based on observed timestamp spacing.
- spacing summary with interval count, minimum interval, maximum interval, and mean interval.

## Data Boundary

Inputs require a `NumericalSourceReference` source reference. Current settings allow
synthetic/local/test sources only. `real_market_data=true` is rejected. Timestamp
inputs must be timezone-aware by default and are normalized to UTC where
practical.

## Deferred Scope

No stationarity tests are implemented in Prompt 32. No ADF, KPSS, Hurst,
autocorrelation analytics, or regime detection are implemented. Explicit audit
phrases: no stationarity tests; no regime detection. These require future
dependency and safety review.

## Safety Boundary

Time-Series Diagnostics outputs are descriptive-only and data-quality-only. Gaps,
duplicates, and irregular intervals are not signals, not recommendations, not
DecisionObjects, not trade calls, and not execution instructions. Explicit
audit phrases: no signals, no recommendations, no execution APIs.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The target
desktop product remains Windows-native Stark Terminal.
