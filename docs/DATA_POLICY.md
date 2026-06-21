# Data Policy

Stark Terminal will use a data-provider adapter architecture. Provider-specific behavior must remain behind explicit adapters and typed contracts.

## Rules

- Do not hardcode fragile scraping as the foundation.
- Do not commit credentials.
- Do not expose raw database URLs, provider URLs with credentials, tokens, or secrets through API responses.
- Use local sample data only in early versions.
- Respect provider terms of service.
- Do not create scraping code that violates provider terms.
- Use migrations first for database schema changes.
- Do not add ingestion without a provider adapter contract and data-quality checks.
- Do not allow path traversal in research lake dataset names, versions, partitions, or manifest paths.
- Use temporary synthetic data for tests only.
- Do not check generated data files into the repository.
- Maintain timestamp consistency for operational time-series records; timestamps should be timezone-aware or normalized consistently to UTC.
- Do not create analytics-generated state without source data reference, model/rule version where applicable, and audit path.
- Do not use cache entries as durable truth; Redis cache is only a short-lived acceleration layer.
- Do not put secrets, credentials, tokens, raw URLs, or provider credentials in cache keys.
- Cache entries should have explicit TTLs or use the configured default TTL.
- Do not use Redis Streams as durable truth; streams coordinate events only.
- Do not put secrets, credentials, tokens, raw URLs, API keys, database URLs, Redis URLs, or broker tokens in event payloads.
- Every event payload must use a declared schema version.
- Do not use Kafka/Redpanda events as durable truth; the event backbone coordinates replayable events only.
- Do not put secrets, credentials, tokens, raw URLs, API keys, database URLs, Redis URLs, ClickHouse URLs, Kafka bootstrap servers, broker tokens, or broker secrets in durable event payloads.
- Kafka/Redpanda topic names must be deterministic, namespaced, and free of secrets, URLs, path traversal, or execution/order/broker/live-trading concepts.
- Do not use worker jobs as durable truth; workers coordinate typed jobs only.
- Do not put secrets, credentials, tokens, raw URLs, API keys, database URLs, Redis URLs, broker tokens, or broker secrets in job payloads.
- Every job payload must use a declared schema version.
- Use stable instrument identifiers in `EXCHANGE:SYMBOL:SEGMENT` format.
- Do not scrape NSE/BSE or call external providers in Prompt 08.
- Do not commit provider credentials, broker credentials, tokens, API keys, raw provider URLs, or SDK secrets.
- Provider adapters must be read-only and must respect provider terms.
- Do not add market data ingestion without an explicit implementation prompt, adapter contract, data-quality checks, and audit/source reference policy.
- Do not put secrets, credentials, tokens, raw URLs, ClickHouse users, ClickHouse passwords, provider credentials, or broker credentials in warehouse queries.
- Do not create ClickHouse tables automatically from imports, health checks, API routes, or app startup.
- Do not let analytical warehouse outputs become trade calls.
- Keep operational, research, and analytical stores distinct: TimescaleDB for operational time-series, DuckDB/Parquet for research lake, ClickHouse for analytical warehouse.
- Do not use features as trade calls.
- Do not compute features without an explicit future prompt.
- Feature definitions must include source reference expectations, lineage expectations, freshness/staleness metadata, and quality requirements.
- Feature snapshots must eventually carry source data references, quality reports, and lineage records before being used as decision evidence.
- Validate data contracts before ingestion, analytics, feature computation, backtests, or decision-support use.
- Validation reports must include stable issue codes, severities, source references where required, schema version, and auditability.
- Timestamp quality checks must prefer timezone-aware UTC timestamps.
- Validation failure must never silently pass.
- Do not use validation results or quality gates as trade calls, signals, order instructions, or execution approvals.
- Prompt 13 performs no external validation and no production validation pipeline work.
- Synthetic fixtures must remain synthetic, local-only, and test/dev only.
- Do not check real production data or generated fixture datasets into the repository.
- Do not use sample data as a trade signal, analytics signal, recommendation, or decision.
- Synthetic fixture disk writes are disabled by default for the configured output root.
- Real ingestion requires provider adapter contracts, data-policy review, source references, and validation gates.
- Keep raw provider payloads separate from cleaned, normalized, feature-ready, backtest-ready, and research-artifact datasets.
- Every dataset should eventually be auditable and reproducible.

## Database Safety

PostgreSQL is the system of record. Prompt 02 adds metadata persistence only. Database schema changes must be reviewed, tested, and represented through Alembic migrations. Execution tables, broker credential tables, order placement tables, and hidden trading workflows remain forbidden.

## Operational Time-Series Safety

Prompt 03 adds operational time-series schemas only. It does not add market data ingestion, provider clients, live data loading, or analytics engines. Operational records must preserve source references, provider identity where available, timestamp consistency, and quality status. Raw/provider data separation remains mandatory.

## Research Lake Zone Policy

Prompt 04 adds DuckDB + Parquet research lake contracts only. Research lake datasets must stay in the correct zone: raw, cleaned, normalized, feature_ready, backtest_ready, or research_artifacts. Future datasets must include source reference, schema information, lineage, and audit context where applicable. No ingestion is allowed without provider adapter contracts and data-quality checks.

## Cache Safety

Prompt 05 adds Redis cache contracts only. Redis is not the source of truth for market data, decisions, research artifacts, audit records, or infrastructure state. Cache keys must be namespaced and must not contain secrets or raw URLs. Cache values should be JSON-serializable and short-lived. Redis Streams and event pipelines remain deferred.

## Event Payload Safety

Prompt 06 adds Redis Streams event pipeline contracts only. Event envelopes must include schema version, event type, source, stream, payload, and timestamp. Payloads must be JSON-serializable and must not include secrets, raw URLs, provider credentials, broker credentials, API keys, database URLs, Redis URLs, or broker tokens. Streams do not replace PostgreSQL as the system of record, and no market ingestion is allowed without provider adapter contracts and data-quality checks.

## Durable Event Backbone Safety

Prompt 12 adds Kafka/Redpanda Event Backbone contracts only. Durable event envelopes must include schema version, event type, source, topic, payload, and timestamp. Payloads must be JSON-serializable and must not include secrets, raw URLs, provider credentials, broker credentials, API keys, database URLs, Redis URLs, ClickHouse URLs, Kafka bootstrap servers, broker tokens, or broker secrets. Kafka/Redpanda is not durable truth; PostgreSQL remains system of record. No market ingestion is allowed without provider adapter contracts, data-quality checks, and audit/source reference policy.

## Job Payload Safety

Prompt 07 adds Worker System contracts only. Job envelopes must include schema version, worker role, job type, queue, payload, and timestamp. Job payloads must be JSON-serializable and must not include secrets, raw URLs, provider credentials, broker credentials, API keys, database URLs, Redis URLs, broker tokens, or broker secrets. Workers do not replace PostgreSQL as the system of record. No market ingestion is allowed without provider adapter contracts and data-quality checks.

## Instrument Master And Provider Policy

Prompt 08 adds Instrument Master and Market Data Provider contracts only. Synthetic/local fixtures are for deterministic tests and local contract checks; they are not live data. Provider adapters are read-only. External calls, scraping, NSE/BSE loading, provider SDKs, credentials, broker integrations, and execution APIs are not implemented. Every future dataset must include provider identity, source reference, schema version, quality status, timestamp consistency, and auditability where applicable.

## Analytical Warehouse Policy

Prompt 09 adds ClickHouse analytical warehouse contracts only. DDL helpers return SQL strings and do not execute table creation. The memory query recorder is local/test-only. Analytical warehouse queries must not contain secrets and must not create trade calls. Real analytical ingestion requires a future explicit prompt, provider adapter contracts, quality checks, and source/audit references.

## Feature Governance Policy

Prompt 10 adds the custom Stark Feature Registry foundation only. It stores metadata contracts in memory for tests/local use and does not compute real features. Feature definitions, snapshots, quality reports, and lineage records must be auditable. No feature may represent execution, order placement, broker credentials, live trading triggers, or real-money routing. Feature quality reports and lineage are required by default before future feature values can become decision or model evidence.

## Data Quality Policy

Prompt 13 adds the Data Quality + Validation Framework only. Validators are deterministic, local, and side-effect free. They do not make provider calls, call external services, mutate durable state, ingest real market data, compute indicators, produce analytics signals, compute features, train models, or enable execution APIs.

Future ingestion, feature, backtest, warehouse, research lake, and decision-support workflows must pass explicit validation rules and quality gates before promotion. Source references are required by default. Timestamp validation requires timezone-aware timestamps by default. Quality gates are conservative and may ALLOW, WARN, or BLOCK, but no quality gate can authorize execution or trading.

## Synthetic Fixture Policy

Prompt 14 adds Synthetic Market Data Fixtures only. Fixtures are synthetic, local-only, test/dev only, not real market data, not trading data, not investment advice, and have no external provider source.

Fixture helpers may generate tiny deterministic OHLCV bars and MarketDataBatch objects for tests. They must use explicit seeds, UTC timestamps, `LOCAL_SAMPLE` provider metadata, synthetic source data references, and Data Quality Framework validation. They must not scrape NSE/BSE, call provider APIs, publish events, write production datasets, compute indicators, compute features, backtest strategies, generate decisions, or expose execution APIs.

## Prompt 11 Data Audit

Prompt 12 confirms no real market ingestion exists yet. Future market data ingestion requires a provider-specific implementation prompt, data-policy review, read-only provider adapter contract, source reference policy, quality checks, and audit path. no execution APIs and broker integrations remain forbidden.

## Planned Data Zones

- `raw`
- `cleaned`
- `normalized`
- `feature-ready`
- `backtest-ready`
- `research-artifacts`

## Reproducibility Expectations

Datasets should eventually include source references, ingestion timestamps, provider identifiers, schema versions, quality checks, transformation versions, and deterministic partitioning where practical.

## Prompt 15 Instrument Metadata Persistence Policy

Instrument metadata persistence is allowed for canonical `Instrument` records only. Repositories and services must not fetch real market data, call external providers, scrape NSE/BSE, persist OHLCV bars, publish events, compute signals, or expose execution APIs.

Instrument metadata writes require validation-before-persistence by default. Synthetic fixture seeding is local/test/dev only and must remain clearly synthetic. Repository and service errors must not expose database URLs, credentials, provider secrets, broker secrets, tokens, or API keys.

## Prompt 16 Batch Metadata Persistence Policy

Market Data Batch Persistence records batch metadata only. The persistence layer may store `batch_id`, instrument identity, timeframe, provider identity, row count, start/end timestamps, quality status, `source_data_reference`, synthetic flag, `fixture_id`, `dataset_manifest_id`, and `validation_report_id`.

The metadata table must store no full OHLCV bars, no tick history, no provider payloads, no options payloads, no secrets, no broker data, no order data, no trading signals, and no recommendations. Batch metadata is not a trade signal and must not become an execution gate.

Validation-before-persistence is required by default. Synthetic batch metadata is allowed only for local/test/dev use and must use a synthetic/local/test source reference. Repositories and services must make no external calls and must not perform real market ingestion. Future real ingestion requires provider adapters, source references, data quality gates, data-policy review, and an explicit future prompt.
