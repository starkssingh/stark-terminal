# Decision Display Unavailable Responses

Prompt 43 adds unavailable display response contracts for the Decision Desk
Display contract skeleton.

## Purpose

Unavailable display responses are the fail-closed output for current display
skeleton endpoints. They make the display contract discoverable while
preventing any display card, badge, or section from being interpreted as a
recommendation, approval, override, safety pass, readiness-to-trade status,
active DecisionObject, active UI, or execution instruction.

## Boundary

An unavailable display response is expected in this phase. It is not a system
failure.

No display recommendation is returned. No approval is returned. No override is
returned. No readiness-to-trade is returned. No confidence score is returned. No
action state is returned. No DecisionObject is generated. No execution API is
exposed.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.

