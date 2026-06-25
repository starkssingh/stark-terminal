# Retail Dashboard Forbidden Behavior Registry

Prompt 54 adds a Retail Dashboard forbidden behavior registry. The registry is documentation-backed contract metadata only; it does not enable any Retail Dashboard capability.

## Forbidden Categories

The registry blocks:

- active UI
- frontend components
- desktop components
- recommendation cards
- action buttons
- confidence score widgets
- DecisionObject display
- readiness-to-trade
- broker controls
- order buttons
- execution
- approval controls
- override controls
- real or live market data display
- external calls
- secrets or credentials
- provider SDK behavior
- scraping

Each behavior is forbidden now, requires a future prompt before unlock, and requires audit-before-unlock. The registry itself is a boundary-hardening-only artifact.

## Safety Interpretation

A forbidden behavior entry is not a roadmap approval. It is a blocker declaration. Retail Dashboard modules and endpoints must not interpret registry coverage as permission to implement recommendations, broker controls, active UI, or execution APIs.

Development remains on Mac mini M2 / macOS / Apple Silicon. The target desktop product remains Windows-native Stark Terminal.

## Prompt 55 Integration Readiness Confirmation

Prompt 55 confirms the forbidden behavior registry covers the Retail Dashboard
planning, API, display, and boundary integration surface. The registry remains
policy metadata only and does not unlock active UI, frontend components,
desktop components, recommendations, action generation, confidence scoring,
DecisionObject generation, readiness-to-trade, broker controls, approvals,
overrides, or execution APIs.
