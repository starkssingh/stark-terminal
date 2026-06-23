# Regime Feature Provenance Policy

Prompt 34 adds Regime Feature Preparation provenance requirements before any
future regime feature computation.

## Required Provenance

Every future regime feature candidate must specify:

- source references.
- analytics family references.
- validation report requirement.
- dataset manifest requirement where applicable.
- synthetic/local-only current scope.
- schema version and auditability.

Prompt 34 provenance contracts point to analytics families and source-reference
requirements only. They do not point to computed feature values.

## Current Boundary

There is no real-data assumption. Real market data remains unavailable to
regime feature preparation. Current provenance requirements allow only
synthetic/local/test planning semantics until a future provider and data-policy
approval phase exists.

Prompt 34 has no feature computation, no feature registry writes, no
classification, no signals, no recommendations, no DecisionObject generation,
and no execution APIs.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.
