# Strategy Research Workspace API Unavailable Responses

Prompt 64 defines unavailable responses for the Strategy Research Workspace
API contract skeleton.

## Purpose

Unavailable responses make fail-closed behavior explicit. They are expected in
this phase because the Strategy Research Workspace API is unavailable by
default and API contract skeleton only.

## Unavailable Reasons

Unavailable reasons include active UI disabled, frontend components disabled,
desktop components disabled, paper ingestion disabled, paper parsing disabled,
strategy generation disabled, strategy code generation disabled, backtesting
disabled, optimization disabled, recommendations disabled, action generation
disabled, confidence scoring disabled, DecisionObject generation disabled,
readiness-to-trade disabled, broker controls disabled, execution disabled, and
API contract skeleton only.

## Boundary

Unavailable responses return no active UI, no paper parser, no strategy, no
backtest, no recommendation, no action state, no confidence score, no
DecisionObject generation, no readiness-to-trade, no broker controls, and no
execution control.
