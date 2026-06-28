# Research Artifact Registry Display Unavailable Responses

Prompt 72 display unavailable responses are fail-closed response contracts for the Research Artifact Registry Display skeleton.

Every unavailable response must state that the display layer is unavailable-by-default and display-contract-skeleton-only. Dangerous flags must remain false:

- active UI
- frontend components
- desktop components
- active ingestion
- persistent storage
- file uploads
- file downloads
- paper parsing
- strategy generation
- backtesting
- recommendations
- execution

Unavailable responses must not provide parsed paper content, generated strategies, backtest results, recommendation cards, confidence scores, DecisionObjects, readiness-to-trade, broker controls, approvals, overrides, or execution controls.
