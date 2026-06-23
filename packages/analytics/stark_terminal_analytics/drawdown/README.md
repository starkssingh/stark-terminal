# Drawdown Analytics v0

This package contains descriptive drawdown analytics for Prompt 29.

- Drawdown is calculated as `current_value / running_peak - 1`.
- Drawdown values are zero or negative.
- Max drawdown is the minimum drawdown value.
- Drawdown duration is the longest consecutive run below zero.
- Inputs require positive synthetic/local/test values and source references.
- Outputs are descriptive-only research artifacts.
- No thresholds, regime labels, signals, recommendations, DecisionObject generation, or execution APIs are implemented.
