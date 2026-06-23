# Decision Evidence Validation No-Recommendation Policy

Prompt 44 forbids validation-as-recommendation.

## Policy

- no validation-as-recommendation.
- no validation-as-readiness-to-trade.
- no validation-as-approval.
- no recommendations.
- no action generation.
- no buy/sell/hold/watch/avoid active outputs.
- no confidence scoring.
- no DecisionObject generation.
- no approval.
- no override.
- no execution APIs.
- no hidden thresholds.

Validation may report completeness, missing references, incomplete checklists,
missing human-review attachments, and unsafe flags. It cannot transform those
findings into a trading call, display decision, approval, override, active
DecisionObject, or execution instruction.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.

