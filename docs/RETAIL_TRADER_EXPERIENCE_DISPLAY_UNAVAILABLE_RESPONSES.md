# Retail Trader Experience Display Unavailable Responses

Retail Trader Experience Display unavailable responses are the expected output in Prompt 58. They provide a fail-closed display contract response and do not unlock any active experience.

Unavailable by default means the display contract may describe future placeholder surfaces, but it does not render them and does not produce generated trading output.

Prompt 58 requires:

- no active UI is returned
- no frontend components are returned
- no desktop components are returned
- no recommendation is returned
- no action generation is returned
- no confidence scoring is returned
- no DecisionObject generation is returned
- no readiness-to-trade is returned
- no broker controls are returned
- no suitability profiling is returned
- no approval or override is returned
- no execution control is returned
- no execution APIs are exposed

The unavailable response is display-contract-skeleton-only and remains appropriate until a future audited prompt changes the phase.
