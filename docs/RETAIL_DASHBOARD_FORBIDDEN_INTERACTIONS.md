# Retail Dashboard Forbidden Interactions

Prompt 49 defines a forbidden interaction registry for Retail Dashboard planning and guardrails.

Forbidden interactions include recommendation card, action button, confidence score, DecisionObject display, readiness-to-trade badge, broker control, order button, approval control, override control, and live data control.

Each forbidden interaction remains forbidden now, requires a future prompt, and requires audit-before-unlock. The registry does not enable any active UI, recommendation, action generation, confidence scoring, DecisionObject generation, readiness-to-trade, broker controls, or execution APIs.

No dashboard control may be interpreted as buy/sell/hold/watch/avoid output. No dashboard interaction may bypass the Decision Desk boundary policies. Development remains Mac mini M2 / macOS while the target desktop product remains Windows-native.
