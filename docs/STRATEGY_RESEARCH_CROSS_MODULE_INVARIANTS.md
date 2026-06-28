# Strategy Research Cross-Module Invariants

Strategy Research cross-module invariants are boundary-hardening-only checks.
They evaluate endpoint policies, module policies, and the forbidden behavior
registry together.

Development remains Mac mini M2 / macOS / Apple Silicon. The target desktop
product remains Windows-native Stark Terminal.

## Invariants

- Endpoint families remain read-only and unavailable by default.
- Module families remain contracts, placeholders, display skeletons, or
  boundary metadata only.
- Dangerous flags remain false across all Strategy Research boundary results.
- Passed invariant results cannot include blockers.
- Rejection helpers return blocked, safe results.

The invariants explicitly prevent active UI, frontend implementation, desktop
implementation, paper ingestion, paper parsing, arXiv ingestion, LLM paper
analysis, strategy generation, strategy code generation, signal/factor/alpha
generation, backtesting, optimization, recommendation generation, action
generation, confidence scoring, DecisionObject generation, readiness-to-trade,
broker controls, approvals, overrides, and execution APIs.

## Prompt 69 Cross Endpoint Integration Readiness

Prompt 69 confirms the invariants apply across
`/strategy-research-workspace/*`, `/strategy-research-workspace-api/*`,
`/strategy-research-workspace-display/*`, and
`/strategy-research-workspace-boundary/*`. The audit confirms no
cross-endpoint bypass, no API-to-display strategy path, no API-to-display
backtest path, no API-to-display recommendation path, no readiness-to-trade
path, no broker-control path, and no execution path.
