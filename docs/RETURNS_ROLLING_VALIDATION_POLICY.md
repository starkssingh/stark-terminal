# Returns and Rolling Validation Policy

Prompt 28 adds deterministic validation for Returns Analytics and Rolling Window Analytics v0.

## Price Vector Validation

- Price vectors require at least two values for returns.
- Finite values are required.
- Positive prices are required by default.
- Positive prices are mandatory for log returns.
- Source references are required.
- Real market data is not allowed under current settings.

## Rolling Window Validation

- Rolling vectors require finite values.
- Window size must be positive.
- Window size must be less than or equal to vector length for successful calculation.
- Window size must be less than or equal to the configured max window when provided.
- Metric must be one of mean, min, max, or count.
- Right alignment is the only supported alignment in v0.

## Failure Behavior

Invalid requests return failed descriptive result contracts where practical. Validation failure does not silently pass, does not create successful metrics, does not create signals, does not create recommendations, and does not create execution approval.

## Side-Effect Boundary

Returns and rolling validation performs no external calls, no file IO, no persistence writes, no event publishing, no provider calls, no scraping, and no broker integration. Helpers are deterministic and do not mutate input contracts.

## No Trading Interpretation

Validation success means only that a local contract passed Prompt 28 checks. It does not approve real market data, authorize trading interpretation, generate DecisionObject evidence, or create an execution path.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
