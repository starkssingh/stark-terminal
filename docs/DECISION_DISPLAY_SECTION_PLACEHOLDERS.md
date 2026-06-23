# Decision Display Section Placeholders

Prompt 43 defines display section placeholder schemas for the Decision Desk
Display contract skeleton.

## Section Placeholder Schema

A section placeholder records a stable section identifier, section kind, title,
description, placeholder cards, visibility flag, unavailable state,
planning-only state, schema version, timestamp, and notes.

Supported section kinds include:

- HEADER
- EVIDENCE_SUMMARY
- RISK_SUMMARY
- DATA_QUALITY
- HUMAN_REVIEW
- SAFETY_STATUS
- UNAVAILABLE_NOTICE

## Placeholder Layout

The placeholder layout can show planned sections and cards as contract metadata
only. It is not a live UI implementation and does not render active Decision
Desk behavior.

Prompt 43 has no recommendation sections, no execution sections, no broker
linked controls, no approval controls, no override controls, and no
readiness-to-trade display.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.

