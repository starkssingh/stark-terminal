# Decision Desk Display Boundary

Prompt 36 defines display boundary contracts only. It does not build a Decision
Desk UI.

## Allowed Future Planning Sections

- instrument context placeholder.
- evidence requirements summary.
- data quality boundary.
- risk context placeholder.
- human review status.
- safety boundary.

These are planning-level sections only.

## Forbidden Sections In Prompt 36

- active recommendation cards.
- generated action labels.
- confidence score.
- DecisionObject display.
- execution buttons.
- broker linkage.
- market-data input for recommendations.

Prompt 36 includes no active recommendation cards, no generated action labels,
no confidence score, no execution buttons, no broker linkage, no trading
interpretation, no DecisionObject generation, and no execution APIs.

## Prompt 43 Display Contract Skeleton Note

Prompt 43 adds the Decision Desk Display Contract Skeleton. It defines display
contract metadata, card placeholders, section placeholders, badge placeholders,
evidence/safety display references, and unavailable display responses only. It
does not build active UI, active recommendation cards, generated action labels,
confidence displays, active DecisionObject displays, approval displays,
override displays, readiness-to-trade displays, broker linkage, execution
buttons, or execution APIs.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The target
desktop product remains Windows-native Stark Terminal.
