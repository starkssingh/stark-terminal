# Numerical Analytics Validation Policy

Prompt 27 adds deterministic local validation helpers for Numerical Analytics contracts.

## Validation Rules

- Finite values are required by default.
- Vectors must be non-empty and must respect the configured maximum vector length.
- Tables must declare columns and a non-negative row count.
- Source references must include source id, source type, and source data reference.
- Real market data claims remain false.
- Numerical outputs must be descriptive-only.
- Signal, recommendation, DecisionObject, and execution flags must remain false.

## Failure Behavior

Invalid values fail safely with descriptive `NumericalComputationResult` objects where practical. Failed results do not contain successful metrics and do not become signals, recommendations, decisions, or execution approvals.

## Side-Effect Boundary

Numerical validation performs no external calls, no file IO, no persistence writes, no event publishing, no provider calls, no scraping, and no broker integration. Helpers are deterministic and do not mutate input contracts.

## No Trading Interpretation

Validation success means only that a numerical contract passed local contract checks. It does not approve real market data, generate DecisionObject evidence, authorize trading interpretation, or create an execution path.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
