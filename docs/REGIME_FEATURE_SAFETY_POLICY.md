# Regime Feature Safety Policy

Prompt 34 adds the Regime Feature Preparation safety policy.

## Fail-Closed Rules

- no feature computation.
- no feature registry writes.
- no classification.
- no regime classification.
- no regime detection.
- no trade signals.
- no recommendations.
- no DecisionObject generation.
- no execution APIs.
- no hidden thresholds.
- no classifier inputs.
- provenance required.
- evidence mapping required.

Feature candidates are metadata only. Feature readiness is not regime
classification. Evidence mapping is not hidden decision logic.

## Forbidden Interpretation

Regime feature preparation must not produce buy/sell/hold/watch/avoid output,
action-state logic, confidence-for-action, broker behavior, event publishing to
decision or execution systems, production-ready regime claims, or
production-ready feature claims.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.
