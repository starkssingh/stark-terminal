# Time-Series Analytics Boundary

Prompt 26 establishes the Time-Series Analytics boundary before implementation.

## Future Allowed Direction

Later prompts may implement descriptive research computations such as returns, rolling windows, volatility, drawdown, correlation, beta, diagnostics, and other audited time-series metrics.

Those future modules must:

- be deterministic.
- require validated inputs.
- require source references.
- preserve input metadata where practical.
- avoid mutating source datasets.
- include tests and documentation.
- label outputs as descriptive/research-only.

## Forbidden In Prompt 26

Prompt 26 does not implement:

- analytics calculations.
- returns.
- rolling windows.
- volatility.
- drawdown.
- indicators.
- feature computation.
- factors.
- regimes.
- models.
- backtests.
- trading signals.
- recommendations.
- decisions.
- execution APIs.

## Input Boundary

Future analytics inputs must pass Data Quality validation. Synthetic/local data is allowed for tests only and carries no live-data or real-market-data meaning.

Real market data is not available to analytics in Prompt 26. Any future real-data analytics path requires provider approval, data-policy review, source references, validation gates, and audit coverage.

## Interpretation Boundary

Time-Series Analytics outputs are descriptive/research artifacts. They must not be interpreted as trading advice, trade instructions, model authority, or hidden decision logic.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.

