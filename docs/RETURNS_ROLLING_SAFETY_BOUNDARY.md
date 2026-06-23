# Returns and Rolling Safety Boundary

Prompt 28 keeps Returns Analytics and Rolling Window Analytics descriptive/research-only.

## Core Safety Rules

- Returns are not signals.
- Rolling averages are not trend calls.
- Rolling metrics are not recommendations.
- No thresholds.
- No buy/sell/hold/watch/avoid action states.
- No signals.
- No recommendations.
- No DecisionObject generation.
- Prompt 28 allows no DecisionObject generation.
- No execution APIs.
- No broker integration.
- No real market data assumptions.

## Output Labels

Returns and rolling outputs must keep:

- `descriptive_only=true`.
- `trade_signal=false`.
- `recommendation=false`.
- `decision_object_generated=false`.
- safety labels such as `DESCRIPTIVE_ONLY`, `RESEARCH_ONLY`, or `NOT_A_SIGNAL`.

## API Boundary

The `/returns-analytics` endpoints expose health and contracts metadata only. Prompt 28 adds no POST endpoint and no endpoint that accepts arbitrary prices or vectors for computation.

## Future Decision Desk Boundary

Future DecisionObject or Decision Desk use must be audited separately. Prompt 28 does not generate decision evidence, confidence fields, action states, recommendations, or execution wiring.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
