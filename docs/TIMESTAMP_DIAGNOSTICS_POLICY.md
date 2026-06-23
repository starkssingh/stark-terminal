# Timestamp Diagnostics Policy

Prompt 32 defines the timestamp policy for Time-Series Diagnostics.

## Timestamp Policy

- timestamps must be timezone-aware by default.
- timezone-aware timestamps are normalized consistently to UTC.
- naive timestamps are rejected when `require_timezone_aware=true`.
- source references are required.
- real market data claims are rejected under current settings.

## Monotonicity Convention

input-order policy: order is diagnosed exactly as provided. The diagnostics layer does not silently
sort timestamps before reporting order quality.

- `STRICTLY_INCREASING`: every timestamp is greater than the previous timestamp.
- `NON_DECREASING`: timestamps never move backward, but duplicates exist.
- `NON_MONOTONIC`: at least one timestamp moves backward.

## Duplicate Convention

Duplicate timestamp diagnostics return each duplicated timestamp once, preserving
the first duplicate encounter order. Duplicates are data-quality observations,
not trading interpretations.

## Interval Convention

Intervals are calculated between adjacent timestamps in the provided order. Gap
and irregular interval diagnostics require monotonic input to avoid hiding input
quality issues.

## Failure Behavior

Invalid inputs fail closed through validation or failed descriptive results. The
diagnostics layer performs no external calls, no file IO, no persistence writes,
no event publishing, no provider calls, no scraping, and no broker integration.
Explicit audit phrase: no trading interpretation.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The target
desktop product remains Windows-native Stark Terminal.
