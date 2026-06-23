# Time-Series Gap Diagnostics

Prompt 32 implements fixed-interval gap diagnostics for timestamp series.

## Expected Interval

`expected_interval_seconds` must be a positive integer. Gap diagnostics require
this value. If it is missing for a gap request, the request fails safely.

## Gap Definition

A gap exists when an observed interval is greater than the expected interval:

`observed_interval_seconds > expected_interval_seconds`

The diagnostic uses timestamps in the provided order after validating that the
series is monotonic enough for interval analysis.

## Missing Count Estimate

The missing count estimate is:

`max(floor(observed_interval_seconds / expected_interval_seconds) - 1, 0)`

This is a descriptive estimate only. It is not a reconstruction of actual market
events and must not be treated as real market data.

## Limitations

Duplicate or non-monotonic timestamps are reported safely. Non-monotonic input
blocks interval diagnostics so the result does not hide timestamp-quality
problems.

Gap outputs are descriptive-only and data-quality-only. Gaps are not signals,
not recommendations, not DecisionObjects, and not execution instructions.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The target
desktop product remains Windows-native Stark Terminal.

