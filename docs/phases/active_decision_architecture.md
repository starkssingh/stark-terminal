# Active Decision Architecture Phase Target

Status: future target documentation only.

The active decision architecture is documented as a future target, not an active implementation.

## Target Pipeline

Market data
↓
Data quality + provenance layer
↓
Timeseries engine
↓
Feature / regime / state engine
↓
Deterministic quant engine
↓
Decision candidate
↓
Verifier layer
↓
Human review / paper-trade gate
↓
Audit log + journal

## Principles

- Decision candidate is not a trade.
- No direct market-data-to-trade path is allowed.
- No direct signal-to-trade path is allowed.
- The verifier layer is the hard gate.
- Human review / paper-trade gate must come before anything execution-like.
- Audit log + journal must preserve provenance, checks, reasons, and outcomes.
- No LLM or autonomous model may bypass the verifier.
- Strategy, backtest, or recommendation output must not become executable without future explicitly audited phases.
- Execution APIs remain forbidden.

## Current Boundary

No active decision engine, paper trading engine, broker integration, order placement, readiness-to-trade generation, recommendation engine, confidence scoring engine, or execution API exists in this target documentation phase.
