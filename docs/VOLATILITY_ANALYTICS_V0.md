# Volatility Analytics v0

Prompt 29 implements Volatility Analytics v0 as descriptive-only research analytics for validated synthetic/local return vectors.

## Purpose

Volatility Analytics v0 provides standard deviation metrics for return vectors that already carry Prompt 27 numerical source references. It does not ingest market data, call providers, scrape websites, read files, publish events, generate DecisionObject records, produce recommendations, or expose execution APIs.

## Supported Metrics

- Sample standard deviation: uses the n-1 denominator and requires at least two finite return values.
- Population standard deviation: uses the n denominator and is validated with at least two finite return values in Prompt 29 for consistency.
- Annualized volatility: `volatility * sqrt(periods_per_year)` and only when `periods_per_year` is explicitly supplied as a positive integer.

## Boundaries

- Inputs must include a source reference.
- Inputs must remain synthetic/local/test posture and cannot claim real market data.
- Outputs preserve source provenance.
- Outputs are descriptive-only and research-only.
- There are no thresholds, regime labels, trading signals, recommendations, DecisionObject generation, broker behavior, or execution APIs.

## Future Relationship

Future risk diagnostics may build on this contract after a separate audit. Prompt 29 does not implement correlation, beta, backtesting, regimes, indicators, or features.

## Platform Notes

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The target desktop product remains Windows-native Stark Terminal, and the implementation avoids OS-specific paths or assumptions.
