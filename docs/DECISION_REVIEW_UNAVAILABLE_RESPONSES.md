# Decision Review Unavailable Responses

Prompt 45 adds unavailable responses for Decision Human Review workflow
skeleton endpoints.

## Purpose

Unavailable responses are expected in this phase. They tell clients that human
review workflow behavior is not available and that the returned payload is
workflow skeleton metadata only.

## Fail-Closed Behavior

Unavailable responses set workflow-skeleton-only flags and keep every
dangerous capability false: no active workflow, no task assignment, no reviewer
auth, no notifications, no approval, no override, no recommendations, no
action generation, no confidence scoring, no DecisionObject generation, no
readiness-to-trade, and no execution APIs.

An unavailable response is not a failure of architecture. It is the intended
safe output until future audits authorize a different contract boundary.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.
