# Retail Trader Experience Forbidden Behavior Registry

Prompt 61 adds a Retail Trader Experience forbidden behavior registry. The
registry is a boundary-hardening-only contract and does not enable any
capability.

The registry marks these behavior categories as forbidden now:

- Active UI.
- Frontend components.
- Desktop components.
- Recommendation cards.
- Action buttons.
- Confidence scores.
- DecisionObject display.
- Readiness-to-trade.
- Suitability profiling.
- Trading permission profiles.
- Persona-to-suitability-profile paths.
- Journey-to-trading-advice paths.
- Broker controls.
- Order buttons.
- Execution.
- Approval controls.
- Override controls.
- Real or live data display.
- External calls.
- Secrets or credentials.
- Provider SDKs.
- Scraping.

Every forbidden behavior requires a future prompt and an audit-before-unlock.
The registry itself cannot grant approval, create overrides, generate
recommendations, create active UI, produce suitability profiling, expose broker
controls, or enable execution APIs.

This registry is used by endpoint and module boundary policies as a shared
source of forbidden behavior names. It is not a workflow engine, permission
system, trading system, broker integration, or UI implementation.

## Prompt 62 Integration Readiness Confirmation

Prompt 62 confirms the forbidden behavior registry remains integrated with
Retail Trader Experience endpoint policies, module policies, and cross-module
invariants. The registry still does not enable active UI, recommendations,
action generation, confidence scoring, DecisionObject generation,
readiness-to-trade, suitability profiling, broker controls, approvals,
overrides, or execution APIs.
