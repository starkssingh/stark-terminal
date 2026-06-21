# Feature Registry Foundation

The Stark Feature Registry is the feature governance foundation for Stark Terminal. It defines metadata contracts for future feature definitions, feature sets, feature values, feature snapshots, quality reports, and lineage records.

## Purpose

The registry exists to keep future analytics, regime, decision, backtest, and model workflows reproducible. It records what a feature means, who owns it, which entities it belongs to, which upstream data it depends on, how fresh it is allowed to be, and which quality and lineage records must accompany it.

## Custom Registry First

Prompt 10 implements a custom Stark Feature Registry first. Feast planned support remains a future option, not a Prompt 10 dependency. Feast is not installed, configured, or integrated in Prompt 10.

## Prompt 10 Scope

Prompt 10 implements:

- Feature Registry settings.
- FeatureDefinition and FeatureDependency contracts.
- FeatureSet contracts.
- FeatureEntity, FeatureValue, and FeatureSnapshot contracts.
- FeatureQualityReport contracts.
- FeatureLineageRecord contracts.
- In-memory StarkFeatureRegistry.
- Feature registry health checks.
- API feature registry health and contract endpoints.

Prompt 10 does not compute features, implement indicators, train ML models, ingest market data, implement production feature pipelines, integrate Feast, connect to external services, or expose execution APIs.

## Store Relationships

Future features may reference:

- PostgreSQL for durable metadata and audit state.
- TimescaleDB for operational time-series inputs.
- DuckDB and Parquet for research lake and offline datasets.
- ClickHouse for analytical warehouse scans.
- Redis/Redis Streams for short-lived state and coordination only.

The registry itself is metadata/governance foundation in Prompt 10. It is not a computation engine and is not a source of live trading signals.

## Safety Boundary

Feature definitions must not represent execution, order placement, broker credentials, live trading triggers, or real-money routing. Features may support future decision support only after explicit computation, source, quality, lineage, and validation prompts.

## Next Step

Prompt 11 should perform a Milestone A/B Infrastructure Audit and Consolidation unless the roadmap is updated through documented architecture review.

