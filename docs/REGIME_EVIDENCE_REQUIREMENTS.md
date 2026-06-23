# Regime Evidence Requirements

Prompt 33 defines Regime Analytics evidence requirements before any future
classifier, market-state output, or feature preparation work.

## Required Evidence Categories

Future regime work must require validated and source-referenced evidence from:

- returns.
- volatility.
- drawdown.
- correlation.
- beta.
- time-series diagnostics.
- volume.
- liquidity.
- options context.
- macro context.

Some categories are implemented today only as descriptive analytics, while
others remain future evidence categories. Prompt 33 does not compute volume,
liquidity, options context, macro context, features, indicators, or regime
classification.

## Source And Validation Requirements

Every future evidence item must carry a source reference, use validated input,
and remain synthetic/local/test-compatible until real provider work is
separately approved. There is no real-data assumption in Prompt 33.

Missing required evidence blocks readiness. A readiness template may list
blockers, but it cannot classify a regime or generate a recommendation.

Prompt 34 adds regime feature preparation contracts that map these evidence
requirements to future feature candidates. The mapping is metadata only: it
does not compute features, does not create classifier inputs, does not assign
regime labels, and does not generate signals, recommendations, DecisionObjects,
or execution instructions.

## Safety

Evidence requirements are governance constraints, not hidden decision logic.
They do not generate signals, recommendations, DecisionObjects, or execution
APIs.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.
