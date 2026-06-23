# Analytics Safety Policy

Prompt 26 adds the analytics safety policy for the Quant/Time-Series Analytics Foundation Plan.

## Core Rules

- No analytics-as-trade-call.
- No indicators-as-signals.
- No buy, sell, hold, watch, avoid, reduce, or action-state recommendations.
- No execution APIs.
- No broker integration.
- No hidden decision logic.
- No unvalidated model outputs.
- No real-data assumptions.

## Output Labels

Future analytics outputs must be labelled descriptive/research-only. Output contracts must keep:

- `descriptive_only=true`.
- `trade_signal=false`.
- `recommendation=false`.
- `execution_ready=false`.

Prompt 26 enforces these flags through analytics output contracts and safety evaluation helpers.

## Quality Gates

Future analytics modules must require:

- validated input data.
- source references.
- deterministic behavior.
- focused tests.
- documentation.
- audit coverage.

Validation results, quality gates, and analytics results cannot authorize execution, order placement, real-money routing, or trading recommendations.

## Future DecisionObject Boundary

Any future DecisionObject linkage must be audited separately. Prompt 26 does not create DecisionObjects, decision evidence, recommendations, action states, or trading interpretation.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.

