# Decision Cross-Module Invariants

Prompt 47 adds cross-module invariants for the Decision Desk skeleton stack.

## Invariants

The invariant layer checks that endpoint policies, module policies, and the
forbidden behavior registry agree on these boundaries:

- no recommendations.
- no action generation.
- no confidence scoring.
- no active DecisionObjects.
- no approvals.
- no overrides.
- no active UI.
- no active workflow.
- no readiness-to-trade.
- no execution.

## Blockers And Warnings

Any boundary violation is a blocker. A passed invariant result cannot contain
blockers and cannot set dangerous allowed flags. Rejection helpers return
blocked results for recommendation, execution, approval/override, active
UI/workflow, and readiness-to-trade boundary violations.

These invariants are deterministic contract checks only. They do not read
market data, call external services, publish events, persist outputs, or
create Decision Desk capability.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.
## Prompt 48 Cross-Endpoint Integration Readiness Note

Prompt 48 confirms the cross-module invariants also support cross-endpoint
integration readiness across Decision API, readiness API, display, validation,
human review, and boundary endpoints. Passing invariants remain a safety check
only. They do not permit recommendations, action generation, confidence
scoring, active DecisionObject generation, approvals, overrides, active UI,
active workflow, readiness-to-trade, or execution APIs.
