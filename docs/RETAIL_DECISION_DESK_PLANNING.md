# Retail Decision Desk Planning

Prompt 36 implements Retail Decision Desk planning and guardrails for Stark
Terminal. This is planning-only governance work for a future retail decision
support surface.

## Purpose

The Retail Decision Desk will eventually organize evidence, risk context,
analytics context, and human-review state for retail-facing decision support.
Prompt 36 does not implement that product surface. It creates contracts and
guardrails so future prompts can add evidence bundle contracts before any
Decision Desk skeleton is considered.

## Current Boundary

Prompt 36 implements:

- planning-only Decision Desk plan contracts.
- action placeholder contracts.
- evidence requirement contracts.
- human-review guardrails.
- display boundary contracts.
- readiness report contracts.
- fail-closed safety policy and health metadata.

Prompt 36 implements no recommendations, no action generation, no action-state
generation, no confidence scoring, no DecisionObject generation, no signals, no trading
decisions, no broker linkage, and no execution APIs.

## Human Review

Human review is required by default. A human-review checklist is not an approval
system and does not unlock recommendations, DecisionObjects, confidence scoring,
or execution in Prompt 36.

## Future Relationship

Prompt 37 should add DecisionObject evidence bundle contracts only. It must
still avoid actual DecisionObject generation, recommendations, confidence
scoring, action generation, and execution APIs.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The target
desktop product remains Windows-native Stark Terminal.
