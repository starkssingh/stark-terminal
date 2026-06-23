# Decision Evidence Provenance Policy

Prompt 38 requires provenance contracts before any future DecisionObject
evidence bundle can be validated.

## Required Provenance

Every future evidence item must have:

- source reference requirement.
- validation report requirement.
- dataset manifest where applicable.
- analytics family provenance where applicable.
- synthetic/local-only current scope.
- schema version and auditability.

Real market data is not allowed in Prompt 38. Synthetic/local file data remains
test/dev data only and is not trusted real market data, not trading data, and
not investment advice.

Provenance completeness is not a trade recommendation, not approval, not an
action state, and not a DecisionObject generation signal.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.

