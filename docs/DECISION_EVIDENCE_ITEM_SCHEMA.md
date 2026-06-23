# Decision Evidence Item Schema

Prompt 38 defines decision evidence item contracts. Evidence items are schema
metadata only.

## Evidence Item Kinds

- instrument context.
- data quality.
- returns.
- volatility.
- drawdown.
- correlation/beta.
- time-series diagnostics.
- regime context.
- regime feature context.
- risk context.
- human review.

## Status Meanings

- PLANNED: contract exists for future evidence.
- REQUIRED: item is required before future bundle validation.
- MISSING: expected item is absent.
- PRESENT: future validation may mark an item present.
- INVALID: future validation may mark an item invalid.
- BLOCKED: item cannot proceed.

Prompt 38 stores no value payloads and computes no evidence values. Evidence
item contracts contain no computed recommendation fields, no active action
fields, no confidence score, no active DecisionObject generation, and no
execution readiness.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.

