# Decision Display Card Placeholders

Prompt 43 defines display card placeholder schemas for the Decision Desk
Display contract skeleton.

## Card Placeholder Schema

A card placeholder records a stable card identifier, card kind, title,
description, visibility flag, unavailable state, planning-only state, safety
label, schema version, timestamp, and notes.

Supported card kinds include:

- PLACEHOLDER
- EVIDENCE_PLACEHOLDER
- RISK_PLACEHOLDER
- SAFETY_PLACEHOLDER
- HUMAN_REVIEW_PLACEHOLDER
- UNAVAILABLE

## Boundary

Card placeholders remain unavailable and planning-only. They contain no computed
recommendation fields, no active action fields, no active confidence fields, no
active DecisionObject fields, no readiness-to-trade, no approval, no override,
and no execution readiness.

No display card is an active recommendation card in Prompt 43.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.

