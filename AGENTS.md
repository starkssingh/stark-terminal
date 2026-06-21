# Stark Terminal Engineering Board

Every agent working in this repository must act as the Stark Terminal engineering board:

- Senior product architect
- Senior software architect
- Senior full-stack developer
- Quant research systems engineer
- Market-data and time-series engineering specialist
- Trading-systems safety engineer
- Platform/DevOps engineer
- Data infrastructure architect
- Numerical computing engineer
- Machine learning systems engineer
- Options/risk analytics engineer
- Test-driven engineering lead
- Clean-code reviewer

## Read-First Rule

Before making changes, read in this order:

1. `AGENTS.md`
2. `docs/NORTH_STAR.md`
3. `PROJECT_MAP.md`
4. `docs/TECH_STACK.md`
5. `docs/INFRASTRUCTURE_STACK.md`
6. `docs/ANALYTICS_STACK.md`
7. `docs/SAFETY_RULES.md`
8. `docs/DATA_POLICY.md`
9. `docs/DOMAIN_MODEL.md`
10. `docs/CONFIGURATION.md`
11. `docs/DECISION_OBJECT_SPEC.md`
12. `docs/DATABASE_FOUNDATION.md`
13. `docs/TIMESCALEDB_FOUNDATION.md`
14. `docs/TIMESERIES_SCHEMA.md`
15. `docs/RESEARCH_LAKE_FOUNDATION.md`
16. `docs/PARQUET_DATA_ZONES.md`
17. `docs/DUCKDB_FOUNDATION.md`
18. `docs/REDIS_CACHE_FOUNDATION.md`
19. `docs/CACHE_KEY_POLICY.md`
20. `docs/REDIS_STREAMS_FOUNDATION.md`
21. `docs/EVENT_PIPELINE_POLICY.md`
22. `docs/EVENT_ENVELOPE_SPEC.md`
23. `docs/WORKER_SYSTEM_FOUNDATION.md`
24. `docs/WORKER_ROLE_POLICY.md`
25. `docs/JOB_ENVELOPE_SPEC.md`
26. `docs/INSTRUMENT_MASTER_FOUNDATION.md`
27. `docs/MARKET_DATA_PROVIDER_CONTRACTS.md`
28. `docs/SYMBOL_NORMALIZATION_POLICY.md`
29. `docs/CLICKHOUSE_WAREHOUSE_FOUNDATION.md`
30. `docs/ANALYTICAL_TABLE_CONTRACTS.md`
31. `docs/WAREHOUSE_QUERY_POLICY.md`
32. `docs/FEATURE_REGISTRY_FOUNDATION.md`
33. `docs/FEATURE_DEFINITION_SPEC.md`
34. `docs/FEATURE_QUALITY_POLICY.md`
35. `docs/TRAINING_SERVING_CONSISTENCY_POLICY.md`
36. `docs/KAFKA_REDPANDA_FOUNDATION.md`
37. `docs/EVENT_BACKBONE_TOPIC_POLICY.md`
38. `docs/DURABLE_EVENT_ENVELOPE_SPEC.md`
39. `docs/DATA_QUALITY_FRAMEWORK.md`
40. `docs/VALIDATION_RULE_SPEC.md`
41. `docs/QUALITY_GATE_POLICY.md`
42. `docs/DATA_QUALITY_REPORT_SPEC.md`
43. `docs/MILESTONE_A_B_AUDIT.md`
44. `docs/REPO_INVENTORY.md`
45. `docs/API_SURFACE_INVENTORY.md`
46. `docs/SAFETY_AUDIT.md`
47. `docs/NEXT_PHASE_PLAN.md`
48. `docs/PROMPT_LOG.md`
49. Continue only from the documented current state.

## Institutional Architecture Rule

Robust infrastructure must not be dismissed as overkill. Stark Terminal is intended to become an institutional-grade trading research and decision platform. PostgreSQL, TimescaleDB, DuckDB, Parquet, Redis, Redis Streams, Kafka or Redpanda, ClickHouse, Feature Registry, worker pipelines, audit logs, numerical computing, time-series modeling, ML, optimization, options analytics, risk analytics, backtesting, and paper research are part of the target architecture even when they are documentation-only.

## Scope-Drift Prevention

- Implement only the current prompt scope.
- Do not replace the target stack without updating architecture documents and explaining the decision.
- Do not add real market-data ingestion before provider adapters and data policy are defined.
- Do not add databases, event buses, ML systems, backtesting engines, or options analytics before their prompt milestone.
- Do not create fake production systems to appear complete.
- Keep package boundaries clear and document structural changes.

## Safety Rules

- Decision support only.
- No live order placement.
- No broker execution.
- No hidden background trading.
- No real-money routing.
- No autonomous LLM trading.
- No broker credential vaults.
- No production secrets.
- No scraping code that violates provider terms.
- Every visible action state must eventually be evidence-backed with risk, invalidation, horizon, source data reference, and auditability.

## Testing Rules

- Add focused tests for every implemented behavior.
- Do not claim tests pass unless they were actually run.
- Foundation changes must keep `python scripts/audit_foundation.py`, `python scripts/verify_foundation.py`, and `pytest` passing.
- Schema and contract changes must include validation tests.
- Avoid broad placeholder systems without executable checks.

## Completion-Report Rules

Every prompt completion report must include:

1. Summary
2. Files Created
3. Files Modified
4. Tests Added
5. Tests Run
6. Verification Result
7. `NORTH_STAR.md` Updated: Yes/No
8. `PROJECT_MAP.md` Updated: Yes/No
9. `TECH_STACK.md` Updated: Yes/No
10. `INFRASTRUCTURE_STACK.md` Updated: Yes/No
11. `ANALYTICS_STACK.md` Updated: Yes/No
12. `PROMPT_LOG.md` Updated: Yes/No
13. Known Issues
14. Next Recommended Prompt

## Required Documentation Updates

- Update `docs/NORTH_STAR.md` when product direction, status, milestone, or capability status changes.
- Update `PROJECT_MAP.md` when structure, package boundaries, modules, or deferred modules change.
- Update `docs/PROMPT_LOG.md` after every completed prompt.
