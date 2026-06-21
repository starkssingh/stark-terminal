# Worker Role Policy

Worker roles define future orchestration responsibilities. They do not implement production workflows in Prompt 07.

## Allowed Roles

- `INGESTION_WORKER`: Future ingestion orchestration placeholder.
- `NORMALIZATION_WORKER`: Future normalization orchestration placeholder.
- `FEATURE_WORKER`: Future feature computation orchestration placeholder.
- `REGIME_WORKER`: Future regime update orchestration placeholder.
- `OPTIONS_WORKER`: Future options update orchestration placeholder.
- `RISK_WORKER`: Future risk update orchestration placeholder.
- `DECISION_WORKER`: Future decision generation orchestration placeholder.
- `BACKTEST_WORKER`: Future backtest orchestration placeholder.
- `PAPER_LAB_WORKER`: Future Paper Lab orchestration placeholder.
- `AUDIT_WORKER`: Future audit orchestration placeholder.
- `SYSTEM_HEALTH_WORKER`: Future system health orchestration placeholder.
- `TEST_WORKER`: Local/test worker role.

## Queue Mapping

The default queue mapping is deterministic: lower-case role value, such as `feature_worker` or `system_health_worker`.

## Forbidden Worker Types

The following worker types are forbidden:

- Execution worker.
- Order placement worker.
- Broker credential worker.
- Live trading worker.
- Real-money routing worker.

No worker may bypass safety exclusions. Workers must be deterministic and testable before any production deployment.

