# Decision Desk API No Recommendation Policy

Prompt 40 explicitly forbids recommendation-like behavior in the Decision Desk
API skeleton.

## Policy

The API skeleton has:

- no recommendations.
- no action generation.
- no buy/sell/hold/watch/avoid active outputs.
- no confidence scoring.
- no DecisionObject generation.
- no approvals.
- no overrides.
- no execution APIs.
- no hidden thresholds.

The API skeleton is contract skeleton only. Every response remains unavailable
or placeholder metadata and must not be interpreted as a trade call,
recommendation, approval, safety pass, action state, market-state decision, or
execution instruction.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.
