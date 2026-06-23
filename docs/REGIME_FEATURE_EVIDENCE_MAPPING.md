# Regime Feature Evidence Mapping

Prompt 34 maps Regime Analytics evidence requirements to feature candidates.
This evidence mapping is contracts-only and cannot classify a market state.

## Evidence Mapping

The mappings connect planned feature candidates to evidence categories:

- returns evidence.
- volatility evidence.
- drawdown evidence.
- correlation and beta evidence.
- time-series diagnostics evidence.
- volume and liquidity evidence placeholders.
- options context evidence placeholders.
- macro context evidence placeholders.
- market microstructure evidence placeholders.

Missing evidence produces blockers in readiness reports. Missing evidence does
not produce a classification, recommendation, signal, DecisionObject, decision,
or execution instruction.

## Safety Boundary

Evidence mapping is not hidden decision logic. Prompt 34 has no feature
computation, no evidence-derived classification, no signals, no
recommendations, no DecisionObject generation, and no execution APIs.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.
