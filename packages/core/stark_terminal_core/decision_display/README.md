# Decision Display Package

Prompt 43 adds the `decision_display` package as a display contract skeleton
only.

This package defines display contract metadata, section placeholders, card
placeholders, badge placeholders, evidence/safety reference placeholders,
unavailable display responses, and health metadata for future Decision Desk
surfaces.

It implements no active frontend UI, no recommendation cards, no action
generation, no confidence scoring, no active DecisionObject generation, no
readiness-to-trade, no approval, no override, no broker behavior, and no
execution APIs.

Future prompts may add UI skeletons only after separate audits. Display
placeholders in Prompt 43 are contract metadata only and must not be interpreted
as recommendations, approvals, safety passes, readiness-to-trade, or execution
instructions.
