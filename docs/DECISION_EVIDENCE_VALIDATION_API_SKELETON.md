# Decision Evidence Validation API Skeleton

Prompt 44 adds a read-only Decision Evidence Validation API skeleton.

## Endpoints

- `GET /decision-evidence-validation/health`
- `GET /decision-evidence-validation/contracts`
- `GET /decision-evidence-validation/template`
- `GET /decision-evidence-validation/sample`

The sample endpoint uses only built-in default contracts and accepts no user
input. The API has no POST endpoints.

## Boundary

The API does not provide a user-supplied market-data validation endpoint. It
does not validate arbitrary market data for a recommendation. It does not
return readiness-to-trade, generate recommendations, compute confidence,
generate action states, create active DecisionObjects, grant approval, allow
override, expose secrets, make external calls, or expose execution APIs.

Validation API responses are validation-only metadata. They are not production
decision claims and not investment advice.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.

