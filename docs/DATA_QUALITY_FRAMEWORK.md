# Data Quality Framework

The Data Quality + Validation Framework is Stark Terminal's deterministic validation foundation. It gives future ingestion, feature, research, warehouse, backtest, and decision-support systems a shared way to validate local contracts before data moves farther into the platform.

## Prompt 13 Scope

Prompt 13 implements:

- data quality settings
- validation issue, rule, result, and validation report contracts
- quality gate policy and result contracts
- deterministic validator base interface
- built-in validators for current local contracts
- validation registry
- data quality health checks
- `GET /data-quality/health`
- read-only `GET /data-quality/contracts`

Prompt 13 does not implement real market data ingestion, provider network calls, production validation pipelines, analytics engines, indicators, feature computation, ML models, signals, recommendations, broker integrations, or execution APIs.

## Deterministic Validators

Validators are local, deterministic, and side-effect free. They do not call PostgreSQL, TimescaleDB, DuckDB, ClickHouse, Redis, Redis Streams, Kafka/Redpanda, provider APIs, cloud services, brokers, or external validation engines. Expected validation failures become auditable validation reports instead of unhandled crashes.

Built-in validators cover the existing local contracts:

- Instrument
- InstrumentUniverseSnapshot
- MarketDataBar
- MarketDataRequest
- MarketDataResponse
- OptionsChainSnapshot
- DatasetManifest
- FeatureSnapshot
- FeatureQualityReport
- WarehouseTableContract

## Validation Registry

The validation registry is explicit and in-memory for Prompt 13. It maps validation scopes to validators and can infer scope from supported local contract types. It is not global durable state and does not persist reports.

## Quality Gates

Quality gates evaluate validation reports against explicit policies. Gates can ALLOW, WARN, or BLOCK. They are conservative by default, and validation failure must never silently pass. Quality gates may later protect ingestion, features, backtests, and decision-support workflows, but no quality gate can enable execution APIs.

## Infrastructure Relationship

PostgreSQL remains system of record. TimescaleDB remains the operational time-series target. DuckDB/Parquet remains the research lake. ClickHouse remains the analytical warehouse. Feature Registry remains governance. Redis Streams and Kafka/Redpanda remain event foundations. The Data Quality Framework validates contracts across these layers before future data movement, but it does not ingest, store, publish, or compute real data.

Development environment remains Mac mini M2 / macOS / Apple Silicon. Target desktop product remains Windows-native Stark Terminal.
