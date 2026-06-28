# Strategy Research Module Boundary Policy

The module boundary policy is boundary-hardening-only. It defines allowed
purposes for Strategy Research Workspace packages and rejects module-level
bypasses.

Development remains Mac mini M2 / macOS / Apple Silicon. The target desktop
product remains Windows-native Stark Terminal.

## Module Families

- `strategy_research_workspace`: planning and guardrail placeholders only.
- `strategy_research_workspace_api`: API contract skeleton placeholders only.
- `strategy_research_workspace_display`: display contract skeleton
  placeholders only.
- `strategy_research_workspace_boundary`: boundary-hardening contracts and
  invariant helpers only.

## Forbidden Module Behavior

Modules may not create active UI, frontend components, desktop components,
paper ingestion, paper parsing, arXiv ingestion, LLM paper analysis, method
extraction, strategy extraction, strategy generation, strategy code
generation, signal generation, factor generation, alpha generation,
backtesting, optimization, parameter search, walk-forward analysis,
performance claims, recommendations, action generation, confidence scoring,
DecisionObject generation, readiness-to-trade, broker controls, approvals,
overrides, external calls, provider SDK use, scraping, or execution APIs.

## Prompt 69 Integration Readiness

Prompt 69 confirms module boundary policies protect Strategy Research
Workspace planning, API, display, and boundary modules together. No module
creates an API-to-display strategy path, parsed-paper display path,
backtest-result display path, recommendation path, readiness-to-trade path,
broker-control path, or execution path.
