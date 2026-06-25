# Retail Trader Experience Forbidden Interactions

Prompt 56 defines forbidden Retail Trader Experience interactions as planning
contracts only. A forbidden interaction entry is a blocker declaration, not a
permission to implement the behavior.

## Forbidden Categories

The registry forbids recommendation cards, action buttons, confidence scores,
DecisionObject display, readiness-to-trade badges, broker controls, order
buttons, approval controls, override controls, suitability profiling, and live
data controls.

Each interaction is forbidden now, requires a future prompt before unlock, and
requires audit-before-unlock.

## Safety Interpretation

Forbidden interaction coverage does not enable active UI, frontend components,
desktop components, recommendations, action generation, confidence scoring,
DecisionObject generation, readiness-to-trade, broker controls, suitability
profiling, or execution APIs.

Development remains Mac mini M2 / macOS / Apple Silicon. The target desktop
product remains Windows-native Stark Terminal.
