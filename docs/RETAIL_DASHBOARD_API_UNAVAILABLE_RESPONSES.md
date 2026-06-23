# Retail Dashboard API Unavailable Responses

Retail Dashboard API unavailable responses are the expected output in Prompt
50.

## Purpose

Unavailable responses make the API fail closed while the Retail Dashboard is
still a contract skeleton. They prevent callers from treating API placeholders
as active UI, recommendation cards, dashboard decisions, broker controls, or
execution controls.

## Unavailable Reasons

Unavailable reasons include active UI disabled, recommendations disabled,
action generation disabled, confidence scoring disabled, DecisionObject
generation disabled, readiness-to-trade disabled, broker controls disabled,
execution disabled, and API contract skeleton only.

## Fail-Closed Behavior

Each unavailable response is marked `unavailable=true` and
`api_contract_skeleton_only=true`. It returns no active UI, no recommendation,
no action generation, no confidence scoring, no DecisionObject generation, no
readiness-to-trade, no approval, no override, no broker controls, and no
execution APIs.

Development remains Mac mini M2 on macOS / Apple Silicon. The target desktop
product remains Windows-native Stark Terminal.
