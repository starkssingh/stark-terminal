# Decision Display No Recommendation Policy

Prompt 43 explicitly forbids recommendation-like behavior in the Decision Desk
Display contract skeleton.

## Policy

The display skeleton has:

- no display-as-recommendation.
- no recommendations.
- no action generation.
- no buy/sell/hold/watch/avoid active outputs.
- no confidence scoring.
- no DecisionObject generation.
- no readiness-to-trade.
- no approvals.
- no overrides.
- no execution APIs.
- no hidden thresholds.

The display contract skeleton is contract metadata only. Every response remains
unavailable or placeholder metadata and must not be interpreted as a trade call,
recommendation, approval, override, safety pass, action state, market-state
decision, readiness-to-trade status, UI implementation, or execution
instruction.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.
