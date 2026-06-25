# Strategy Research Workspace API Request Response Placeholders

Prompt 64 defines Strategy Research Workspace API request and response
placeholders for contract metadata only.

## Request Placeholder

The request placeholder can carry requested workspace, artifact, paper,
hypothesis, dataset, and experiment reference identifiers. It requires a safety
reference by default.

The request placeholder allows no active UI fields, no active action fields, no
computed strategy fields, no backtest fields, no paper ingestion, no paper
parsing, no strategy generation, no strategy code generation, no optimization,
no recommendation generation, no confidence scoring, no DecisionObject
generation, no readiness-to-trade, no broker controls, and no execution APIs.

## Response Placeholder

The response placeholder contains:

- workspace reference.
- artifact reference.
- paper reference.
- hypothesis reference.
- dataset reference.
- experiment reference.
- safety reference.
- unavailable response.

It generates no paper, no parsed research, no strategy, no strategy code, no
backtest, no optimization result, no recommendation, no action state, no
confidence score, no active UI, no active DecisionObject fields, no
readiness-to-trade, no broker controls, and no execution behavior.

The API remains unavailable by default and API contract skeleton only.
