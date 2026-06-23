# Decision Desk Evidence Requirements

Prompt 36 defines required evidence categories before any future Retail Decision
Desk output can be considered. The evidence model is planning-only and does not
generate recommendations, action states, confidence scores, DecisionObjects, or
execution behavior.

## Required Evidence Categories

- instrument context.
- data quality.
- returns.
- volatility.
- drawdown.
- correlation/beta.
- time-series diagnostics.
- regime context.
- feature context.
- risk context.
- human review.

Every future evidence item must carry source references and validated input
status. Current synthetic/local data remains test/dev data only and is not
trusted real market data, trading data, investment advice, or decision evidence.

## Failure Behavior

Missing evidence creates readiness blockers. Evidence readiness is not trade
readiness, not recommendation approval, and not a DecisionObject generation
gate. Human review remains required and cannot be bypassed in Prompt 36.

## Prompt 38 Evidence Bundle Contract Note

Prompt 38 adds DecisionObject evidence bundle contracts for these evidence
categories. The bundle contracts are contracts-only and do not permit active
DecisionObject generation, recommendations, action generation, confidence
scoring, execution APIs, real-data assumptions, or hidden decision logic.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The target
desktop product remains Windows-native Stark Terminal.
