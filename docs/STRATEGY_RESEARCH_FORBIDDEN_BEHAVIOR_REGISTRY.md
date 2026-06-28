# Strategy Research Forbidden Behavior Registry

The Strategy Research forbidden behavior registry is boundary-hardening-only.
It records behavior kinds that must remain blocked across Strategy Research
Workspace planning, API, display, and boundary layers.

Development remains Mac mini M2 / macOS / Apple Silicon. The target desktop
product remains Windows-native Stark Terminal.

## Prompt 69 Integration Readiness Confirmation

Prompt 69 confirms the forbidden behavior registry covers API/display
integration boundaries. It continues to block active UI, frontend
implementation, desktop implementation, paper ingestion, paper parsing, arXiv
ingestion, LLM paper analysis, strategy generation, strategy code generation,
signal/factor/alpha generation, backtesting, optimization, recommendation
generation, action generation, confidence scoring, DecisionObject generation,
readiness-to-trade, broker controls, approvals, overrides, execution APIs,
API-to-display strategy paths, API-to-display backtest result paths,
parsed-paper-to-display paths, research-as-recommendation paths, and
research-as-execution-control paths.

Research Artifact Registry remains ready for Planning and Guardrails only.
Registry implementation, active artifact ingestion/storage, paper parsing,
strategy generation, backtesting, recommendations, broker controls, and
execution remain forbidden until future prompts and audits explicitly unlock
them.

## Registry Coverage

The registry covers active UI, frontend components, desktop components, paper
ingestion, paper parsing, arXiv ingestion, LLM paper analysis, method
extraction, strategy extraction, strategy generation, strategy code
generation, signal generation, factor generation, alpha generation,
backtesting, optimization, parameter search, walk-forward analysis,
performance claims, recommendation generation, action generation, confidence
scoring, DecisionObject generation, readiness-to-trade, broker controls, order
buttons, execution, approval controls, override controls, live data display,
external calls, secrets or credentials, provider SDKs, and scraping.

Each behavior remains forbidden now, requires a future prompt, and requires an
audit before unlock. The registry does not create active UI, paper parsing,
strategy generation, backtesting, recommendations, broker controls, or
execution APIs.
