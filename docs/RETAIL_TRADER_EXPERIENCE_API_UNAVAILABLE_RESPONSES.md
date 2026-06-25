# Retail Trader Experience API Unavailable Responses

Prompt 57 keeps Retail Trader Experience API responses unavailable by default.
Unavailable responses are expected in this phase because the API is a contract
skeleton only.

## Unavailable Reasons

- Active UI disabled.
- Frontend components disabled.
- Desktop components disabled.
- Recommendations disabled.
- Action generation disabled.
- Confidence scoring disabled.
- DecisionObject generation disabled.
- Readiness-to-trade disabled.
- Broker controls disabled.
- Execution disabled.
- Suitability profiling disabled.
- API contract skeleton only.

Unavailable responses are fail-closed. They return no active UI, no frontend
components, no desktop components, no recommendation, no action generation, no
confidence score, no active DecisionObject, no readiness-to-trade, no broker
control, no suitability profile, no approval, no override, and no execution
control.
