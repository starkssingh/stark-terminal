# Regime Analytics Safety Policy

Prompt 33 adds the Regime Analytics safety policy.

## Fail-Closed Rules

- no classification.
- no regime detection.
- no real market data assumption.
- no trade signals.
- no recommendations.
- no DecisionObject generation.
- no execution APIs.
- no broker integration.
- no hidden thresholds.
- human review required.
- evidence required.

Regime readiness is not a market state. Evidence requirements are not hidden
decision logic. Label placeholders are not trading instructions.

## Human Review

Human review is required before any future feature preparation, classifier
design, validation process, or user-facing regime surface can be considered.
Prompt 33 readiness reports keep `ready_for_classification=false` and
`ready_for_production=false`.

## Prompt 34 Regime Feature Preparation Boundary

Prompt 34 extends the safety boundary to regime feature preparation contracts.
Feature candidates, feature groups, provenance requirements, evidence mappings,
and readiness templates are contracts-only.

The regime feature layer has no feature computation, no feature registry
writes, no classifier inputs, no actual regime classification, no trade
signals, no recommendations, no DecisionObject generation, no execution APIs,
and no hidden thresholds. Provenance and evidence mapping are required before
any future feature computation prompt can be considered.

## Forbidden Interpretation

Regime planning must not produce buy/sell/hold/watch/avoid output, action-state
logic, confidence-for-action, broker behavior, or event publishing to decision
or execution systems.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.
