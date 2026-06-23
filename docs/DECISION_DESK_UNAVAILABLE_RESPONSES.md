# Decision Desk Unavailable Responses

Prompt 40 adds unavailable response contracts for the Decision Desk API
skeleton.

## Purpose

Unavailable responses are the fail-closed output for every current Decision Desk
API skeleton endpoint. They make the API contract discoverable while preventing
any endpoint response from being interpreted as a recommendation, approval,
trade readiness, active DecisionObject, or execution instruction.

## Unavailable Reasons

Unavailable reasons include:

- recommendations disabled.
- action generation disabled.
- confidence scoring disabled.
- DecisionObject generation disabled.
- execution disabled.
- human review required.
- evidence bundle required.
- contract skeleton only.

## Boundary

An unavailable response is not a system failure. It is the intended Prompt 40
behavior. No recommendation is returned, no approval is returned, no override is
returned, no confidence score is returned, no action state is returned, and no
execution API is exposed.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.

