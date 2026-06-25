# Retail Trader Experience No-Recommendation Policy

Retail Trader Experience planning cannot be treated as a recommendation
surface.

Prompt 56 allows no experience-as-recommendation behavior, no recommendation
cards, no buy/sell/hold/watch/avoid active outputs, no action generation, no
action states, no confidence scoring, no active DecisionObject generation, no
active DecisionObject display, no readiness-to-trade, and no hidden thresholds
or trade interpretation.

Persona, journey, section, card, dashboard, decision, evidence, safety, and
readiness references are placeholders only. They do not make synthetic or local
data trusted real market data, and they do not imply validated
recommendations.

Planning-only outputs are not trading advice, investment advice, suitability
profiles, broker controls, approvals, overrides, or execution instructions.
There are no action states in Prompt 56.

Development remains Mac mini M2 / macOS / Apple Silicon. The target desktop
product remains Windows-native Stark Terminal.

## Prompt 57 API No-Recommendation Linkage

Prompt 57 extends this policy to the Retail Trader Experience API skeleton. API
request placeholders, response placeholders, persona references, journey
references, dashboard references, decision references, safety references, and
unavailable responses cannot generate recommendations, buy/sell/hold/watch/avoid
outputs, action states, confidence scores, active DecisionObjects,
readiness-to-trade, suitability profiles, broker controls, or execution.

## Prompt 58 Display No-Recommendation Linkage

Prompt 58 extends this policy to the Retail Trader Experience Display Contract
Skeleton. Persona visual placeholders, journey visual placeholders, visual
sections, widgets, badges, and unavailable display responses cannot generate
recommendation cards, recommendation widgets, buy/sell/hold/watch/avoid
outputs, action states, confidence scores, DecisionObject displays,
readiness-to-trade, suitability profiles, broker controls, or execution.

## Prompt 59 Safety Boundary Audit Confirmation

Prompt 59 confirms the no-recommendation policy across planning, API, and
display layers. No recommendation cards, recommendation widgets,
buy/sell/hold/watch/avoid active outputs, action generation, confidence
scoring, active DecisionObject display, readiness-to-trade, hidden trade
interpretation, or experience-as-recommendation behavior exists.

## Prompt 61 Boundary Hardening Confirmation

Prompt 61 strengthens the no-recommendation policy with a forbidden behavior
registry, endpoint boundary policies, module boundary policies, and
cross-module invariants. No Retail Trader Experience endpoint or module can
convert placeholders into recommendations, action generation, confidence
scoring, DecisionObjects, readiness-to-trade, or hidden trade interpretation.
