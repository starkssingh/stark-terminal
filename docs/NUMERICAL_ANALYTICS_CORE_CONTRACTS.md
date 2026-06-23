# Numerical Analytics Core Contracts

Prompt 27 implements the Numerical Analytics Core Contracts for Stark Terminal.

## Purpose

The numerical core gives future analytics modules a typed, validated contract layer for descriptive/research-only numerical inputs and outputs. It is a contract and validation boundary, not a trading engine and not a market analytics implementation.

## Implemented Scope

- `NumericalSourceReference` records source id, source type, source data reference, synthetic/local semantics, provider name, optional DatasetManifest linkage, schema version, and UTC creation time.
- `NumericalVectorContract` records a numeric vector with finite-value expectations, descriptive-only labeling, safety labeling, and a required source reference.
- `NumericalTableContract` records table shape metadata, required columns, row count, descriptive-only labeling, and a required source reference.
- `NumericalComputationRequest` and `NumericalComputationResult` define safe request/result metadata for validation and tiny descriptive summaries.
- Helper constructors create safe synthetic/local source references, vector contracts, summary requests, and descriptive results.

## Allowed Tiny Helpers

Prompt 27 allows only generic standard-library summaries needed to validate the contracts:

- count.
- min.
- max.
- mean.
- finite values.
- shape checks.
- source reference checks.

These helpers are descriptive-only and carry no trading or investment meaning.

## Explicit Non-Scope

Prompt 27 does not implement returns, rolling windows, volatility, drawdown, correlation, beta, indicators, factors, feature computation, regimes, model outputs, backtests, signals, recommendations, DecisionObject generation, broker integration, or execution APIs.

Numerical metrics are not signals. Count, min, max, and mean are descriptive research metadata only.

## Future Relationship

Future returns, rolling window, volatility, drawdown, and correlation modules must use these contracts with validation gates, source references, documentation, tests, and safety audits before any scoped calculation is added.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
