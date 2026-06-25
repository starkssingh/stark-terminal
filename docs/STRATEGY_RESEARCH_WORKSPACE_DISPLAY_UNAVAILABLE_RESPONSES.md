# Strategy Research Workspace Display Unavailable Responses

Prompt 65 defines unavailable display responses for the Strategy Research
Workspace Display Contract Skeleton.

## Purpose

Unavailable display responses make fail-closed behavior explicit. They are
expected in this phase because the display layer is unavailable by default and
display contract skeleton only.

## Boundary

Unavailable display responses return no active UI, no frontend components, no
desktop components, no paper parser, no strategy, no generated strategy code,
no backtest, no optimization result, no recommendation, no action state, no
confidence score, no DecisionObject generation, no readiness-to-trade, no
broker controls, no approval or override, and no execution control.

Development remains Mac mini M2 / macOS / Apple Silicon. The target desktop
product remains Windows-native Stark Terminal.
