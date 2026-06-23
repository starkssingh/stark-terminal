# Decision Desk Action Placeholders

Prompt 36 defines action placeholders for future planning only. These names are
not generated actions and are not recommendations.

## Planned Placeholder Categories

- BUY_BIAS
- SELL_BIAS
- HOLD
- WATCH
- AVOID
- REDUCE

These placeholder categories are contract metadata only. They must not be shown
as active outputs, action states, trade calls, signals, or recommendation labels
in Prompt 36.

## Safety Boundary

Prompt 36 includes no action-state engine, no active action generation, no
confidence/action-state scoring, no DecisionObject generation, no broker
integration, and no execution APIs. Future action generation requires separate
validation, evidence, human-review, safety, and audit prompts.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The target
desktop product remains Windows-native Stark Terminal.
