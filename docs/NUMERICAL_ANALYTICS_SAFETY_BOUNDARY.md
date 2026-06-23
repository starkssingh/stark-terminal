# Numerical Analytics Safety Boundary

Prompt 27 keeps Numerical Analytics descriptive/research-only.

## Core Safety Rules

- Numerical metrics are not signals.
- No signals.
- Count, min, max, and mean are descriptive-only.
- No returns calculations.
- No rolling windows.
- No volatility calculations.
- No drawdown calculations.
- No correlation or beta calculations.
- No indicators.
- No recommendations.
- No DecisionObject generation.
- Prompt 27 allows no DecisionObject generation.
- No execution APIs.
- No broker integration.
- No real market data assumptions.

## Output Labels

Numerical outputs must keep:

- `descriptive_only=true`.
- `trade_signal=false`.
- `recommendation=false`.
- `decision_object_generated=false`.
- safety labels such as `DESCRIPTIVE_ONLY`, `RESEARCH_ONLY`, or `NOT_A_SIGNAL`.

## API Boundary

The `/numerical-analytics` endpoints expose health, contracts, and dependency gate metadata only. Prompt 27 adds no POST endpoint and no endpoint that accepts arbitrary vectors for computation.

## Future Decision Desk Boundary

Future DecisionObject or Decision Desk use must be audited separately. Prompt 27 does not generate decision evidence, confidence fields, action states, buy/sell/hold/watch/avoid labels, recommendations, or execution wiring.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
