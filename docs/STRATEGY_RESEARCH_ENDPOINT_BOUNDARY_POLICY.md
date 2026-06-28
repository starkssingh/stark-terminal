# Strategy Research Endpoint Boundary Policy

The endpoint boundary policy is boundary-hardening-only. It defines safe
read-only endpoint families and forbids endpoint-level bypasses.

Development remains Mac mini M2 / macOS / Apple Silicon. The target desktop
product remains Windows-native Stark Terminal.

## Endpoint Families

- `strategy-research-workspace`
- `strategy-research-workspace-api`
- `strategy-research-workspace-display`
- `strategy-research-workspace-boundary`

Each endpoint family is read-only and unavailable by default. Allowed methods
are GET only. POST, PUT, PATCH, and DELETE remain forbidden.

## Forbidden Endpoint Behavior

No endpoint may accept paper input, PDF input, URLs, arXiv IDs, market data
for research decisions, strategy instructions, broker instructions, approval
requests, override requests, or execution requests.

No endpoint may create active UI, frontend components, desktop components,
paper ingestion, paper parsing, arXiv ingestion, LLM paper analysis, strategy
generation, strategy code generation, signal/factor/alpha generation,
backtesting, optimization, recommendation generation, action generation,
confidence scoring, DecisionObject generation, readiness-to-trade, broker
controls, approvals, overrides, or execution APIs.

## Prompt 69 Integration Readiness

Prompt 69 confirms endpoint boundary policies protect planning/API/display
integration. There is no paper input for parsing, no market-data input for
recommendations, no strategy-generation endpoint, no backtesting endpoint, no
recommendation endpoint, no broker-control endpoint, and no execution-like
endpoint.
