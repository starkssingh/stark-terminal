# Safety Rules

Stark Terminal is decision support only.

## Hard Prohibitions

- No live orders.
- No broker execution.
- No hidden trading.
- No real-money routing.
- No autonomous trading.
- No broker credential vaults.
- No production secrets.
- No high-frequency trading execution systems.
- No payment systems.

## Decision Safety

- All action states must be evidence-backed.
- User-facing outputs must include risk and invalidation in later versions.
- Advanced analytics must not create unverified trade calls.
- ML models must not be treated as authoritative without validation.
- DecisionObject records must eventually include source data references, model or rule versions, generated timestamps, and audit IDs.

## Research Safety

- Research outputs are candidates, not instructions.
- Backtests must include assumptions and limitations.
- Strategies must be validated before being promoted as decision evidence.
- Paper-to-strategy workflows must generate reviewable StrategyCandidate objects, not executable trading systems.

## Milestone Audit Safety Rule

Prompt 11 confirms execution APIs remain forbidden. Future milestone audits must search for execution, broker, order, live-trading, real-money routing, broker credential, autonomous trading, and hidden background trading concepts in code, routes, worker roles, provider contracts, settings, docs, and tests.

The current foundation has no execution APIs, no broker execution, no real market ingestion, no external provider calls, no production Kafka/Redpanda pipelines, no production validation pipelines, and no analytics signals.
