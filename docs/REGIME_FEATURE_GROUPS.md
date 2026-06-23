# Regime Feature Groups

Prompt 34 defines Regime Feature Preparation feature groups as planned
metadata only. No computed values exist in Prompt 34.

## Planned Feature Groups

- Returns group: planned candidates such as `returns_momentum_summary`.
- Volatility group: planned candidates such as `volatility_level_summary`.
- Drawdown group: planned candidates such as `drawdown_pressure_summary`.
- Relationship group: planned candidates for correlation and beta context.
- Time-Series Diagnostics group: planned candidates for timestamp gap and
  interval quality context.
- Volume/liquidity placeholder: future evidence category only.
- Options context placeholder: future evidence category only.
- Macro context placeholder: future evidence category only.
- Market microstructure placeholder: future evidence category only.

## Boundary

Feature groups are contracts-only. They are not Feature Registry writes, feature
values, classifier inputs, market state decisions, signals, recommendations,
DecisionObject evidence, or execution instructions.

Prompt 34 has no feature computation, no classification, no signals, no
recommendations, no DecisionObject generation, and no execution APIs.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.
