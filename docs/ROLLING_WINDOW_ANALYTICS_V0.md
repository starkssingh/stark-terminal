# Rolling Window Analytics v0

Prompt 28 implements Rolling Window Analytics v0 for Stark Terminal.

## Purpose

Rolling Window Analytics v0 provides tiny deterministic descriptive rolling metrics over validated synthetic/local vectors. It uses source references from Prompt 27 Numerical Analytics contracts and keeps all outputs descriptive-only.

## Supported Metrics

- rolling count.
- rolling mean.
- rolling min.
- rolling max.

Prompt 28 uses a right-aligned window convention. For vector length `n` and window `w`, output length is `n - w + 1` when `w <= n`.

## Input Requirements

- Vectors must contain finite values.
- Source references are required.
- Window size must be positive.
- Window size must not exceed the vector length for successful calculation.
- Window size must respect the configured max window when validation receives one.
- Real market data claims are rejected under current settings.

## Safety Boundary

Rolling Window Analytics v0 produces descriptive-only research metrics. Rolling averages are not trend calls, rolling min/max are not support/resistance calls, and rolling counts are not quality approvals.

Prompt 28 implements no trend labels, no thresholds, no signals, no recommendations, no DecisionObject generation, no execution APIs, no volatility, no drawdown, and no correlation.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
