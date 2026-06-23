# Correlation and Beta Validation Policy

Prompt 31 adds deterministic local validation helpers for Correlation Analytics v0 and Beta Analytics v0.

## Paired Vector Validation

Correlation and beta requests require paired vectors that satisfy:

- equal length.
- minimum observations of at least two.
- finite values.
- source-reference presence on both vectors.
- descriptive-only vector contracts.
- no real market data claims under current settings.

## Correlation Validation

Pearson correlation requires non-zero sample variance for both input vectors. If either vector has zero variance, correlation is undefined and the calculation fails safely.

## Beta Validation

Beta requires non-zero sample variance for the benchmark return vector. If benchmark variance is zero, beta is undefined and the calculation fails safely.

## Failure Behavior

Prompt 31 failure behavior is fail-closed: invalid inputs return failed descriptive results where practical. Failed results do not become signals, recommendations, decisions, DecisionObjects, or execution approvals.

## Side-Effect Boundary

Validation performs no external calls, no file IO, no persistence writes, no event publishing, no provider calls, no scraping, and no broker integration. Helpers are deterministic and do not mutate input contracts.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The target desktop product remains Windows-native Stark Terminal.
