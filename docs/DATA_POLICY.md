# Data Policy

Stark Terminal will use a data-provider adapter architecture. Provider-specific behavior must remain behind explicit adapters and typed contracts.

## Prompt 107 Retail Decision Console Internal Preview Closure Data Policy

Retail Decision Console internal preview milestone closure does not certify
live data, recommendation, confidence, trading, broker, order, or execution
readiness. Internal preview artifacts remain local/demo/static/unavailable
and must not be treated as live market intelligence, validated research,
recommendations, action states, confidence scores, active DecisionObjects,
broker controls, order controls, or execution data.

Internal preview artifacts must not be used for trading decisions. Commit/push
after closure preserves a local internal preview milestone only, not a
production release or trading-ready release.

## Prompt 106 Retail Decision Console Internal Preview Smoke Data Policy

Retail Decision Console internal preview smoke verification does not certify
live data, recommendation, confidence, trading, broker, order, or execution
readiness. Smoke verification may inspect local internal preview artifacts
only and must not treat package artifacts as live market intelligence,
validated recommendations, action states, confidence scores, active
DecisionObjects, broker controls, order controls, or execution data.

## Prompt 105 Retail Decision Console Internal Preview Package Data Policy

Retail Decision Console internal preview packages must be marked demo, static,
local-only, read-only, unavailable, not production ready, not trading ready,
not recommendation ready, and not execution ready. Generated internal preview
artifacts must not contain secrets, credentials, live market data,
recommendations, action states, confidence scores, active DecisionObjects,
broker controls, order controls, or execution data.

Sharing internal preview packages does not imply production readiness, trading
readiness, recommendation readiness, confidence readiness, DecisionObject
readiness, broker readiness, order readiness, or execution readiness.

## Prompt 104 Retail Decision Console Manual Acceptance Data Policy

Retail Decision Console manual acceptance cannot certify live data,
recommendation, strategy, confidence, DecisionObject, broker, order, or
execution readiness. Acceptance artifacts remain local, demo/static,
unavailable, and read-only unless explicitly promoted in a later safe release
phase.

Manual acceptance artifacts must not contain secrets, credentials, live market
data, recommendations, action states, confidence scores, active
DecisionObjects, broker controls, order controls, or execution data.

## Prompt 103 Retail Decision Console Local QA Bundle Data Policy

Retail Decision Console local QA bundles must be marked demo, static,
local-only, read-only, and unavailable. Generated QA artifacts must not
contain secrets, credentials, live market data, recommendations, action
states, confidence scores, active DecisionObjects, broker controls, order
controls, or execution data.

Generated QA artifacts remain local-only unless manually shared. A QA bundle
must not turn static shell state into market intelligence, validated
research, a confidence report, a DecisionObject, a broker/order artifact, or
an execution artifact.

## Prompt 102 Retail Decision Console Preview Snapshot Data Policy

Retail Decision Console preview snapshots must be marked demo, static, local,
read-only, and unavailable. They must not contain secrets, credentials, live
market data, recommendations, action states, confidence scores, active
DecisionObjects, broker controls, order controls, or execution data.

Preview snapshot export must not turn static shell state into market
intelligence, validated research, a confidence report, a DecisionObject, or
an execution artifact.

## Prompt 101 Retail Decision Console Static Interaction Data Policy

Retail Decision Console static interactions must not trigger live data,
recommendation generation, action generation, confidence scoring,
DecisionObject generation, broker controls, order controls, or execution.

Local placeholder refresh must not fetch, infer, validate, rank, recommend, or
transform market data. Static instrument/timeframe placeholder selection must
remain local, demo-only, unavailable, and non-executive.

## Prompt 100 Retail Decision Console Visual Layout Data Policy

Retail Decision Console visual polish must not make demo/static state appear
live, validated, actionable, or executable. All display zones must preserve
demo/unavailable provenance and false dangerous flags.

The visual layout pass must not create data-to-recommendation,
data-to-confidence, data-to-DecisionObject, broker-control, order-button, or
execution paths.

## Prompt 99 Retail Decision Console Local Preview Data Policy

Retail Decision Console local preview must not require credentials, provider
setup, broker setup, live market data, or an API server. Preview state must
remain demo, static, unavailable, and read-only.

The preview must not treat local/static placeholders as live market
intelligence, validated research, recommendations, action states, confidence
scores, active DecisionObjects, broker controls, order controls, or execution
readiness.

## Prompt 98 Retail Decision Console Static State Wiring Data Policy

Retail Decision Console state-to-view wiring must preserve demo/unavailable
provenance. The UI shell and static-state view-model must not present
demo/static placeholders as live market intelligence, validated research,
recommendations, action states, confidence scores, active DecisionObjects,
broker controls, order controls, or execution readiness.

Prompt 98 adds no data ingestion, data-to-recommendation,
data-to-confidence, data-to-DecisionObject, broker-control, order-button, or
execution path.

## Prompt 97 Retail Decision Console Demo Static State Data Policy

Retail Decision Console demo/static state must be labeled as demo,
static, and unavailable. It must not be treated as live market intelligence,
real instrument data, a recommendation, an action state, a confidence score,
an active DecisionObject, a broker control, an order control, or execution
readiness.

Any future Retail Decision Console display state must carry provenance,
source status, data-quality status, and demo/unavailable status before it can
move toward user-facing decision support. Prompt 97 adds no data-to-
recommendation, data-to-confidence, data-to-DecisionObject, broker-control,
order-button, or execution path.

## Prompt 96 Retail Decision Console UI Shell Data Policy

The Retail Decision Console UI shell must not present local, synthetic,
static, or placeholder data as live market intelligence. Every visible shell
state in Prompt 96 remains unavailable/demo/skeleton only.

Any future display state must carry source, provenance, demo/unavailable
status, and data-quality validation status before it can be treated as
decision-support content. Prompt 96 adds no data-to-recommendation,
data-to-confidence, data-to-DecisionObject, broker-control, order-button, or
execution path.

## Prompt 95 Retail Decision Console Data Policy

Retail Decision Console cannot treat synthetic or local data as live market
intelligence. Any future user-facing decision state must require data-quality,
provenance, and decision validation checks before it can move beyond
unavailable/demo/skeleton state.

The Retail Decision Console cannot create a data-to-recommendation,
data-to-confidence, data-to-DecisionObject, data-to-broker-control, or
data-to-execution bypass. No live market-data claims are allowed in the
Prompt 95 productization plan and UI shell boundary.

## Prompt 94 Product Surface Reorientation Data Policy

Product surfaces must not treat synthetic or local data as trusted live market
intelligence. User-facing decision surfaces must remain unavailable, demo-only,
or skeleton-only until data quality and decision validation are implemented.

No product surface may create a knowledge-map-to-product-action,
research-to-strategy, strategy-to-backtest, recommendation, confidence,
DecisionObject, broker-control, or execution bypass.

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

## Prompt 93 Research Knowledge Map Phase Closure Data Policy

Prompt 93 confirms these knowledge map phase-closure data rules:

- No knowledge-map-to-product-action bypass rule.
- No knowledge-map-to-strategy path.
- No knowledge-map-to-backtest path.
- No knowledge-map-to-recommendation path.
- No knowledge-map-to-execution path.
- No phase-closure bypass for active implementation, database, traversal,
  search, ranking, retrieval, embeddings, vector store, ingestion, storage,
  upload/download/preview, paper parsing, strategy generation, backtesting,
  recommendations, broker controls, or execution APIs.
- Planning/API/display placeholders remain descriptive contract metadata only.

## Prompt 92 Research Knowledge Map Safety Data Policy

Prompt 92 confirms these knowledge map safety audit rules:

- No knowledge-map safety audit as implementation bypass rule.
- No knowledge-map-to-strategy path.
- No knowledge-map-to-backtest path.
- No knowledge-map-to-recommendation path.
- No knowledge-map-to-execution path.
- No planning/API/display traversal/search/retrieval bypass rule.
- No database, table, migration, persistent write, embedding, vector-store,
  ingestion, storage, upload/download/preview, or paper-parsing bypass rule.
- Planning/API/display placeholders remain descriptive contract metadata only.

## Prompt 91 Research Knowledge Map Display Data Policy

Prompt 91 confirms these knowledge map display rules:

- No knowledge-map-display-to-strategy path.
- No knowledge-map-display-to-backtest path.
- No knowledge-map-display-to-recommendation path.
- No knowledge-map-display-to-execution path.
- No display-as-search/retrieval bypass rule.
- No display-as-trusted-source rule.
- No display active UI, frontend, desktop, database, persistent write,
  embedding, vector-store, ingestion, storage, upload/download/preview, or
  paper-parsing bypass rule.
- Display placeholders remain descriptive backend contract metadata only.

## Prompt 90 Research Knowledge Map API Data Policy

Prompt 90 confirms these knowledge map API rules:

- No knowledge-map-api-to-strategy path.
- No knowledge-map-api-to-backtest path.
- No knowledge-map-api-to-recommendation path.
- No knowledge-map-api-to-execution path.
- No API traversal/search/retrieval bypass rule.
- No API database, persistent write, embedding, vector-store, ingestion,
  storage, upload/download/preview, or paper-parsing bypass rule.
- API placeholders remain descriptive contract metadata only.

## Prompt 89 Research Knowledge Map Data Policy

Prompt 89 confirms these knowledge map planning rules:

- No knowledge-map-to-strategy path.
- No knowledge-map-to-backtest path.
- No knowledge-map-to-recommendation path.
- No knowledge-map-to-execution path.
- No knowledge map traversal/search/retrieval bypass rule.
- No knowledge map database, persistent write, embedding, vector-store,
  ingestion, storage, upload/download/preview, or paper-parsing bypass rule.
- Knowledge map placeholders remain descriptive planning metadata only.

## Prompt 88-B Research Metadata Graph Phase Closure Data Policy

Prompt 88-B confirms these metadata graph phase-closure rules:

- No metadata graph phase closure as implementation bypass rule.
- No metadata graph phase closure as graph database, traversal, search,
  ranking, retrieval, embedding, vector-store, ingestion, storage,
  upload/download/preview, or active UI bypass rule.
- No graph-to-strategy path.
- No graph-to-backtest path.
- No graph-to-recommendation path.
- No graph-to-execution path.
- Planning/API/display placeholders remain descriptive and unavailable by
  default where applicable.
- Research Knowledge Map Planning and Guardrails is the only next allowed
  phase.

## Prompt 87 Research Metadata Graph Safety Data Policy

Prompt 87 confirms these metadata graph safety rules:

- No metadata graph safety audit as implementation bypass rule.
- No metadata graph safety audit as graph database, traversal, search,
  ranking, retrieval, embedding, vector-store, ingestion, storage,
  upload/download/preview, or active UI bypass rule.
- No graph-to-strategy path.
- No graph-to-backtest path.
- No graph-to-recommendation path.
- No graph-to-execution path.
- Planning/API/display placeholders remain descriptive and unavailable by
  default where applicable.

## Prompt 86 Research Metadata Graph Display Data Policy

Prompt 86 confirms these metadata graph display rules:

- No graph display as implementation bypass rule.
- No graph display as active UI, frontend, or desktop bypass rule.
- No graph display traversal/search/retrieval bypass rule.
- No graph display ranking or scoring bypass rule.
- No graph display embedding/vector-store bypass rule.
- No graph display ingestion/storage/upload/download/preview bypass rule.
- No graph display paper parsing, PDF parsing, arXiv ingestion, or LLM paper
  analysis.
- No graph display as trusted source rule.
- No graph display to strategy path.
- No graph display to backtest path.
- No graph display to recommendation path.
- No graph display to execution path.

## Prompt 85 Research Metadata Graph API Data Policy

Prompt 85 confirms these metadata graph API rules:

- No graph API as implementation bypass rule.
- No graph API traversal/search/retrieval bypass rule.
- No graph API ranking or scoring bypass rule.
- No graph API embedding/vector-store bypass rule.
- No graph API ingestion/storage/upload/download/preview bypass rule.
- No graph API paper parsing, PDF parsing, arXiv ingestion, or LLM paper
  analysis.
- No graph API to strategy path.
- No graph API to backtest path.
- No graph API to recommendation path.
- No graph API to execution path.

## Prompt 84 Research Metadata Graph Planning Data Policy

Prompt 84 confirms these metadata graph rules:

- No metadata graph implementation before API, display, safety, and milestone
  audit phases.
- No active graph database.
- No persistent graph writes.
- No graph storage tables or graph migrations.
- No graph traversal/search/retrieval bypass rule.
- No graph ranking or scoring bypass rule.
- No embedding/vector-store bypass rule.
- No active graph ingestion or active graph storage.
- No file upload/download/preview bypass rule.
- No paper parsing, PDF parsing, arXiv ingestion, or LLM paper analysis.
- No graph-to-strategy path.
- No graph-to-backtest path.
- No graph-to-recommendation path.
- No graph-to-execution path.

## Prompt 83 Research Artifact Index Integration Data Policy

Prompt 83 confirms these API/display integration rules:

- No API-to-display indexing/search/retrieval bypass rule.
- No display-as-graph-implementation rule.
- No artifact index placeholder may become a metadata graph implementation.
- No graph database, graph traversal, graph search, graph ranking, graph
  retrieval, embedding, vector-store, ingestion, storage, upload/download/
  preview, parsing, strategy, backtest, recommendation, or execution path is
  allowed before future explicit audited phases.
- No artifact-to-strategy rule.
- No artifact-to-backtest rule.
- No artifact-to-recommendation rule.
- No artifact-to-execution rule.

## Prompt 81 Research Artifact Index Milestone Audit Confirmation

Prompt 81 confirms these Research Artifact Index data policy rules:

- No artifact-index-to-graph implementation before planning/guardrails rule:
  Research Metadata Graph work must start with planning and guardrails only.
- No index ingestion/storage bypass rule.
- No index upload/download/preview bypass rule.
- No index/search/ranking/retrieval bypass rule.
- No embedding/vector-store bypass rule.
- No artifact-index-to-strategy rule.
- No artifact-index-to-backtest rule.
- No artifact-index-to-recommendation rule.
- No artifact-index-to-execution rule.
- Index placeholders must not be treated as trusted real market data.

## Prompt 82 Research Artifact Index Boundary Bypass Rules

Prompt 82 confirms the Research Artifact Index boundary layer is a safety and
control layer only. It must not become an implementation bypass.

- No artifact index boundary bypass for active UI, frontend, or desktop.
- No artifact index boundary bypass for indexing/search/ranking/retrieval.
- No artifact index boundary bypass for embeddings/vector store.
- No artifact index boundary bypass for active ingestion or persistent storage.
- No artifact index boundary bypass for file upload/download/preview.
- No artifact index boundary bypass for paper parsing, PDF parsing, arXiv
  ingestion, LLM paper analysis, method extraction, or strategy extraction.
- No artifact-index-to-strategy rule.
- No artifact-index-to-backtest rule.
- No artifact-index-to-recommendation rule.
- No artifact-index-to-execution rule.

## Prompt 80 Research Artifact Index Safety Audit Confirmation

Prompt 80 adds these Research Artifact Index safety audit data policy rules:

- No index ingestion/storage bypass rule: index placeholders must not ingest,
  persist, or store artifact content.
- No index upload/download/preview bypass rule: index/API/display placeholders
  must not accept file bytes, download files, or preview file content.
- No index/search/ranking/retrieval bypass rule: metadata, keys, references,
  tags, provenance, lifecycle, API responses, and display placeholders must
  not become indexing, search, ranking, retrieval, lookup, or source lookup
  behavior.
- No embedding/vector-store bypass rule: index records must not create
  embeddings, vector IDs, vector databases, semantic vector search, or vector
  store dependencies.
- No index display preview rule: display placeholders must not render file
  previews, indexed records, search results, ranking results, retrieval
  results, embedding/vector displays, parsed papers, generated strategies,
  backtest results, recommendations, broker controls, or execution controls.
- No artifact-to-strategy rule.
- No artifact-to-backtest rule.
- No artifact-to-recommendation rule.
- No artifact-to-execution rule.
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

## Prompt 17 Data Foundation Audit Confirmation

Prompt 17 confirms Prompts 14-16 remain synthetic/metadata-only. The current data foundation persists instrument metadata and market data batch metadata only. It does not persist real market data, full OHLCV production bars, provider-ingested datasets, strategy outputs, trading decisions, recommendations, or signals.

Persistence boundaries remain:

- PostgreSQL stores metadata/system-of-record records.
- TimescaleDB will own future operational OHLCV/time-series storage.
- DuckDB/Parquet will own future research datasets.
- ClickHouse will own future analytical warehouse copies.
- Redis remains cache only.
- Redis Streams and Kafka/Redpanda remain event coordination/backbone contracts only.

No store currently receives real market data. Prompt 18 TimescaleDB synthetic OHLCV storage must remain synthetic-only until real ingestion is separately approved through provider adapter guardrails, validation gates, source reference policy, and data-policy review.

## Prompt 18 Synthetic OHLCV Storage Policy

Synthetic-only OHLCV storage is allowed for local/test/dev workflows through `SyntheticOHLCVStorageService`. Every stored bar must carry a synthetic/local/test `source_data_reference`, `LOCAL_SAMPLE` provider identity where practical, UTC timestamps, quality status, and instrument/timeframe/timestamp identity.

Validation-before-storage is required. Invalid bars, non-synthetic source references, real/provider-source claims, and non-local sample providers must be blocked before storage. The service must not silently pass validation failures.

Prompt 18 stores no real bars and performs no real market ingestion. It makes no external calls, publishes no Redis/Kafka events, writes no ClickHouse or DuckDB/Parquet production stores, computes no analytics/signals/features, generates no decisions, and exposes no execution APIs. Synthetic stored bars are not trading data, not investment advice, and not a trade signal.

## Prompt 19 Synthetic OHLCV Export Policy

Synthetic-only OHLCV export is allowed for local/test/dev workflows through `SyntheticOHLCVResearchLakeExportService`. Every export must use a synthetic/local/test `source_data_reference`, create a DatasetManifest, preserve row count and schema metadata, and write only when an explicit safe output path is provided.

Validation-before-export is required by default. Invalid bars, non-synthetic source references, real/provider-source claims, and rows beyond the configured limit must be blocked before export.

Prompt 19 exports no real bars and performs no real market ingestion. It makes no external calls, performs no scraping, writes no production research lake data by default, publishes no Redis/Kafka events, writes no ClickHouse, computes no analytics/signals/features, generates no decisions, and exposes no execution APIs. Exported synthetic datasets are not trading data, not investment advice, and not trade signals.

## Prompt 20 Provider Guardrail Policy

Provider Adapter Guardrails are required before real provider implementation. Future provider work must have an approval workflow record, terms/compliance checklist, data quality plan, audit logging plan, source reference policy, and explicit future implementation prompt before any real ingestion can occur.

Default provider policy:

- no network calls by default.
- no scraping by default.
- no credentials in the repository.
- no provider SDKs in Prompt 20.
- no real market ingestion.
- no external provider calls.
- no execution APIs through providers.
- no broker execution adapters, order placement providers, credential vaults, live trading, or real-money routing.

Provider test mode in the current phase can use synthetic/local fixtures only. Provider guardrails are governance contracts and cannot approve real market data ingestion, analytics signals, trading decisions, or execution behavior.

## Prompt 21 Local Sample Provider Policy

Local Sample Provider Adapter v0 is a safe provider adapter. It is synthetic, local-only, test/dev only, read-only, and guardrail-protected. It uses synthetic/local instruments and deterministic synthetic OHLCV generation only. Prompt 24 adds Local File Provider Adapter v0 as a second local/test/dev adapter.

Policy rules:

- no external calls.
- no scraping.
- no credentials.
- no provider SDKs.
- no real market data.
- no real market ingestion.
- no persistence writes from provider responses.
- no event publishing.
- no analytics signals, feature computation, decisions, recommendations, or backtests.
- no execution APIs, broker execution, order placement, live trading, or real-money routing.

Local sample provider responses must carry `LOCAL_SAMPLE` provider identity where practical and synthetic/local/test source references such as `synthetic-local-test-only`. They must never be presented as live, real, tradable, production, provider-sourced, or investment data.

## Prompt 22 Data Foundation Milestone Audit Confirmation

Prompt 22 confirms the Prompt 18-21 data foundation remains synthetic-only and governance-bounded.

Policy summary:

- synthetic OHLCV storage may store synthetic/local/test bars only after validation-before-storage.
- synthetic OHLCV export may write explicit safe/temp Parquet artifacts only after validation-before-export and DatasetManifest creation.
- provider guardrails must stay fail-closed for network calls, scraping, credentials, real ingestion, and execution.
- Local Sample Provider Adapter v0 remains synthetic/local/test-only, and Prompt 24 adds Local File Provider Adapter v0 as local-file/test/dev-only.
- API responses must not claim live or real market data.
- no real market ingestion is allowed.
- no external provider calls are allowed.
- no scraping is allowed.
- no credentials or provider SDKs are allowed.
- no analytics/signals/decisions may be produced from synthetic storage/export/provider responses.
- no execution APIs are allowed.

Real provider work remains forbidden until the real-provider readiness checklist and local-file provider phase are complete. Future real ingestion requires provider candidate review, terms/compliance review, data-policy review, source references, Data Quality gates, audit logging, and an explicit future implementation prompt.

## Prompt 23 Provider Readiness And Candidate Selection Policy

Prompt 23 adds Real Provider Readiness and Candidate Selection governance only. Provider candidate profiles, readiness checklists, selection criteria, risk scoring, capability gap analysis, and the in-memory candidate registry are metadata contracts.

Policy rules:

- no real provider implementation.
- no provider SDKs.
- no external calls.
- no scraping.
- no credentials.
- no credential vaults or secret injection.
- no real market ingestion.
- no production approval.
- no broker execution, order placement, live trading, or real-money routing.
- no analytics signals, feature computation, decisions, recommendations, or backtests.
- no execution APIs.

Candidate scores and shortlist decisions are pre-approval only. They cannot authorize provider integration, network tests, storage of real data, redistribution, production use, or trading interpretation.

Real provider implementation remains forbidden until provider readiness, approval workflow, compliance review, data-policy review, source reference policy, Data Quality gates, local-file provider testing, and an explicit future implementation prompt are complete.

## Prompt 24 Local File Provider Policy

Local File Provider Adapter v0 is allowed only for explicitly supplied local CSV/Parquet test/dev files. Local file inputs are not trusted real market data by default and must not be presented as live, provider-sourced, tradable, production, or investment data.

## Prompt 50 Retail Dashboard API Policy

Retail Dashboard API placeholders are unavailable by default and contract-only.

Policy rules:

- no dashboard API as recommendation.
- no dashboard API as execution control.
- no dashboard API live data claim.
- no dashboard API market-data input for decisions.
- no API placeholder as active UI.
- no API placeholder as DecisionObject display.
- no API placeholder as readiness-to-trade.
- no API reference as approval or override.

The Retail Dashboard API returns request/response/reference placeholders only.
It must not treat synthetic/local data as real market data and must not expose
broker controls, secrets, or execution APIs.

Policy rules:

- file paths must remain under the configured allowed root.
- path traversal must be rejected.
- network paths must be rejected.
- symlink escape must be rejected, and symlinks are disabled by default.
- only `.csv` and `.parquet` files are allowed.
- row count must respect the configured maximum.
- local file provider API endpoints must not expose arbitrary file read behavior or accept caller-supplied paths.
- Data Quality validation must run before successful provider responses where practical.
- no external calls.
- no scraping.
- no credentials.
- no provider SDKs.
- no real market ingestion.
- no persistence writes from provider responses.
- no event publishing.
- no analytics/signals/decisions.
- no execution APIs.

Local file provider work remains a local/test/dev provider-boundary exercise only. Real provider work still requires readiness review, terms/compliance review, data-policy review, source references, Data Quality gates, audit logging, and a future explicit implementation prompt.

## Prompt 25 Provider Adapter Milestone Audit Confirmation

Prompt 25 confirms the provider boundary after Prompts 20-24:

- Provider guardrails are fail-closed.
- Provider readiness and candidate selection are governance-only.
- Local Sample Provider remains synthetic/local/test-only.
- Local File Provider remains explicit local-file/test/dev-only with path safety and no arbitrary file read API.
- no real provider implementation exists.
- no production provider approval exists.
- no external calls are allowed.
- no scraping is allowed.
- no credentials or provider SDKs are allowed.
- no real market ingestion is allowed.
- no analytics/signals/decisions may be produced from provider responses.
- no execution APIs are allowed.

Real provider work remains forbidden until a future explicit prompt completes approval, terms/compliance review, data-policy review, source reference policy, Data Quality gates, and audit logging.

## Prompt 26 Analytics Foundation Policy

Prompt 26 adds Quant Analytics and Time-Series Analytics planning contracts only. Analytics is descriptive/research-only at this stage.

Policy rules:

- future analytics must require validated input data.
- future analytics must require source references.
- analytics outputs must be descriptive/research-only.
- analytics outputs must not be trade calls.
- indicators must not be treated as signals.
- no buy, sell, hold, watch, avoid, reduce, or action-state recommendations.
- no hidden decision logic.
- no execution APIs.
- no broker integration.
- no real market data assumption.
- no analytics calculations in Prompt 26.
- no heavy analytics dependency installation in Prompt 26.

Synthetic/local data can support deterministic tests, but it is not real market data, not provider-sourced production data, not trading data, not investment advice, and not decision evidence. Future analytics results require explicit prompt scope, validation gates, source references, documentation, and audit coverage before they can become evidence for any future Decision Desk workflow.

## Prompt 27 Numerical Analytics Policy

Prompt 27 adds Numerical Analytics Core Contracts. Numerical inputs must carry source references, remain synthetic/local/test-compatible in the current phase, and reject real market data claims.

Policy rules:

- numerical inputs must require source references.
- numerical vectors must require finite values by default.
- numerical outputs must be descriptive/research-only.
- numerical metrics must not become trade calls.
- count, min, max, and mean are generic descriptive summaries only.
- no returns, volatility, drawdown, correlation, beta, indicators, factors, or features in Prompt 27.
- no buy, sell, hold, watch, avoid, reduce, or action-state recommendations.
- no DecisionObject generation.
- no hidden decision logic.
- no execution APIs.
- no broker integration.
- no real market data assumption.
- no heavy analytics dependency installation in Prompt 27.

Future returns and rolling analytics must use validated inputs, source references, explicit docs, tests, and audit coverage before they can be added. Numerical metrics alone are not decision evidence, trading data, investment advice, or execution approval.

## Prompt 28 Returns and Rolling Analytics Policy

Prompt 28 adds Returns Analytics v0 and Rolling Window Analytics v0. Inputs must carry source references, remain synthetic/local/test-compatible in the current phase, and reject real market data claims.

Policy rules:

- returns and rolling inputs must require source references.
- price vectors must require finite values.
- positive prices are required by default and mandatory for log returns.
- rolling windows must be positive and bounded.
- returns outputs must be descriptive/research-only.
- rolling outputs must be descriptive/research-only.
- returns must not become trade calls.
- rolling metrics must not become signals.
- no volatility, drawdown, correlation, beta, indicators, factors, or features in Prompt 28.
- no buy, sell, hold, watch, avoid, reduce, or action-state recommendations.
- no DecisionObject generation.
- no hidden decision logic.
- no execution APIs.
- no broker integration.
- no real market data assumption.
- no heavy analytics dependency installation in Prompt 28.

Returns and rolling metrics are not decision evidence, trading data, investment advice, or execution approval.

## Prompt 29 Volatility and Drawdown Analytics Policy

Prompt 29 adds Volatility Analytics v0 and Drawdown Analytics v0. Inputs must carry source references, remain synthetic/local/test-compatible in the current phase, and reject real market data claims.

Policy rules:

- volatility inputs must require source references.
- return vectors must require finite values.
- annualized volatility requires explicit positive periods_per_year.
- drawdown inputs must require source references.
- drawdown value vectors must require finite and positive values by default.
- volatility outputs must be descriptive/research-only.
- drawdown outputs must be descriptive/research-only.
- volatility must not become a trade call.
- drawdown must not become a signal.
- risk metrics must not become recommendations.
- no correlation, beta, indicators, factors, or features in Prompt 29.
- no buy, sell, hold, watch, avoid, reduce, or action-state recommendations.
- no DecisionObject generation.
- no hidden decision logic.
- no execution APIs.
- no broker integration.
- no real market data assumption.
- no heavy analytics dependency installation in Prompt 29.

Volatility and drawdown metrics are not decision evidence, trading data, investment advice, or execution approval.

## Prompt 30 Analytics Milestone Policy

Prompt 30 audits the analytics milestone across Prompts 26-29. It confirms current analytics outputs are descriptive/research-only artifacts with source-reference and validation boundaries.

Policy rules:

- analytics outputs remain research-only until future decision-engine audit.
- no real market ingestion is available to analytics.
- no external calls are allowed from analytics modules.
- no heavy analytics dependencies are added by Prompt 30.
- no signals, recommendations, decisions, or DecisionObject generation.
- no buy/sell/hold/watch/avoid outputs.
- no hidden action-state or confidence trading logic.
- no execution APIs.
- no correlation, beta, indicators, backtests, regimes, ML models, or feature computation in Prompt 30.

Descriptive analytics metrics are not decision evidence, trading data, investment advice, recommendation payloads, or execution approval.

## Prompt 31 Correlation and Beta Analytics Policy

Prompt 31 adds Correlation Analytics v0 and Beta Analytics v0. Inputs must carry source references, remain synthetic/local/test-compatible in the current phase, and reject real market data claims.

Policy rules:

- correlation and beta inputs must require source references.
- paired vectors must require equal length.
- paired vectors must require finite values.
- paired vectors must satisfy the configured minimum observations.
- zero variance must fail safely.
- correlation outputs must be descriptive/research-only.
- beta outputs must be descriptive/research-only.
- correlation must not become a trade call.
- beta must not become a signal.
- relationship metrics must not become recommendations.
- no indicators, factors, features, backtests, or regimes in Prompt 31.
- no buy, sell, hold, watch, avoid, reduce, or action-state recommendations.
- no DecisionObject generation.
- no hidden decision logic.
- no execution APIs.
- no broker integration.
- no real market data assumption.
- no heavy analytics dependency installation in Prompt 31.

Correlation and beta metrics are not decision evidence, trading data, investment advice, or execution approval.

## Prompt 32 Time-Series Diagnostics Policy

Prompt 32 adds Time-Series Diagnostics Foundation. Inputs must carry source
references, remain synthetic/local/test-compatible in the current phase, reject
real market data claims, and use timezone-aware timestamps by default.

Policy rules:

- diagnostics inputs must require source references.
- timestamp series must require timezone-aware timestamps by default.
- real market data claims must be rejected.
- monotonicity diagnostics are descriptive/data-quality-only.
- duplicate timestamp diagnostics are descriptive/data-quality-only.
- gap diagnostics are descriptive/data-quality-only.
- irregular interval diagnostics are descriptive/data-quality-only.
- timestamp gaps must not become trade calls.
- diagnostics must not become recommendations.
- no stationarity tests in Prompt 32.
- no regime detection in Prompt 32.
- no indicators, factors, features, backtests, or regimes in Prompt 32.
- no buy, sell, hold, watch, avoid, reduce, or action-state recommendations.
- no DecisionObject generation.
- no hidden decision logic.
- no execution APIs.
- no broker integration.
- no real market data assumption.
- no heavy analytics dependency installation in Prompt 32.

Time-series diagnostics are not decision evidence, trading data, investment
advice, or execution approval.

## Prompt 33 Regime Analytics Planning Policy

Prompt 33 adds Regime Analytics Planning and Guardrails. Regime evidence
requirements must carry source-reference expectations, remain
synthetic/local/test-compatible in the current phase, and reject real market
data assumptions until a future provider phase is separately approved.

Policy rules:

- regime evidence must require source references.
- regime evidence must require validated inputs before future use.
- missing required evidence blocks readiness.
- human review is required.
- regime label placeholders must not be assigned in Prompt 33.
- regime readiness must not become a recommendation.
- regime labels must not become trade calls.
- no actual regime classification in Prompt 33.
- no stationarity tests, HMMs, clustering, or ML models in Prompt 33.
- no indicators, factors, features, backtests, or computed regimes in Prompt 33.
- no buy, sell, hold, watch, avoid, reduce, or action-state recommendations.
- no DecisionObject generation.
- no hidden decision logic.
- no execution APIs.
- no broker integration.
- no real market data assumption.
- no heavy analytics dependency installation in Prompt 33.

Regime planning contracts are not decision evidence, trading data, investment
advice, or execution approval.

## Prompt 34 Regime Feature Preparation Policy

Prompt 34 adds Regime Feature Preparation Contracts. Regime feature candidates
are metadata-only names/contracts that map future feature ideas to provenance
and evidence requirements. They do not contain feature values and they cannot be
treated as trusted real market data.

Policy rules:

- regime feature provenance is required before any future feature computation.
- regime feature evidence mapping is required before any future feature computation.
- source references and analytics family references are required by contract.
- synthetic/local-only scope remains in force until a future real-data phase is separately approved.
- no feature computation in Prompt 34.
- no feature registry writes in Prompt 34.
- no classifier inputs in Prompt 34.
- no actual regime classification in Prompt 34.
- no feature-as-trade-call rule: feature candidates must not become trading guidance.
- no feature-readiness-as-recommendation rule: readiness reports must not become advice.
- no buy, sell, hold, watch, avoid, reduce, or action-state recommendations.
- no DecisionObject generation.
- no hidden decision logic.
- no execution APIs.
- no broker integration.
- no real market data assumption.
- no heavy analytics dependency installation in Prompt 34.

Regime feature preparation contracts are governance metadata only. They are not
decision evidence, trading data, investment advice, classifier input, or
execution approval.

## Prompt 35 Analytics/Regime Milestone Audit Policy

Prompt 35 audits the analytics/regime milestone across Prompts 26-34. It
confirms current analytics outputs remain descriptive/research/data-quality-only
artifacts with source-reference and validation boundaries, and regime outputs
remain planning/contracts-only artifacts.

Rules after Prompt 35:

- analytics outputs remain research-only until future decision-engine audit.
- regime planning outputs remain planning-only until future regime audit.
- regime feature preparation outputs remain contracts-only until future feature audit.
- no real market ingestion is available to analytics/regime modules.
- no external calls are allowed from analytics/regime modules.
- no heavy analytics/model dependencies are added by Prompt 35.
- no feature computation is implemented.
- no feature registry writes are implemented.
- no classifier inputs are generated.
- no actual regime classification is implemented.
- no signals, recommendations, decisions, or DecisionObject generation are implemented.
- no execution APIs are implemented.
- Decision Desk work remains planning-only until future safety audit.

Descriptive analytics metrics, regime label placeholders, evidence mappings,
provenance requirements, and readiness reports are not decision evidence,
trading data, investment advice, recommendation payloads, or execution approval.

## Prompt 36 Retail Decision Desk Planning Policy

Prompt 36 adds Retail Decision Desk planning and guardrails. Decision Desk
evidence requirements must retain source-reference expectations, validated
input expectations, and synthetic/local-only scope until a future real-data
phase is separately approved.

Policy rules:

- decision desk evidence source references are required before future use.
- action placeholders must not be treated as recommendations.
- readiness reports must not be treated as approval.
- human-review checklists must not be bypassed or interpreted as automatic approval.
- no recommendation generation in Prompt 36.
- no action-state generation in Prompt 36.
- no confidence scoring in Prompt 36.
- no DecisionObject generation in Prompt 36.
- no execution APIs.
- no broker integration.
- no real market data assumption.

Retail Decision Desk planning contracts are governance metadata only. They are
not decision evidence, trading data, investment advice, recommendation payloads,
or execution approval.

## Prompt 38 DecisionObject Evidence Bundle Policy

Prompt 38 adds DecisionObject evidence bundle contracts. Decision evidence
items, source/provenance maps, validation checklists, human-review attachments,
and readiness reports remain contracts-only and do not contain trusted real
market data or active decision payloads.

Policy rules:

- decision evidence source references are required.
- decision evidence validation checklists are required.
- human-review attachments are required.
- real market data remains disallowed until a future real-data phase is separately approved.
- evidence bundle readiness must not be treated as a recommendation.
- evidence item presence must not be treated as decision approval.
- human-review attachment completion must not be treated as approval.
- bundle completeness must not be treated as action readiness.
- no recommendation generation in Prompt 38.
- no action-state generation in Prompt 38.
- no confidence scoring in Prompt 38.
- no active DecisionObject generation in Prompt 38.
- no execution APIs.
- no broker integration.
- no real market data assumption.

DecisionObject evidence bundle contracts are governance metadata only. They are
not trading data, investment advice, recommendation payloads, active
DecisionObjects, or execution approval.

## Prompt 39 Decision Safety Policy

Prompt 39 adds Decision Safety and Human-Review Guardrails. Decision safety
guardrails, human-review gates, approval placeholders, override prohibition
contracts, blocked output policies, and readiness reports remain governance
metadata only.

Policy rules:

- decision safety blocked output policy is required.
- human-review gates are not approvals.
- approval placeholders are inactive and must not grant output permissions.
- overrides are prohibited.
- emergency bypass is not implemented.
- readiness reports must not be treated as recommendations, approvals, or trade readiness.
- no recommendation generation in Prompt 39.
- no action-state generation in Prompt 39.
- no confidence scoring in Prompt 39.
- no active DecisionObject generation in Prompt 39.
- no approvals in Prompt 39.
- no overrides in Prompt 39.
- no execution APIs.
- no broker integration.
- no real market data assumption.

Decision Safety outputs are not trading data, investment advice,
recommendation payloads, active DecisionObjects, approval records, override
records, or execution approval.

## Prompt 40 Decision Desk API Contract Skeleton Policy

Prompt 40 adds Decision Desk API request/response placeholders, evidence
reference placeholders, safety reference placeholders, unavailable responses,
and API contract metadata. These are contract metadata only.

Policy rules:

- no Decision Desk API input-for-recommendation endpoint is allowed.
- Decision Desk API responses must be unavailable by default.
- request placeholders must not be treated as recommendation requests.
- response placeholders must not be treated as decisions.
- evidence references must not be treated as complete bundles.
- safety references must not be treated as passed checks.
- unavailable responses must not be treated as recommendations, approvals, or trade readiness.
- no recommendation generation in Prompt 40.
- no action-state generation in Prompt 40.
- no confidence scoring in Prompt 40.
- no active DecisionObject generation in Prompt 40.
- no approvals in Prompt 40.
- no overrides in Prompt 40.
- no execution APIs.
- no broker integration.
- no real market data assumption.

Decision Desk API skeleton outputs are not trading data, investment advice,
recommendation payloads, active DecisionObjects, approval records, override
records, safety approvals, or execution approval.

## Prompt 41 Decision Desk Milestone Audit Policy

Prompt 41 audits the Decision Desk planning milestone and confirms Prompts
36-40 remain planning, contract, guardrail, and unavailable metadata only.

Policy rules:

- Decision Desk API responses remain unavailable by default.
- no Decision Desk API input-for-recommendation endpoint is allowed.
- placeholders must not be treated as decisions.
- readiness templates must not be treated as recommendations.
- human-review gates and attachments must not be treated as approvals.
- approval placeholders must remain inactive.
- override prohibition must remain fail-closed.
- no recommendation generation is allowed.
- no action-state generation is allowed.
- no confidence scoring is allowed.
- no active DecisionObject generation is allowed.
- no execution APIs are allowed.

Decision Desk milestone audit artifacts are governance records only. They are
not trading data, investment advice, approval, override, execution readiness,
or production market-data evidence.

## Prompt 42 Decision Readiness API Policy

Prompt 42 adds read-only Decision Desk Readiness API skeleton endpoints and
settings.

Policy rules:

- no Decision Readiness API input-for-recommendation endpoint is allowed.
- no Decision Readiness API input-for-readiness-to-trade endpoint is allowed.
- readiness responses remain unavailable by default.
- readiness placeholders must not be treated as trade readiness.
- evidence references must not be treated as complete evidence bundles.
- safety references must not be treated as passed safety checks.
- human-review references must not be treated as approvals.
- blocked-output references must not be treated as bypass permission.
- no recommendation generation is allowed.
- no action-state generation is allowed.
- no confidence scoring is allowed.
- no active DecisionObject generation is allowed.
- no approval or override is allowed.
- no execution APIs are allowed.

Decision readiness API artifacts are contract metadata only. They are not
trading data, investment advice, approval, override, execution readiness,
recommendation readiness, or production market-data evidence.

## Prompt 43 Decision Display Policy

Prompt 43 adds read-only Decision Desk Display Contract Skeleton endpoints and
settings.

Policy rules:

- no display-as-recommendation is allowed.
- no Decision Display input-for-recommendation endpoint is allowed.
- no Decision Display input-for-readiness-to-trade endpoint is allowed.
- display responses remain unavailable by default.
- display placeholders must not be treated as decisions.
- display cards must not be treated as recommendation cards.
- display sections must not be treated as active UI.
- evidence references must not be treated as complete evidence bundles.
- safety references must not be treated as passed safety checks.
- no recommendation generation is allowed.
- no action-state generation is allowed.
- no confidence scoring is allowed.
- no active DecisionObject generation is allowed.
- no approval or override is allowed.
- no execution APIs are allowed.

Decision display artifacts are contract metadata only. They are not trading
data, investment advice, active UI, approval, override, execution readiness,
recommendation readiness, readiness-to-trade, or production market-data
evidence.

## Prompt 44 Decision Evidence Validation Policy

Prompt 44 adds Decision Evidence Validation v0 as validation-only inspection of
DecisionObject evidence bundle contracts, evidence items, source references,
provenance, validation checklists, and human-review attachments.

Policy rules:

- no validation-pass-as-recommendation is allowed.
- no validation-pass-as-readiness-to-trade is allowed.
- no validation-pass-as-approval is allowed.
- validation results must not be treated as active DecisionObject readiness.
- evidence bundle completeness must not be treated as decision approval.
- human-review attachment completeness must not be treated as human approval.
- no validation endpoint may accept market data to produce recommendations.
- no recommendation generation is allowed.
- no action-state generation is allowed.
- no confidence scoring is allowed.
- no active DecisionObject generation is allowed.
- no approval or override is allowed.
- no execution APIs are allowed.

Decision evidence validation artifacts are contract validation metadata only.
They are not trading data, investment advice, approval, override, execution
readiness, recommendation readiness, readiness-to-trade, or production
market-data evidence.

## Prompt 45 Decision Human Review Workflow Policy

Prompt 45 adds Decision Human Review workflow skeleton endpoints and settings.

Policy rules:

- no human-review-workflow-as-approval is allowed.
- human review workflow responses remain unavailable by default.
- review placeholders must not be treated as decisions.
- review task placeholders must not be treated as assigned or completed tasks.
- reviewer role placeholders must not be treated as authenticated users.
- review queue placeholders must not be treated as active queues.
- no task assignment is allowed.
- no reviewer auth is allowed.
- no notifications are allowed.
- no active workflow persistence is allowed.
- no recommendation generation is allowed.
- no action-state generation is allowed.
- no confidence scoring is allowed.
- no active DecisionObject generation is allowed.
- no readiness-to-trade is allowed.
- no approval or override is allowed.
- no execution APIs are allowed.

Decision human review artifacts are workflow skeleton metadata only. They are
not trading data, investment advice, approval, override, execution readiness,
recommendation readiness, readiness-to-trade, or production market-data
evidence.

## Prompt 46 Decision Desk Milestone Audit 2 Policy

Prompt 46 confirms the second Decision Desk skeleton phase remains audit-only.
Readiness responses must not be treated as recommendations. Display placeholders
must not be treated as decisions. Validation passes must not be treated as
approvals. Human review workflow placeholders must not be treated as approvals.
No readiness-as-recommendation, display-as-decision, validation-as-approval, or
review-workflow-as-approval rule is allowed. None of these layers may ingest
real market data, claim live data, publish events, or enable execution APIs.

## Prompt 47 Decision Boundary Policy

Prompt 47 adds a no cross-module boundary bypass rule. Decision Desk modules may
only expose their documented contract, validation, display, workflow, or
boundary-hardening purpose. A module must not use another module as a shortcut
to generate recommendations, action states, confidence scores, active
DecisionObjects, approvals, overrides, active UI, active workflow,
readiness-to-trade, broker behavior, or execution.

Prompt 47 also adds a no endpoint boundary bypass rule. Decision endpoints must
remain read-only, unavailable-by-default or placeholder-only, and must not
accept market data to generate decisions. They must not expose secrets, claim
live market data, publish events, or create execution APIs.

The forbidden behavior registry is policy metadata only. It records behaviors
that remain forbidden and require a future prompt plus audit-before-unlock. It
does not enable recommendations, approval, override, readiness-to-trade, active
UI, active workflow, or execution.

No endpoint boundary bypass is allowed, and no module bypasses forbidden
behavior registry policy. These rules are explicit Prompt 47 safety invariants.

no module bypasses forbidden behavior registry controls in Prompt 47.

## Prompt 48 Decision API Display Integration Readiness Policy

Prompt 48 confirms Decision API/display integration readiness without changing
data trust boundaries. No API-to-display recommendation path is allowed. No
readiness-to-display-trade path is allowed. No display-as-decision rule is
allowed. no display-as-decision is allowed. No validation-as-approval and no
review-workflow-as-approval behavior is allowed.

Retail Dashboard readiness is planning-only. Dashboard planning must not treat
synthetic/local file data as trusted real market data, must not create
recommendation cards, must not create trading controls, must not expose broker
linkage, and must not add execution APIs.

## Prompt 49 Retail Dashboard Planning Policy

Prompt 49 adds a no dashboard-as-recommendation rule, a no dashboard-as-execution-control rule, a no placeholder-card-as-decision rule, and a no real market data dashboard display yet rule.

Retail Dashboard placeholders must not be treated as validated recommendations, active DecisionObjects, readiness-to-trade, broker controls, or execution controls.

## Prompt 50 Retail Dashboard API Policy

Prompt 50 adds a no dashboard API as recommendation rule, a no dashboard API as
execution control rule, a no dashboard API live data rule, and an
unavailable-by-default dashboard API policy.

Retail Dashboard API placeholders, data references, decision references, safety
references, and unavailable responses must not be treated as live market data,
recommendations, active DecisionObjects, readiness-to-trade, broker controls,
approvals, overrides, or execution controls.

## Prompt 51 Retail Dashboard Display Policy

Prompt 51 adds a no dashboard display as recommendation rule, a no dashboard
display as execution control rule, a no dashboard display live data rule, and an
unavailable-by-default dashboard display policy.

Retail Dashboard Display layout placeholders, widget placeholders, visual
section placeholders, badge placeholders, and unavailable responses must not be
treated as active UI, frontend components, desktop UI components, live market
data, recommendation cards, action generation, confidence scoring, active
DecisionObjects, readiness-to-trade, broker controls, approvals, overrides, or
execution controls.

## Prompt 52 Retail Dashboard Safety Boundary Audit Policy

Prompt 52 confirms the Retail Dashboard safety boundary across planning, API,
and display artifacts.

Policy confirmations:

- no dashboard-as-recommendation rule.
- no dashboard-as-execution-control rule.
- no live data display rule.
- no placeholder-as-dashboard-output rule.
- no API placeholder as active dashboard output.
- no display placeholder as active UI.
- no widget or badge as recommendation, readiness-to-trade, broker control, or execution control.

Retail Dashboard planning/API/display artifacts are not trading data,
investment advice, recommendation payloads, active DecisionObjects, live market
data, approval records, override records, broker controls, or execution
approval.

## Prompt 53 Retail Dashboard Milestone Audit Policy

Prompt 53 confirms the Retail Dashboard milestone boundary across planning,
API, display, and safety audit artifacts.

Policy confirmations:

- no dashboard-as-recommendation rule.
- no dashboard-as-execution-control rule.
- No live data display rule.
- no placeholder-as-dashboard-output rule.
- no API placeholder as active dashboard output.
- no display placeholder as active UI.
- no widget or badge as recommendation, readiness-to-trade, broker control, or execution control.

Retail Dashboard planning/API/display artifacts remain placeholders and audit
records only. They are not live market data, trading data, recommendation
payloads, active DecisionObjects, approval records, override records, broker
controls, or execution approval.

## Prompt 54 Retail Dashboard Boundary Policy

Prompt 54 adds a no cross-module dashboard boundary bypass rule, a no endpoint
dashboard boundary bypass rule, and a Retail Dashboard forbidden behavior
registry policy.

Policy shorthand: no endpoint dashboard boundary bypass, no cross-module
dashboard boundary bypass, and no module bypasses the Retail Dashboard
forbidden behavior registry.

Retail Dashboard planning/API/display/boundary modules must not bypass the
forbidden behavior registry. Endpoint families must remain read-only metadata
surfaces and must not accept market data for dashboard decisions, generate
recommendations, create active UI, generate DecisionObjects, expose broker
controls, or execute trades.

The Retail Dashboard forbidden behavior registry is policy metadata only. It
does not make synthetic/local file data trusted real market data, does not
enable live data display, and does not unlock recommendations, action
generation, confidence scoring, readiness-to-trade, broker controls, approvals,
overrides, or execution APIs.

## Prompt 55 Retail Dashboard API/Display Integration Readiness Policy

Prompt 55 confirms Retail Dashboard planning/API/display/boundary integration
without changing data trust boundaries.

Policy confirmations:

- no API-to-display recommendation path.
- no display-as-decision rule.
- no display-to-decision path.
- no display-to-execution path.
- no dashboard-boundary-bypass rule.
- no live data display rule.
- no placeholder-as-dashboard-output rule.
- no market-data-to-dashboard-recommendation endpoint.

Retail Dashboard planning/API/display/boundary artifacts must not be treated as
live market data, trading data, recommendation payloads, active
DecisionObjects, readiness-to-trade, approval records, override records, broker
controls, or execution approvals.

## Prompt 56 Retail Trader Experience Planning Policy

Prompt 56 adds no retail trader experience as recommendation rule, no retail
trader experience as execution control rule, no retail trader suitability
profiling rule, no placeholder-experience-as-decision rule, and no real market
data trader experience display yet rule.

Retail Trader Experience persona, journey, section, card, dashboard reference,
decision reference, safety reference, and readiness placeholders must not be
treated as live market data, trading data, recommendation payloads, active
DecisionObjects, readiness-to-trade, suitability profiles, approval records,
override records, broker controls, or execution approvals.

The Retail Trader Experience planning layer remains unavailable by default and
does not make synthetic/local file data trusted real market data.

## Prompt 57 Retail Trader Experience API Data Policy

Retail Trader Experience API skeleton responses are placeholders only. They are
not recommendations, not execution controls, not suitability profiles, not live
data displays, and not real market data outputs.

Prompt 57 adds these explicit rules:

- no retail trader API as recommendation rule.
- no retail trader API as execution control rule.
- no retail trader API suitability profiling rule.
- no retail trader API live data rule.
- unavailable-by-default trader experience API policy.

The Retail Trader Experience API must remain unavailable-by-default. It cannot
accept market data and return trader decisions, cannot expose live data, cannot
convert persona or journey references into suitability profiling, cannot treat
dashboard references as active dashboard output, and cannot treat placeholders
as decisions, approvals, overrides, broker controls, readiness-to-trade, or
execution.

## Prompt 58 Retail Trader Experience Display Data Policy

Retail Trader Experience Display skeleton responses are placeholders only. They
are not recommendations, not execution controls, not suitability profiles, not
live data displays, and not real market data outputs.

Prompt 58 adds these explicit rules:

- no retail trader display as recommendation rule.
- no retail trader display as execution control rule.
- no retail trader display suitability profiling rule.
- no retail trader display live data rule.
- unavailable-by-default trader experience display policy.

The Retail Trader Experience Display must remain unavailable-by-default. It
cannot accept market data and return trader displays, cannot expose live data,
cannot convert persona visual placeholders or journey visual placeholders into
suitability profiling, cannot treat dashboard placeholders as active dashboard
output, and cannot treat widgets or badges as decisions, approvals, overrides,
broker controls, readiness-to-trade, recommendations, or execution.

## Prompt 59 Retail Trader Experience Safety Boundary Audit Policy

Prompt 59 confirms Retail Trader Experience safety boundary audit rules:

- no experience-as-recommendation rule.
- no experience-as-execution-control rule.
- no persona-as-suitability-profile rule.
- no live data display rule.
- no placeholder-as-trader-output rule.

Retail Trader Experience planning/API/display artifacts must not be treated as
live market data, trading data, recommendation payloads, active
DecisionObjects, readiness-to-trade, suitability profiles, approval records,
override records, broker controls, or execution approvals. The safety boundary
audit does not change synthetic/local file data into trusted real market data
and does not create a trader-experience-to-execution path.

## Prompt 60 Retail Trader Experience Milestone Audit Policy

Prompt 60 confirms Retail Trader Experience milestone audit rules:

- no experience-as-recommendation rule.
- no experience-as-execution-control rule.
- no persona-as-suitability-profile rule.
- no live data display rule.
- no placeholder-as-trader-output rule.

Retail Trader Experience planning/API/display/safety-audit artifacts must not
be treated as live market data, trading data, recommendation payloads, active
DecisionObjects, readiness-to-trade, suitability profiles, approval records,
override records, broker controls, or execution approvals. The milestone audit
does not change synthetic/local file data into trusted real market data and
does not create a trader-experience-to-execution path.

## Prompt 61 Retail Trader Experience Boundary Hardening Policy

Prompt 61 adds Retail Trader Experience system boundary hardening rules:

- no cross-module Retail Trader Experience boundary bypass rule.
- no endpoint Retail Trader Experience boundary bypass rule.
- Retail Trader Experience forbidden behavior registry policy.
- no persona-to-suitability-profile path rule.
- no journey-to-trading-advice path rule.

Retail Trader Experience planning/API/display/boundary artifacts must not be
treated as live market data, trading data, recommendation payloads, active
DecisionObjects, readiness-to-trade, suitability profiles, trading permission
profiles, approval records, override records, broker controls, or execution
approvals. The boundary layer does not change synthetic/local file data into
trusted real market data, does not enable recommendations, does not create
suitability profiling, and does not create a trader-experience-to-execution
path.

## Prompt 62 Retail Trader Experience API/Display Integration Readiness Policy

Prompt 62 confirms Retail Trader Experience API/display integration readiness
rules:

- no API-to-display recommendation path rule.
- no display-as-decision rule.
- no persona-as-suitability-profile rule.
- no journey-as-trading-advice rule.
- no experience-boundary-bypass rule.
- no live data display rule.

Retail Trader Experience planning/API/display/boundary artifacts must not be
treated as live market data, trading data, recommendation payloads, active
DecisionObjects, readiness-to-trade, suitability profiles, trading permission
profiles, approval records, override records, broker controls, or execution
approvals. The integration readiness audit does not change synthetic/local
file data into trusted real market data, does not enable recommendations, does
not create suitability profiling, does not create an API-to-display
recommendation path, does not create a display-to-decision path, and does not
create a trader-experience-to-execution path.

## Prompt 63 Strategy Research Workspace Planning Policy

Prompt 63 adds Strategy Research Workspace planning and guardrail rules:

- no Strategy Research Workspace as recommendation rule.
- no Strategy Research Workspace as execution control rule.
- no paper-to-strategy rule.
- no strategy-to-backtest rule.
- no research artifact as validated strategy rule.
- no placeholder-workspace-as-decision rule.
- no real market data research workspace display yet.

Strategy Research Workspace placeholders must not be treated as live market
data, real market data, parsed research, generated strategies, generated
signals, generated factors, generated code, backtest results, recommendation
payloads, active DecisionObjects, readiness-to-trade, approval records,
override records, broker controls, or execution approvals. Prompt 63 does not
change synthetic/local file data into trusted real market data and does not
create research-to-recommendation or research-to-execution behavior.

## Prompt 64 Strategy Research Workspace API Policy

Prompt 64 adds Strategy Research Workspace API contract-skeleton rules:

- no strategy research API as recommendation rule.
- no strategy research API as execution control rule.
- no strategy research API paper parsing rule.
- no strategy research API strategy generation rule.
- no strategy research API backtesting rule.
- unavailable-by-default strategy research API policy.

Strategy Research Workspace API request placeholders, response placeholders,
workspace references, artifact references, paper references, hypothesis
references, dataset references, experiment references, safety references, and
unavailable responses must not be treated as live market data, parsed papers,
method extraction, generated strategies, generated strategy code, generated
signals, generated factors, generated backtests, optimization results,
recommendation payloads, action states, confidence scores, active
DecisionObjects, readiness-to-trade, approval records, override records,
broker controls, or execution approvals. Prompt 64 does not change
synthetic/local file data into trusted real market data, does not create paper
ingestion or paper parsing, does not create paper-to-strategy behavior, does
not create strategy-to-backtest behavior, does not create API-to-recommendation
behavior, and does not create API-to-execution behavior.

## Prompt 65 Strategy Research Workspace Display Policy

Prompt 65 adds Strategy Research Workspace display contract-skeleton rules:

- no strategy research display as recommendation rule.
- no strategy research display as execution control rule.
- no strategy research display paper parsing rule.
- no strategy research display strategy generation rule.
- no strategy research display backtesting rule.
- unavailable-by-default strategy research display policy.

Strategy Research Workspace Display contract metadata, workspace visual
placeholders, artifact visual placeholders, paper visual placeholders,
hypothesis visual placeholders, dataset visual placeholders, experiment visual
placeholders, badge placeholders, and unavailable display responses must not
be treated as live market data, parsed papers, method extraction, generated
strategies, generated strategy code, generated signals, generated factors,
generated backtests, optimization results, recommendation payloads, action
states, confidence scores, active DecisionObjects, readiness-to-trade,
approval records, override records, broker controls, or execution approvals.
Prompt 65 does not change synthetic/local file data into trusted real market
data, does not create paper ingestion or paper parsing, does not create
paper-to-strategy behavior, does not create strategy-to-backtest behavior,
does not create display-to-recommendation behavior, and does not create
display-to-execution behavior.

## Prompt 66 Strategy Research Workspace Safety Boundary Audit Confirmation

Strategy Research Workspace planning, API, and display artifacts remain
contract/skeleton/audit layers only. They add no real market ingestion, no
external calls, no scraping, no provider SDKs, no credentials, no live provider
clients, no paper ingestion, no paper parsing, no strategy generation, no
strategy code generation, no backtesting, no optimization, no recommendation
generation, no action generation, no confidence scoring, no DecisionObject
generation, no readiness-to-trade, no broker controls, and no execution APIs.

Data policy rules for the Strategy Research Workspace:

- no paper-to-strategy rule.
- no strategy-to-backtest rule.
- no research-as-recommendation rule.
- no research-as-execution-control rule.
- no live data display rule.
- no placeholder-as-strategy-output rule.
- no paper, PDF, URL, arXiv, or market-data processing endpoint rule.
- unavailable-by-default strategy research API and display policy.

## Prompt 67 Strategy Research Workspace Milestone Audit Confirmation

Prompt 67 confirms the Strategy Research Workspace data policy remains
fail-closed:

- no paper-to-strategy rule.
- no strategy-to-backtest rule.
- no research-as-recommendation rule.
- no research-as-execution-control rule.
- no live data display rule.
- no placeholder-as-strategy-output rule.
- no paper, PDF, URL, arXiv, or market-data processing endpoint rule.
- no synthetic/local file data as trusted real market data rule.
- unavailable-by-default strategy research planning/API/display policy.

Strategy Research Workspace milestone artifacts must not be treated as live
market data, parsed research, generated strategies, backtest results,
recommendations, action states, confidence scores, DecisionObjects,
readiness-to-trade, broker controls, approvals, overrides, or execution
controls.

## Prompt 79 Research Artifact Index Display Data Policy

Prompt 79 adds these Research Artifact Index Display data policy rules:

- no display-as-indexing rule.
- no display-as-search-result rule.
- no display-as-ranking-result rule.
- no display-as-embedding/vector-store rule.
- no display-as-ingestion rule.
- no display-as-file-preview rule.
- no display-as-paper-parsing rule.
- no display-as-strategy-output rule.
- no display-as-backtest-result rule.
- no display-as-recommendation rule.
- no display-as-execution-control rule.

Research Artifact Index Display card, reference, tag, provenance, lifecycle,
badge, unavailable, safety, and health artifacts are backend display contract
metadata only. They must not be treated as ingested content, stored content,
indexed content, searchable content, ranked content, embedded/vectorized
content, retrieved content, parsed paper content, trusted market data,
generated strategy output, backtest evidence, recommendations, action states,
confidence scores, DecisionObjects, readiness-to-trade, broker controls,
approvals, overrides, or execution controls.

## Prompt 68 Strategy Research Workspace System Boundary Hardening Policy

Prompt 68 adds Strategy Research Workspace forbidden behavior registry,
endpoint boundary policy, module boundary policy, and cross-module invariant
contracts. These are boundary-hardening-only data policy controls and not
active research capability.

Policy rules:

- no cross-module research boundary bypass.
- no endpoint research boundary bypass.
- no paper-to-strategy boundary bypass.
- no strategy-to-backtest boundary bypass.
- no research-as-recommendation boundary bypass.
- no research-as-execution-control boundary bypass.
- no live data display through Strategy Research Workspace placeholders.
- no placeholder-as-strategy-output rule.
- forbidden behavior registry policy applies to active UI, frontend
  components, desktop components, paper ingestion, paper parsing, arXiv
  ingestion, LLM paper analysis, strategy generation, strategy code
  generation, signal/factor/alpha generation, backtesting, optimization,
  recommendation generation, action generation, confidence scoring,
  DecisionObjects, readiness-to-trade, broker controls, approvals, overrides,
  provider SDKs, scraping, external calls, secrets, and execution APIs.

Strategy Research Workspace boundary artifacts must not be treated as live
market data, parsed research, generated strategies, backtest results,
recommendations, action states, confidence scores, DecisionObjects,
readiness-to-trade, broker controls, approvals, overrides, or execution
controls.

## Prompt 69 Strategy Research Workspace API Display Integration Policy

Prompt 69 confirms the Strategy Research Workspace integration data policy:

- no API-to-display strategy path rule.
- no API-to-display backtest result path rule.
- no parsed-paper-to-display path rule.
- no Research Artifact Registry implementation before planning/guardrails rule.
- no active artifact ingestion/storage before planning/guardrails rule.
- no research-as-recommendation rule.
- no research-as-execution-control rule.
- no live data display rule.
- no placeholder-as-strategy-output rule.

Strategy Research Workspace integration artifacts must not be treated as live
market data, parsed research, generated strategies, backtest results,
recommendations, action states, confidence scores, DecisionObjects,
readiness-to-trade, broker controls, approvals, overrides, or execution
controls. Research Artifact Registry is ready for planning and guardrails only.

## Prompt 70 Research Artifact Registry Planning Policy

Prompt 70 adds these data policy rules:

- no active artifact ingestion/storage rule.
- no persistent artifact registry writes rule.
- no artifact reference fetch rule.
- no file upload/download rule.
- no paper parsing rule.
- no PDF parsing, arXiv ingestion, or LLM paper analysis rule.
- no placeholder-as-validated-artifact rule.
- no artifact-as-strategy-output rule.
- no artifact-as-backtest-result rule.
- no artifact-as-recommendation rule.
- no artifact-as-execution-control rule.

Research Artifact Registry metadata, references, provenance records, and
lifecycle records are placeholders only. They cannot claim trusted real market
data, validated strategies, backtest evidence, recommendations,
readiness-to-trade, broker controls, approvals, overrides, or execution
capability.
## Prompt 71 Research Artifact Registry API Contract Policy

Prompt 71 adds these API data policy rules:

- no API artifact ingestion/storage rule.
- no API persistent artifact registry writes rule.
- no API file upload/download rule.
- no API artifact reference fetch rule.
- no API paper parsing rule.
- no API PDF parsing, arXiv ingestion, or LLM paper analysis rule.
- no API placeholder-as-validated-artifact rule.
- no API artifact-as-strategy-output rule.
- no API artifact-as-backtest-result rule.
- no API artifact-as-recommendation rule.
- no API artifact-as-execution-control rule.

Research Artifact Registry API requests, responses, references, provenance
references, lifecycle references, and unavailable responses are placeholders
only. They cannot claim trusted real market data, validated artifacts,
validated strategies, backtest evidence, recommendations, readiness-to-trade,
broker controls, approvals, overrides, or execution capability.

This API contract layer performs no external calls, reads no market data,
reads no files, writes no files, publishes no events, creates no frontend
components, creates no desktop components, generates no recommendations,
scores no confidence, generates no DecisionObjects, exposes no broker
controls, and creates no execution APIs.

## Prompt 72 Research Artifact Registry Display Contract Policy

Prompt 72 adds these display data policy rules:

- no display-as-ingestion rule.
- no display-as-file-preview rule.
- no display-as-paper-parsing rule.
- no display-as-strategy-output rule.
- no display-as-backtest-result rule.
- no display-as-recommendation rule.
- no display-as-execution-control rule.
- no display-as-validated-artifact rule.

Research Artifact Registry display metadata, artifact card placeholders,
reference display placeholders, provenance display placeholders, lifecycle
display placeholders, lifecycle badges, safety badges, and unavailable display
responses are placeholders only. They cannot claim trusted real market data,
validated artifacts, validated strategies, backtest evidence,
recommendations, readiness-to-trade, broker controls, approvals, overrides, or
execution capability.

This display contract layer performs no external calls, reads no market data,
reads no files, writes no files, stores no artifacts, previews no files,
publishes no events, creates no frontend components, creates no desktop
components, creates no active UI, parses no papers, parses no PDFs, ingests no
arXiv records, runs no LLM analysis, generates no strategies, runs no
backtests, generates no recommendations, scores no confidence, generates no
DecisionObjects, exposes no broker controls, and creates no execution APIs.

## Prompt 73 Research Artifact Registry Safety Audit Policy

Prompt 73 confirms these Research Artifact Registry data policy rules:

- no artifact ingestion/storage bypass rule.
- no artifact persistent storage bypass rule.
- no artifact upload/download bypass rule.
- no artifact reference fetch rule.
- no artifact display preview rule.
- no artifact-to-strategy rule.
- no artifact-to-backtest rule.
- no artifact-to-recommendation rule.
- no artifact-to-execution rule.

Research Artifact Registry planning, API, and display placeholders must not be
treated as ingested content, stored content, parsed paper content, trusted
market data, generated strategy output, backtest evidence, recommendations,
action states, confidence scores, DecisionObjects, readiness-to-trade, broker
controls, approvals, overrides, or execution controls.

## Prompt 74 Research Artifact Registry Milestone Audit Policy

Prompt 74 confirms these Research Artifact Registry data policy rules:

- no artifact-to-index implementation before planning/guardrails rule.
- no artifact ingestion/storage bypass rule.
- no artifact upload/download bypass rule.
- no artifact reference fetch rule.
- no artifact display preview rule.
- no artifact-to-strategy rule.
- no artifact-to-backtest rule.
- no artifact-to-recommendation rule.
- no artifact-to-execution rule.

Research Artifact Registry planning, API, display, and safety audit artifacts
remain milestone-audited placeholders only. They must not be treated as
ingested content, stored content, parsed paper content, trusted market data,
generated strategy output, backtest evidence, recommendations, action states,
confidence scores, DecisionObjects, readiness-to-trade, broker controls,
approvals, overrides, or execution controls.

## Prompt 75 Research Artifact Registry Boundary Hardening Policy

Prompt 75 adds these artifact registry boundary policy rules:

- no cross-module artifact registry boundary bypass rule.
- no endpoint artifact registry boundary bypass rule.
- no artifact ingestion/storage boundary bypass rule.
- no artifact upload/download boundary bypass rule.
- no artifact file preview boundary bypass rule.
- no artifact-to-strategy boundary bypass rule.
- no artifact-to-backtest boundary bypass rule.
- forbidden behavior registry policy.

Research Artifact Registry forbidden behavior registry, endpoint policies,
module policies, and invariants are boundary metadata only. They must not be
treated as active ingestion, persistent storage, upload/download, file
preview, parsed paper content, trusted market data, generated strategy output,
backtest evidence, recommendations, action states, confidence scores,
DecisionObjects, readiness-to-trade, broker controls, approvals, overrides, or
execution controls.

## Prompt 76 Research Artifact Registry Integration Readiness Policy

Prompt 76 adds these artifact registry integration-readiness policy rules:

- no API-to-display artifact implementation path rule.
- no API-to-display file preview path rule.
- no API-to-display paper parsing path rule.
- no artifact-to-index implementation before planning/guardrails rule.
- no artifact-as-strategy output rule.
- no artifact-as-backtest result rule.
- no artifact-as-recommendation rule.
- no artifact-as-execution-control rule.

Research Artifact Registry planning, API, display, and boundary artifacts
remain placeholders and metadata only. They must not be treated as ingested
content, stored content, indexed content, searchable content, ranked content,
embedded/vectorized content, parsed paper content, trusted market data,
generated strategy output, backtest evidence, recommendations, action states,
confidence scores, DecisionObjects, readiness-to-trade, broker controls,
approvals, overrides, or execution controls.

## Prompt 77 Research Artifact Index Planning Data Policy

Prompt 77 adds these Research Artifact Index data policy rules:

- no index-as-ingestion rule.
- no index-as-storage rule.
- no index-as-search rule.
- no index-as-ranking rule.
- no index-as-embedding/vector-store rule.
- no artifact index reference fetch rule.
- no artifact-to-strategy rule.
- no artifact-to-backtest rule.
- no artifact-to-recommendation rule.
- no artifact-to-execution rule.

Research Artifact Index metadata, key, reference, tag, provenance, lifecycle,
forbidden-interaction, safety, readiness, and endpoint artifacts are planning
metadata only. They must not be treated as ingested content, stored content,
indexed content, searchable content, ranked content, embedded/vectorized
content, retrieved content, parsed paper content, trusted market data,
generated strategy output, backtest evidence, recommendations, action states,
confidence scores, DecisionObjects, readiness-to-trade, broker controls,
approvals, overrides, or execution controls.

## Interlude Active Decision Architecture Target Data Policy

Future market data must pass data quality and provenance layers before any
future decision candidate use. This requirement does not enable market-data
ingestion, provider clients, external calls, timeseries writes, feature
computation, recommendation generation, confidence scoring, DecisionObject
generation, paper trading, broker controls, or execution APIs.

No direct market-data-to-trade path is allowed. No direct signal-to-trade path
is allowed. Decision candidate is not a trade.

## Prompt 78 Research Artifact Index API Data Policy

Prompt 78 adds these Research Artifact Index API data policy rules:

- no API index-as-ingestion rule.
- no API index-as-storage rule.
- no API index-as-search rule.
- no API index-as-ranking rule.
- no API index-as-embedding/vector-store rule.
- no API artifact index reference fetch rule.
- no API artifact-to-strategy rule.
- no API artifact-to-backtest rule.
- no API artifact-to-recommendation rule.
- no API artifact-to-execution rule.

Research Artifact Index API request, response, reference, unavailable, safety,
and health artifacts are read-only API contract metadata only. They must not
be treated as ingested content, stored content, indexed content, searchable
content, ranked content, embedded/vectorized content, retrieved content,
parsed paper content, trusted market data, generated strategy output, backtest
evidence, recommendations, action states, confidence scores, DecisionObjects,
readiness-to-trade, broker controls, approvals, overrides, or execution
controls.
