# Decision Readiness Request Response Placeholders

Prompt 42 defines request placeholder and response placeholder schemas for the
Decision Desk Readiness API skeleton.

## Request Placeholder

The readiness request placeholder records a planned request kind, optional
instrument ID, optional timeframe, requested readiness sections, and required
evidence, safety, human-review, and blocked-output references.

It is not a live request for readiness-to-trade, recommendations, action
generation, confidence scoring, active DecisionObject generation, approval,
override, or execution.

## Response Placeholder

The readiness response placeholder contains:

- a decision evidence reference placeholder.
- a decision safety reference placeholder.
- a human-review reference placeholder.
- a blocked-output policy reference placeholder.
- an unavailable response.
- planning-only metadata.

The response placeholder has no computed readiness-to-trade fields, no computed
recommendation fields, no active action fields, no confidence score, no active
DecisionObject fields, no approval, no override, and no execution readiness.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.
