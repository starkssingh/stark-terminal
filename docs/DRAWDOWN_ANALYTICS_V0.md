# Drawdown Analytics v0

Prompt 29 implements Drawdown Analytics v0 as descriptive-only research analytics for validated synthetic/local price or equity value vectors.

## Purpose

Drawdown Analytics v0 describes peak-to-current declines in a value vector. It does not ingest real market data, call providers, scrape, use credentials, publish events, generate DecisionObject records, produce recommendations, or expose execution APIs.

## Conventions

- Drawdown formula: `current_value / running_peak - 1`.
- Running peak convention: the running peak updates only when a new high value appears.
- Drawdown series: values are zero or negative.
- Max drawdown convention: the minimum value in the drawdown series.
- Drawdown duration convention: the longest consecutive run of drawdown values below zero.
- Positive value requirement: values must be finite and positive by default.

## Boundaries

- Inputs must include a source reference.
- Inputs must remain synthetic/local/test posture and cannot claim real market data.
- Outputs preserve source provenance.
- Outputs are descriptive-only and research-only.
- There are no thresholds, regime labels, trading signals, recommendations, DecisionObject generation, broker behavior, or execution APIs.

## Future Relationship

Future risk diagnostics may add more audited descriptive metrics. Prompt 29 does not implement correlation, beta, backtesting, regimes, indicators, or features.

## Platform Notes

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The target desktop product remains Windows-native Stark Terminal, and the implementation avoids OS-specific paths or assumptions.
