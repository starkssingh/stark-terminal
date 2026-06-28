# Active Decision Architecture Target

This document records Stark Terminal's future target architecture for active
decision safety. It is documentation only. This is future target architecture,
not current implementation, not active implementation, not an active decision
engine, not a recommendation engine, not paper trading, not broker
integration, and not execution infrastructure.

The current system remains contract/skeleton/audit/boundary-first. Active implementation requires future prompts, future safety audits, and explicit unlock decisions before any execution-like behavior can exist. Execution APIs remain forbidden; execution APIs remain forbidden in the current system and in this future-target documentation.

## Target Pipeline

```text
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
Verifier layer:
- data quality
- risk limits
- exposure
- liquidity
- market regime conflict
- expected value
- confidence reliability
- regulatory/compliance constraints
- strategy validity / backtest provenance
↓
Human review / paper-trade gate
↓
Audit log + journal
```

## Core Interpretation

1. Decision candidate is not a trade.
2. The deterministic quant engine may only produce a future candidate, not an executable order.
3. The verifier layer is the hard safety gate.
4. Human review / paper-trade gate must come before anything execution-like.
5. Audit log + journal must preserve provenance, checks, reasons, and outcomes.
6. No direct market-data-to-trade path is allowed.
7. No direct signal-to-trade path is allowed.
8. No LLM/autonomous model may bypass the verifier.
9. No strategy/backtest/recommendation output may become executable without future explicitly audited phases.
10. Execution APIs remain forbidden.

No trade commit path exists in the current system. No order route, broker
control, execution API, active DecisionObject generation, confidence scoring
engine, expected value engine, paper trading implementation, market-data
ingestion, strategy generation, backtesting engine, frontend UI, desktop UI,
journal database, or audit database is introduced by this document.
