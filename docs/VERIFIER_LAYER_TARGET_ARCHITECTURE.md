# Verifier Layer Target Architecture

This document records the future verifier layer target. It is not an active
verifier implementation, not a risk engine, not an expected value engine, not a
confidence scoring engine, and not execution infrastructure. Execution APIs remain forbidden.

## Required Verifier Checks

The future verifier layer must evaluate every future decision candidate across:

- data quality
- risk limits
- exposure
- liquidity
- market regime conflict
- expected value
- confidence reliability
- regulatory/compliance constraints
- strategy validity / backtest provenance

## Safety Rules

Expected value must be evidence-bound. A future expected value check cannot be
accepted unless it can reference source data, method assumptions, and
validation context.

Confidence must be calibrated/reliability-checked. Confidence must not be a
raw score that bypasses validation, calibration, or historical reliability
review.

Backtest provenance must be available before strategy-derived candidates are trusted. Strategy validity requires traceable research artifacts, method history, validation notes, and backtest provenance before any candidate can be considered beyond placeholder status.

Verifier failure must block candidate progression. A failed verifier check
must prevent movement into human review, paper-trade gates, or any future
execution-like stage.

Verifier must not place orders. The verifier layer is a gate, not a broker,
not an order router, not an approval engine, not a paper trading engine, and
not an execution API.

No LLM/autonomous model may bypass the verifier. Any future LLM-assisted
research, explanation, or summarization path must remain subordinate to
deterministic gates and explicit audits.
