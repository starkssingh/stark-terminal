# Decision Readiness Unavailable Responses

Prompt 42 adds unavailable response contracts for the Decision Desk Readiness
API skeleton.

## Purpose

Unavailable responses are the fail-closed output for every current Decision
Desk Readiness API skeleton endpoint. They make the readiness API contract
discoverable while preventing any endpoint response from being interpreted as a
recommendation, approval, override, safety pass, readiness-to-trade status,
active DecisionObject, or execution instruction.

## Unavailable Reasons

Unavailable reasons include:

- recommendations disabled.
- action generation disabled.
- confidence scoring disabled.
- DecisionObject generation disabled.
- execution disabled.
- approval disabled.
- override disabled.
- human review required.
- evidence bundle required.
- safety guardrails required.
- contract skeleton only.

## Boundary

An unavailable response is not a system failure. It is the intended Prompt 42
behavior. No readiness status is returned, no recommendation is returned, no
approval is returned, no override is returned, no confidence score is returned,
no action state is returned, no DecisionObject is generated, and no execution
API is exposed.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.
