# Decision Endpoint Boundary Policy

Prompt 47 adds endpoint boundary policies for Decision Desk endpoint families.

## Endpoint Posture

Decision endpoint policies are read-only and unavailable by default. They
cover:

- `decision-desk`.
- `decision-evidence`.
- `decision-safety`.
- `decision-desk-api`.
- `decision-readiness-api`.
- `decision-display`.
- `decision-evidence-validation`.
- `decision-human-review`.
- `decision-boundary`.

## Forbidden Endpoint Classes

No Decision endpoint may:

- accept market data to generate decisions.
- create market-data-to-recommendation behavior.
- create readiness-to-trade behavior.
- generate recommendations.
- generate action states.
- compute confidence scoring.
- generate active DecisionObjects.
- grant approval.
- grant override.
- expose broker linkage.
- expose execution endpoints.

The endpoint boundary policy adds no POST endpoints and does not mutate durable
state. It is contract metadata only.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.
## Prompt 48 Integration Readiness Note

Prompt 48 confirms endpoint boundary policies cover API/display integration
readiness. Decision endpoints remain read-only, unavailable by default or
skeleton-only, and blocked from market-data-to-decision, API-to-display
recommendation path, readiness-to-display-trade path, approval/override path,
broker linkage, and execution APIs.
