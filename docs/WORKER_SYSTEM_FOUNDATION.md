# Worker System Foundation

The Worker System Foundation defines Stark Terminal's typed worker lifecycle contracts. It prepares the platform for future orchestration without starting real production workers.

Prompt 07 implements:

- Worker role contracts.
- JobEnvelope schema.
- WorkerResult schema.
- Base worker lifecycle abstraction.
- Worker registry.
- Deterministic in-process worker harness.
- Safe no-op, echo, and failing workers for tests/local harness checks.
- Worker health checks.
- `GET /workers/health`.

## Scope Boundary

Prompt 07 does not implement real production worker loops, market data ingestion, provider clients, analytics engines, option pricing, backtesting, regime detection, Paper Lab logic, broker integrations, or execution APIs.

The in-process harness is local/test-only. It does not create background threads, processes, schedulers, daemons, or infinite loops. Redis Streams future wiring is planned, but Prompt 07 does not connect stream events to real workers.

## Future Worker Roles

- `ingestion_worker`
- `normalization_worker`
- `feature_worker`
- `regime_worker`
- `options_worker`
- `risk_worker`
- `decision_worker`
- `backtest_worker`
- `paper_lab_worker`
- `audit_worker`
- `system_health_worker`

These roles are orchestration placeholders only in Prompt 07.

## Safety

Workers must never bypass the Stark Terminal safety exclusions. Execution workers, order placement workers, broker credential workers, live trading workers, and hidden trading workflows are forbidden.

## Next Step

Prompt 08 should implement Instrument Master + Market Data Contracts: instrument master contracts, exchange/segment symbol normalization, instrument universe registry, and market data provider adapter interfaces, with no real provider ingestion and no execution APIs.
