# Decision Desk Request Response Placeholders

Prompt 40 defines request placeholder and response placeholder schemas for the
Decision Desk API skeleton.

## Request Placeholder

The request placeholder records a planned request kind, optional instrument ID,
optional timeframe, requested sections, and required evidence/safety/human-review
references. It is not a live request for recommendations.

## Response Placeholder

The response placeholder contains:

- an evidence reference placeholder.
- a safety reference placeholder.
- an unavailable response.
- planning-only metadata.

The response placeholder has no computed recommendation fields, no active action
fields, no confidence score, no active DecisionObject fields, no approval, no
override, and no execution readiness.

## Reference Placeholders

Evidence references are placeholders only and do not mean that a complete
DecisionObject evidence bundle exists. Safety references are placeholders only
and do not mean that a safety check passed.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.

