# Research Artifact Forbidden Behavior Registry

Prompt 75 adds a Research Artifact forbidden behavior registry for boundary
hardening only. The registry records blocked behavior kinds and keeps every
dangerous behavior forbidden now, requiring a future prompt and a future audit
before any unlock.

The registry covers active ingestion, persistent storage, file upload, file
download, file preview, active UI, frontend components, desktop components,
paper ingestion, paper parsing, PDF parsing, arXiv ingestion, LLM paper
analysis, method extraction, strategy extraction, strategy generation,
strategy code generation, signal/factor/alpha generation, backtesting,
optimization, parameter search, walk-forward analysis, performance claims,
recommendation generation, action generation, confidence scoring,
DecisionObject generation, readiness-to-trade, broker controls, order buttons,
execution, approvals, overrides, external calls, secrets, provider SDKs, and
scraping.

All dangerous allowed flags remain false. This is not active registry
implementation, not ingestion/storage, not upload/download, not active UI, not
paper parsing, not strategy generation, not backtesting, not recommendations,
and not execution.

Development remains on Mac mini M2 / macOS / Apple Silicon. The target desktop
product remains Windows-native Stark Terminal.

## Prompt 76 Integration Readiness Note

Prompt 76 confirms the forbidden behavior registry remains integrated with
endpoint boundary policies, module boundary policies, and cross-module
invariants. The registry continues to forbid active ingestion/storage,
upload/download, file preview, active UI, frontend/desktop implementation,
paper parsing, strategy generation, backtesting, recommendations, confidence
scoring, DecisionObject generation, readiness-to-trade, broker controls,
approvals/overrides, external calls, secrets, provider SDKs, scraping, and
execution APIs.
