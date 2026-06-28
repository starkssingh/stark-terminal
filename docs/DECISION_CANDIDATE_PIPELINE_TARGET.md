# Decision Candidate Pipeline Target

This document defines the future decision candidate pipeline target. It is a
conceptual architecture note only and is not an active implementation.
Execution APIs remain forbidden.

## Candidate Boundary

Market data is not a decision. Market data must first pass a future data
quality + provenance layer before any future decision candidate use. This
document does not enable market-data ingestion.

Features/regimes are not trades. A future Feature / regime / state engine may
describe state, but state does not authorize action and does not create an
order.

Deterministic quant engine output is not a trade. The deterministic quant
engine may only produce a future decision candidate, not an executable order,
not a recommendation, and not a trade commit.

Decision candidate is not a trade. A candidate is only a candidate and must pass verifier checks before it can progress to any future human review or paper-trade gate.

## Blocked Direct Paths

No direct market-data-to-trade path is allowed.

No direct signal-to-trade path is allowed.

No direct strategy-to-trade path is allowed.

No direct backtest-to-trade path is allowed.

No direct recommendation-to-execution path is allowed.

No direct trade commit path is allowed in the current system or in any future
phase without explicit prompt scope, safety audit, verifier gate definition,
human/paper gate definition, and execution-specific approval.

The current Stark Terminal codebase remains contract/skeleton/audit/boundary-
first. It does not implement active decision generation, recommendation generation, confidence scoring, paper trading, broker controls, market-data ingestion, strategy generation, backtesting, or execution APIs.
