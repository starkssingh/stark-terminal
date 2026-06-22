# Project Map

## Current Repo Structure

```text
stark-terminal/
  README.md
  AGENTS.md
  PROJECT_MAP.md
  pyproject.toml
  .gitignore
  .env.example
  docs/
    MILESTONE_A_B_AUDIT.md
    REPO_INVENTORY.md
    API_SURFACE_INVENTORY.md
    SAFETY_AUDIT.md
    NEXT_PHASE_PLAN.md
    SYNTHETIC_MARKET_DATA_FIXTURES.md
    OHLCV_FIXTURE_CONTRACTS.md
    SAMPLE_DATA_POLICY.md
    INSTRUMENT_PERSISTENCE_FOUNDATION.md
    INSTRUMENT_REPOSITORY_POLICY.md
    MARKET_DATA_BATCH_PERSISTENCE.md
    BATCH_METADATA_POLICY.md
    DATA_FOUNDATION_AUDIT.md
    DATA_PERSISTENCE_BOUNDARY.md
    SYNTHETIC_DATA_SAFETY_AUDIT.md
    DATA_FOUNDATION_NEXT_PHASE.md
    SYNTHETIC_OHLCV_STORAGE_FOUNDATION.md
    TIMESCALE_SYNTHETIC_STORAGE_POLICY.md
    SYNTHETIC_OHLCV_RESEARCH_LAKE_EXPORT.md
    OHLCV_EXPORT_MANIFEST_POLICY.md
    PROVIDER_ADAPTER_IMPLEMENTATION_PLAN.md
    PROVIDER_GUARDRAIL_POLICY.md
    PROVIDER_APPROVAL_WORKFLOW.md
    PROVIDER_COMPLIANCE_CHECKLIST.md
    LOCAL_SAMPLE_PROVIDER_ADAPTER.md
    LOCAL_SAMPLE_PROVIDER_POLICY.md
    DATA_FOUNDATION_MILESTONE_AUDIT.md
    SYNTHETIC_STORAGE_EXPORT_AUDIT.md
    PROVIDER_GUARDRAIL_AUDIT.md
    LOCAL_SAMPLE_PROVIDER_AUDIT.md
    DATA_FOUNDATION_MILESTONE_NEXT_PHASE.md
    REAL_PROVIDER_READINESS_CHECKLIST.md
    PROVIDER_CANDIDATE_SELECTION_POLICY.md
    PROVIDER_RISK_SCORING_POLICY.md
    PROVIDER_CAPABILITY_GAP_ANALYSIS.md
    LOCAL_FILE_PROVIDER_ADAPTER.md
    LOCAL_FILE_PROVIDER_POLICY.md
    LOCAL_FILE_PATH_SAFETY.md
    PROVIDER_ADAPTER_MILESTONE_AUDIT.md
    PROVIDER_BOUNDARY_AUDIT.md
    PROVIDER_NO_EXTERNAL_CALLS_AUDIT.md
    PROVIDER_NEXT_PHASE_PLAN.md
  apps/
    api/
      stark_terminal_api/
        __init__.py
        main.py
        routes/
          __init__.py
          config.py
          cache.py
          data_quality.py
          database.py
          event_backbone.py
          health.py
          instruments.py
          fixtures.py
          instrument_metadata.py
          market_data_batches.py
          synthetic_ohlcv_storage.py
          synthetic_ohlcv_exports.py
          provider_guardrails.py
          provider_readiness.py
          local_sample_provider.py
          local_file_provider.py
          research_lake.py
          streams.py
          timeseries.py
          warehouse.py
          features.py
          workers.py
    desktop/
      stark_terminal_desktop/
        __init__.py
        main.py
  packages/
    core/
      stark_terminal_core/
        __init__.py
        config/
          __init__.py
          settings.py
        domain/
          __init__.py
          audit.py
          enums.py
          identifiers.py
          instrument.py
          market_data.py
          market_data_batch.py
          market_data_contracts.py
          derivatives.py
          options.py
          decision_object.py
        serialization/
          __init__.py
          json.py
    data_platform/
      stark_terminal_data_platform/
        __init__.py
        README.md
        db/
          __init__.py
          base.py
          engine.py
          session.py
          health.py
          models/
            __init__.py
            instrument.py
            data_provider.py
            audit.py
            decision.py
            timeseries.py
            market_data_batch.py
        timeseries/
          __init__.py
          health.py
          hypertables.py
          README.md
        lake/
          __init__.py
          paths.py
          zones.py
          manifest.py
          duckdb_client.py
          parquet_io.py
          registry.py
          health.py
          README.md
        cache/
          __init__.py
          keys.py
          serialization.py
          client.py
          memory.py
          health.py
          README.md
        streams/
          __init__.py
          names.py
          events.py
          serialization.py
          memory.py
          producer.py
          consumer.py
          health.py
          README.md
        event_backbone/
          __init__.py
          topics.py
          envelopes.py
          serialization.py
          memory.py
          producer.py
          consumer.py
          health.py
          README.md
        quality/
          __init__.py
          enums.py
          issues.py
          rules.py
          results.py
          reports.py
          gates.py
          validators.py
          registry.py
          builtins.py
          health.py
          README.md
        fixtures/
          __init__.py
          manifests.py
          synthetic_ohlcv.py
          catalog.py
          validation.py
          parquet.py
          health.py
          README.md
        repositories/
          __init__.py
          instruments.py
          market_data_batches.py
          ohlcv_bars.py
          README.md
        services/
          __init__.py
          instruments.py
          market_data_batches.py
          synthetic_ohlcv_storage.py
          README.md
        exports/
          __init__.py
          synthetic_ohlcv.py
          README.md
        workers/
          __init__.py
          roles.py
          jobs.py
          results.py
          base.py
          registry.py
          harness.py
          health.py
          README.md
        instruments/
          __init__.py
          normalization.py
          universe.py
          master.py
          fixtures.py
          health.py
          README.md
        providers/
          __init__.py
          base.py
          contracts.py
          guardrails.py
          approval.py
          readiness.py
          candidates.py
          selection.py
          local_sample.py
          local_file.py
          registry.py
          health.py
          README.md
        warehouse/
          __init__.py
          tables.py
          ddl.py
          client.py
          memory.py
          health.py
          README.md
        features/
          __init__.py
          definitions.py
          feature_sets.py
          values.py
          quality.py
          lineage.py
          registry.py
          health.py
          README.md
    analytics/
      stark_terminal_analytics/
        __init__.py
        README.md
    research/
      stark_terminal_research/
        __init__.py
        README.md
  alembic/
    env.py
    script.py.mako
    versions/
      0001_initial_metadata_tables.py
      0002_operational_timeseries_tables.py
      0003_market_data_batch_metadata.py
  migrations/
    README.md
  tests/
  scripts/
    audit_foundation.py
    verify_foundation.py
```

## Major Folder Purposes

- `docs/`: Product, architecture, safety, data, analytics, infrastructure, roadmap, prompt-control, and milestone audit documents.
- `apps/api/`: FastAPI backend entrypoint and HTTP routes.
- `apps/desktop/`: Windows-native PySide6 / Qt desktop shell.
- `packages/core/`: Shared typed domain contracts and enums.
- `packages/data_platform/`: SQLAlchemy/Alembic database foundation, repository/service persistence wiring, TimescaleDB schema helpers, DuckDB/Parquet lake helpers, Redis cache foundation, Redis Streams foundation, Kafka/Redpanda Event Backbone foundation, Data Quality + Validation Framework, Synthetic Fixture foundation, Worker System foundation, Instrument Master/Market Data Provider Contracts, Provider Adapter Guardrails, Provider Readiness governance, Local Sample Provider Adapter v0, Local File Provider Adapter v0, ClickHouse Warehouse foundation, and Feature Registry foundation.
- `packages/analytics/`: Placeholder for future numerical, statistical, ML, optimization, options, risk, and backtesting analytics.
- `packages/research/`: Placeholder for future Paper Lab, StrategyCandidate generation, experiment tracking, and research artifact logic.
- `tests/`: Foundation, typed settings, API, domain contract, and audit invariant tests.
- `scripts/`: Repository audit and verification scripts.

## Current Implemented Modules

- `stark_terminal_api.main`: Creates the FastAPI `app` and registers health/config/database/timeseries/research-lake/cache/streams/event-backbone/data-quality/fixtures/instrument-metadata/market-data-batches/synthetic-ohlcv-storage/synthetic-ohlcv-exports/provider-guardrails/provider-readiness/local-sample-provider/local-file-provider/workers/instruments/warehouse/features routers.
- `stark_terminal_api.routes.health`: Implements `GET /health`.
- `stark_terminal_api.routes.config`: Implements safe `GET /config`.
- `stark_terminal_api.routes.database`: Implements safe `GET /database/health`.
- `stark_terminal_api.routes.research_lake`: Implements safe `GET /research-lake/health`.
- `stark_terminal_api.routes.timeseries`: Implements safe `GET /timeseries/health`.
- `stark_terminal_api.routes.cache`: Implements safe `GET /cache/health`.
- `stark_terminal_api.routes.streams`: Implements safe `GET /streams/health`.
- `stark_terminal_api.routes.event_backbone`: Implements safe `GET /event-backbone/health` and `GET /event-backbone/topics`.
- `stark_terminal_api.routes.data_quality`: Implements safe `GET /data-quality/health` and `GET /data-quality/contracts`.
- `stark_terminal_api.routes.fixtures`: Implements safe `GET /fixtures/health` and synthetic metadata-only `GET /fixtures/catalog`.
- `stark_terminal_api.routes.instrument_metadata`: Implements safe `GET /instrument-metadata/health`, synthetic-only `GET /instrument-metadata/sample`, and fail-safe read-only `GET /instrument-metadata/list`.
- `stark_terminal_api.routes.market_data_batches`: Implements safe `GET /market-data-batches/health`, synthetic-only metadata `GET /market-data-batches/sample`, and fail-safe read-only `GET /market-data-batches/list`.
- `stark_terminal_api.routes.synthetic_ohlcv_storage`: Implements safe `GET /synthetic-ohlcv-storage/health`, synthetic/test-only `GET /synthetic-ohlcv-storage/sample`, and read-only `GET /synthetic-ohlcv-storage/contracts`.
- `stark_terminal_api.routes.synthetic_ohlcv_exports`: Implements safe `GET /synthetic-ohlcv-exports/health`, read-only `GET /synthetic-ohlcv-exports/contracts`, and metadata-only `GET /synthetic-ohlcv-exports/sample`.
- `stark_terminal_api.routes.provider_guardrails`: Implements safe `GET /provider-guardrails/health`, `GET /provider-guardrails/contracts`, and template-only `GET /provider-guardrails/readiness-template`.
- `stark_terminal_api.routes.provider_readiness`: Implements safe `GET /provider-readiness/health`, `GET /provider-readiness/contracts`, `GET /provider-readiness/template`, and generic `GET /provider-readiness/example-score`.
- `stark_terminal_api.routes.local_sample_provider`: Implements safe `GET /local-sample-provider/health`, `GET /local-sample-provider/contracts`, `GET /local-sample-provider/instruments`, and tiny synthetic-only `GET /local-sample-provider/sample-bars`.
- `stark_terminal_api.routes.local_file_provider`: Implements safe `GET /local-file-provider/health` and `GET /local-file-provider/contracts`; no arbitrary file read API.
- `stark_terminal_api.routes.workers`: Implements safe `GET /workers/health`.
- `stark_terminal_api.routes.instruments`: Implements safe `GET /instruments/health`, `GET /providers/health`, and synthetic-only `GET /instruments/sample`.
- `stark_terminal_api.routes.warehouse`: Implements safe `GET /warehouse/health` and `GET /warehouse/contracts`.
- `stark_terminal_api.routes.features`: Implements safe `GET /features/health` and `GET /features/contracts`.
- `stark_terminal_desktop.main`: Provides a minimal PySide6 shell when PySide6 is installed and a clear fallback message when unavailable.
- `stark_terminal_core.config.settings`: Defines typed settings and safe configuration snapshots.
- `stark_terminal_core.domain.enums`: Defines core domain enums.
- `stark_terminal_core.domain.identifiers`: Defines InstrumentId, DataProviderId, and AuditId.
- `stark_terminal_core.domain.instrument`: Defines Instrument.
- `stark_terminal_core.domain.market_data`: Defines MarketDataBar and MarketDataBatch.
- `stark_terminal_core.domain.market_data_batch`: Defines `MarketDataBatchMetadata`, `MarketDataBatchPersistenceResult`, and metadata construction helpers.
- `stark_terminal_core.domain.market_data_contracts`: Defines MarketDataRequest and MarketDataResponse contracts.
- `stark_terminal_core.domain.derivatives`: Defines FuturesContract.
- `stark_terminal_core.domain.options`: Defines OptionContract and OptionsChainSnapshot.
- `stark_terminal_core.domain.audit`: Defines AuditMetadata.
- `stark_terminal_core.domain.decision_object`: Defines the enriched Pydantic DecisionObject schema placeholder.
- `stark_terminal_core.serialization.json`: Defines JSON-safe serialization helpers.
- `stark_terminal_data_platform.db.base`: Defines SQLAlchemy declarative base and common mixins.
- `stark_terminal_data_platform.db.engine`: Builds PostgreSQL-ready SQLAlchemy engines with SQLite fallback for tests/dev.
- `stark_terminal_data_platform.db.session`: Defines session factories and FastAPI-compatible session dependency.
- `stark_terminal_data_platform.db.health`: Defines database health status checks.
- `stark_terminal_data_platform.db.models.instrument`: Defines `InstrumentORM`.
- `stark_terminal_data_platform.db.models.data_provider`: Defines `DataProviderORM`.
- `stark_terminal_data_platform.db.models.audit`: Defines `AuditRecordORM`.
- `stark_terminal_data_platform.db.models.decision`: Defines `DecisionObjectRecordORM`.
- `stark_terminal_data_platform.db.models.timeseries`: Defines operational time-series ORM models for OHLCV bars, options-chain snapshots, futures-basis snapshots, market-state snapshots, and regime snapshots.
- `stark_terminal_data_platform.db.models.market_data_batch`: Defines `MarketDataBatchRecordORM` for metadata-only batch persistence with no full bar columns.
- `stark_terminal_data_platform.timeseries.health`: Defines safe TimescaleDB health/capability checks.
- `stark_terminal_data_platform.timeseries.hypertables`: Defines non-executing TimescaleDB extension and hypertable SQL helpers.
- `stark_terminal_data_platform.lake.paths`: Defines cross-platform lake path helpers.
- `stark_terminal_data_platform.lake.zones`: Defines canonical Parquet zone mapping.
- `stark_terminal_data_platform.lake.manifest`: Defines dataset manifest contracts.
- `stark_terminal_data_platform.lake.duckdb_client`: Defines local DuckDB query helpers.
- `stark_terminal_data_platform.lake.parquet_io`: Defines small Parquet read/write helpers.
- `stark_terminal_data_platform.lake.registry`: Defines in-memory dataset registry placeholder.
- `stark_terminal_data_platform.lake.health`: Defines safe research lake health checks.
- `stark_terminal_data_platform.cache.keys` (`cache/keys.py`): Defines cache namespace and key validation policy.
- `stark_terminal_data_platform.cache.serialization`: Defines JSON-safe cache serialization helpers.
- `stark_terminal_data_platform.cache.memory`: Defines local/test in-memory cache fallback.
- `stark_terminal_data_platform.cache.client`: Defines Redis/memory cache client wrapper.
- `stark_terminal_data_platform.cache.health`: Defines safe Redis cache health checks.
- `stark_terminal_data_platform.streams.names` (`streams/names.py`): Defines Redis Streams namespace and stream name validation policy.
- `stark_terminal_data_platform.streams.events`: Defines typed EventEnvelope contracts and field mapping helpers.
- `stark_terminal_data_platform.streams.serialization`: Defines JSON-safe stream serialization helpers and secret-key guards.
- `stark_terminal_data_platform.streams.memory`: Defines local/test in-memory stream fallback.
- `stark_terminal_data_platform.streams.producer`: Defines Redis/memory stream producer wrapper.
- `stark_terminal_data_platform.streams.consumer`: Defines Redis/memory stream consumer wrapper.
- `stark_terminal_data_platform.streams.health`: Defines safe Redis Streams health checks.
- `stark_terminal_data_platform.event_backbone.topics` (`event_backbone/topics.py`): Defines Kafka/Redpanda topic naming policy.
- `stark_terminal_data_platform.event_backbone.envelopes`: Defines DurableEventEnvelope and Redis Streams EventEnvelope compatibility helpers.
- `stark_terminal_data_platform.event_backbone.serialization`: Defines JSON-safe durable event serialization helpers and secret-key guards.
- `stark_terminal_data_platform.event_backbone.memory`: Defines local/test in-memory event backbone fallback.
- `stark_terminal_data_platform.event_backbone.producer`: Defines Kafka/Redpanda/memory event backbone producer wrapper.
- `stark_terminal_data_platform.event_backbone.consumer`: Defines Kafka/Redpanda/memory event backbone consumer wrapper.
- `stark_terminal_data_platform.event_backbone.health`: Defines safe Kafka/Redpanda Event Backbone health checks.
- `stark_terminal_data_platform.quality.enums`: Defines validation severity, status, scope, quality gate, and rule type enums.
- `stark_terminal_data_platform.quality.issues`: Defines ValidationIssue contracts and sanitization helpers.
- `stark_terminal_data_platform.quality.rules`: Defines ValidationRule contracts and helper constructors.
- `stark_terminal_data_platform.quality.results`: Defines ValidationResult contracts and result helper constructors.
- `stark_terminal_data_platform.quality.reports`: Defines ValidationReport contracts, report builders, and summary helpers.
- `stark_terminal_data_platform.quality.gates`: Defines QualityGatePolicy, QualityGateResult, and gate evaluation helpers.
- `stark_terminal_data_platform.quality.validators`: Defines the BaseValidator interface.
- `stark_terminal_data_platform.quality.builtins`: Defines built-in validators for existing local contracts.
- `stark_terminal_data_platform.quality.registry`: Defines the explicit in-memory ValidationRegistry.
- `stark_terminal_data_platform.quality.health`: Defines safe Data Quality health checks.
- `stark_terminal_data_platform.fixtures.manifests`: Defines synthetic fixture manifest contracts.
- `stark_terminal_data_platform.fixtures.synthetic_ohlcv`: Defines deterministic local synthetic OHLCV generation and MarketDataBatch helpers.
- `stark_terminal_data_platform.fixtures.catalog`: Defines an explicit synthetic fixture catalog.
- `stark_terminal_data_platform.fixtures.validation`: Defines fixture validation helpers using the Data Quality Framework.
- `stark_terminal_data_platform.fixtures.parquet`: Defines tiny explicit Parquet fixture roundtrip helpers for tests/local use.
- `stark_terminal_data_platform.fixtures.health`: Defines safe synthetic fixture health checks.
- `stark_terminal_data_platform.repositories.instruments`: Defines `InstrumentRepository` for metadata-only SQLAlchemy instrument persistence.
- `stark_terminal_data_platform.repositories.market_data_batches`: Defines `MarketDataBatchRepository` for metadata-only SQLAlchemy batch records.
- `stark_terminal_data_platform.repositories.ohlcv_bars`: Defines `OHLCVBarRepository` for synthetic-only OHLCV bar persistence through the existing time-series ORM.
- `stark_terminal_data_platform.services.instruments`: Defines `InstrumentMetadataService`, validation-before-persistence, synthetic instrument seeding, and safe persistence health checks.
- `stark_terminal_data_platform.services.market_data_batches`: Defines `MarketDataBatchMetadataService`, validation-before-persistence, synthetic batch metadata persistence, and safe persistence health checks.
- `stark_terminal_data_platform.services.synthetic_ohlcv_storage`: Defines `SyntheticOHLCVStorageService`, validation-before-storage, and synthetic-only OHLCV storage health.
- `stark_terminal_data_platform.exports.synthetic_ohlcv`: Defines `SyntheticOHLCVResearchLakeExportService`, export request/result contracts, DatasetManifest creation, validation-before-export, Parquet export, and DuckDB readback.
- `stark_terminal_data_platform.workers.roles` (`workers/roles.py`): Defines canonical worker roles, queue mapping, role descriptions, and forbidden execution-role detection.
- `stark_terminal_data_platform.workers.jobs` (`workers/jobs.py`): Defines typed JobEnvelope contracts and safe job payload validation.
- `stark_terminal_data_platform.workers.results` (`workers/results.py`): Defines WorkerResult contracts and sanitized result helpers.
- `stark_terminal_data_platform.workers.base` (`workers/base.py`): Defines BaseWorker plus no-op, echo, and failing local/test workers.
- `stark_terminal_data_platform.workers.registry` (`workers/registry.py`): Defines an explicit WorkerRegistry with no global mutable registry.
- `stark_terminal_data_platform.workers.harness` (`workers/harness.py`): Defines a deterministic in-process worker harness for local/test use.
- `stark_terminal_data_platform.workers.health` (`workers/health.py`): Defines safe Worker System health checks.
- `stark_terminal_data_platform.instruments.normalization` (`instruments/normalization.py`): Defines symbol, exchange, segment, and instrument-key normalization.
- `stark_terminal_data_platform.instruments.universe`: Defines InstrumentUniverseSnapshot and universe lookup/filter helpers.
- `stark_terminal_data_platform.instruments.master`: Defines InstrumentMaster and LocalInstrumentMaster contracts.
- `stark_terminal_data_platform.instruments.fixtures`: Defines synthetic/local instrument fixtures for tests only.
- `stark_terminal_data_platform.instruments.health`: Defines safe Instrument Master health checks.
- `stark_terminal_data_platform.providers.contracts`: Defines ProviderCapabilityReport.
- `stark_terminal_data_platform.providers.base`: Defines read-only MarketDataProvider and LocalSampleMarketDataProvider contracts.
- `stark_terminal_data_platform.providers.guardrails`: Defines Provider Adapter Guardrail policy/result/health contracts and guardrail evaluation helpers.
- `stark_terminal_data_platform.providers.approval`: Defines ProviderApprovalRecord and approval workflow helpers.
- `stark_terminal_data_platform.providers.readiness`: Defines ProviderComplianceChecklist, ProviderReadinessReport, and readiness helpers.
- `stark_terminal_data_platform.providers.candidates`: Defines provider candidate profiles, checklists, statuses, data access methods, and guardrail blocker helpers.
- `stark_terminal_data_platform.providers.selection`: Defines provider selection criteria, capability gaps, deterministic risk scoring, in-memory candidate registry, and readiness health.
- `stark_terminal_data_platform.providers.local_sample`: Defines Local Sample Provider Adapter v0, guardrail-protected synthetic instrument master and historical bar responses, health status, and helpers.
- `stark_terminal_data_platform.providers.local_file`: Defines Local File Provider Adapter v0, `LocalFileSource`, path safety helpers, CSV/Parquet local readers, guardrail-protected local file responses, health status, and helpers.
- `stark_terminal_data_platform.providers.registry`: Defines an explicit ProviderRegistry with no global mutable registry.
- `stark_terminal_data_platform.providers.health`: Defines safe provider contract health checks.
- `stark_terminal_data_platform.warehouse.tables` (`warehouse/tables.py`): Defines ClickHouse analytical table contracts.
- `stark_terminal_data_platform.warehouse.ddl`: Defines deterministic ClickHouse DDL string helpers.
- `stark_terminal_data_platform.warehouse.memory`: Defines a local/test memory query recorder.
- `stark_terminal_data_platform.warehouse.client`: Defines a disabled-safe ClickHouse warehouse client wrapper.
- `stark_terminal_data_platform.warehouse.health`: Defines safe ClickHouse Warehouse health checks.
- `stark_terminal_data_platform.features.definitions` (`features/definitions.py`): Defines FeatureDefinition and FeatureDependency contracts.
- `stark_terminal_data_platform.features.feature_sets`: Defines FeatureSet contracts.
- `stark_terminal_data_platform.features.values`: Defines FeatureEntity, FeatureValue, and FeatureSnapshot contracts.
- `stark_terminal_data_platform.features.quality`: Defines FeatureQualityReport contracts and summary helper.
- `stark_terminal_data_platform.features.lineage`: Defines FeatureLineageRecord contracts.
- `stark_terminal_data_platform.features.registry`: Defines the in-memory Stark Feature Registry foundation.
- `stark_terminal_data_platform.features.health`: Defines safe Feature Registry health checks.
- `alembic/`: Alembic migration environment, initial metadata migration, and operational time-series migration.
- `scripts/audit_foundation.py`: Runs deterministic local foundation and data-foundation audit checks for docs, package directories, route files, forbidden route names, Prompt 14-22 data safety artifacts, safety phrases, prompt log, and North Star status.
- `scripts/verify_foundation.py`: Verifies required files, institutional keywords, Prompt 18-22 audit checks, and pytest.

## Prompt 11 Audit Artifacts

- `docs/MILESTONE_A_B_AUDIT.md`: Milestone A/B audit scope, verdicts, known issues, and readiness status.
- `docs/REPO_INVENTORY.md`: Current repo inventory for apps, packages, docs, scripts, and tests.
- `docs/API_SURFACE_INVENTORY.md`: Read-only API endpoint inventory with external-call, secret, mutation, and safety posture.
- `docs/SAFETY_AUDIT.md`: Execution, broker, credential, external-call, provider, cache/stream/worker, and future safety-gate audit.
- `docs/NEXT_PHASE_PLAN.md`: Next prompt recommendation and short infrastructure roadmap.

Prompt 11 adds audit tooling and documentation only. It does not add product capability, no execution APIs, no real market ingestion, no external calls, and Kafka/Redpanda not implemented yet.

## Prompt 12 Event Backbone Artifacts

- `docs/KAFKA_REDPANDA_FOUNDATION.md`: Kafka/Redpanda Event Backbone foundation scope and boundaries.
- `docs/EVENT_BACKBONE_TOPIC_POLICY.md`: Topic naming policy and default namespaces.
- `docs/DURABLE_EVENT_ENVELOPE_SPEC.md`: DurableEventEnvelope fields and Redis Streams compatibility rules.
- `packages/data_platform/stark_terminal_data_platform/event_backbone/`: Topic helpers, durable envelopes, serialization, memory fallback, producer/consumer wrappers, and health checks.
- `apps/api/stark_terminal_api/routes/event_backbone.py`: API health and topic contract route.

Prompt 12 adds Kafka/Redpanda Event Backbone contracts only. It does not add production event pipelines, real market ingestion, schema registry integration, ClickHouse ingestion, Feature Store computation pipelines, analytics engines, or execution APIs.

## Prompt 13 Data Quality Artifacts

- `docs/DATA_QUALITY_FRAMEWORK.md`: Data Quality + Validation Framework scope and boundaries.
- `docs/VALIDATION_RULE_SPEC.md`: ValidationIssue, ValidationRule, ValidationResult, and ValidationReport contracts.
- `docs/QUALITY_GATE_POLICY.md`: Quality gate policy and ALLOW/WARN/BLOCK behavior.
- `docs/DATA_QUALITY_REPORT_SPEC.md`: Validation report fields, counts, source references, and auditability.
- `packages/data_platform/stark_terminal_data_platform/quality/`: Enums, issues, rules, results, reports, gates, validator base, built-ins, registry, and health checks.
- `apps/api/stark_terminal_api/routes/data_quality.py`: API health and contract route.

Prompt 13 adds the Data Quality + Validation Framework only. It does not add real market ingestion, production validation pipelines, external validation calls, analytics signals, feature computation, models, decisions, or execution APIs.

## Prompt 14 Synthetic Fixture Artifacts

- `docs/SYNTHETIC_MARKET_DATA_FIXTURES.md`: Synthetic fixture purpose, deterministic generation, and no-real-data boundary.
- `docs/OHLCV_FIXTURE_CONTRACTS.md`: SyntheticOHLCVConfig, MarketDataBar, MarketDataBatch, OHLC constraints, timestamp rules, and validation expectations.
- `docs/SAMPLE_DATA_POLICY.md`: Sample data safety policy, no scraping, no external calls, and disk-write boundary.
- `packages/data_platform/stark_terminal_data_platform/fixtures/`: Manifest schemas, deterministic OHLCV generation, catalog, validation helpers, Parquet test helpers, and health checks.
- `apps/api/stark_terminal_api/routes/fixtures.py`: API health and synthetic catalog metadata route.

Prompt 14 adds synthetic local-only test/dev fixtures only. It does not add real market data ingestion, provider clients, scraping, production dataset writes, analytics signals, feature computation, backtesting, decisions, or execution APIs.

## Prompt 15 Instrument Metadata Persistence Artifacts

- `docs/INSTRUMENT_PERSISTENCE_FOUNDATION.md`: Instrument metadata persistence purpose, PostgreSQL/SQLite role, repository/service split, validation-before-persistence, and safety boundaries.
- `docs/INSTRUMENT_REPOSITORY_POLICY.md`: Repository and service responsibilities, normalization rules, transaction ownership, and no-external-call policy.
- `packages/data_platform/stark_terminal_data_platform/repositories/`: Metadata persistence repository package.
- `packages/data_platform/stark_terminal_data_platform/repositories/instruments.py`: `InstrumentRepository` for idempotent upsert/list/get/search/count/delete operations.
- `packages/data_platform/stark_terminal_data_platform/services/`: Service-layer package.
- `packages/data_platform/stark_terminal_data_platform/services/instruments.py`: `InstrumentMetadataService` with validation gates, commit/rollback ownership, synthetic seeding, and health status.
- `apps/api/stark_terminal_api/routes/instrument_metadata.py`: API health, synthetic sample, and fail-safe read-only list routes.

Prompt 15 adds Instrument Metadata Persistence Wiring only. It does not add real market data ingestion, external provider calls, provider clients, OHLCV persistence, TimescaleDB writes, ClickHouse writes, event publishing, analytics signals, feature computation, backtesting, decisions, or execution APIs.

## Prompt 16 Market Data Batch Persistence Artifacts

- `docs/MARKET_DATA_BATCH_PERSISTENCE.md`: Market Data Batch Persistence scope, metadata-only persistence boundary, validation-before-persistence, and future storage ownership.
- `docs/BATCH_METADATA_POLICY.md`: Batch metadata identity, source reference, synthetic, fixture, validation report, and no-full-bars policy.
- `packages/core/stark_terminal_core/domain/market_data_batch.py`: `MarketDataBatchMetadata`, `MarketDataBatchPersistenceResult`, and helpers for safe metadata construction from `MarketDataBatch`.
- `packages/data_platform/stark_terminal_data_platform/db/models/market_data_batch.py`: `MarketDataBatchRecordORM` metadata table mapping.
- `packages/data_platform/stark_terminal_data_platform/repositories/market_data_batches.py`: `MarketDataBatchRepository` for idempotent upsert/get/list/search/count/delete operations.
- `packages/data_platform/stark_terminal_data_platform/services/market_data_batches.py`: `MarketDataBatchMetadataService` with validation gates, synthetic batch metadata persistence, and health status.
- `apps/api/stark_terminal_api/routes/market_data_batches.py`: API health, synthetic sample metadata, and fail-safe read-only list routes.
- `alembic/versions/0003_market_data_batch_metadata.py`: Alembic migration for `market_data_batch_records`.

Prompt 16 adds Market Data Batch Persistence Contracts only. It persists batch metadata, not full OHLCV bars. It does not add real market data ingestion, external provider calls, provider clients, TimescaleDB data writes, ClickHouse data writes, DuckDB/Parquet production writes, event publishing, analytics signals, feature computation, backtesting, decisions, or execution APIs.

## Prompt 17 Data Foundation Audit Artifacts

- `docs/DATA_FOUNDATION_AUDIT.md`: Focused audit of Prompts 14-16 covering synthetic fixtures, instrument metadata persistence, market data batch metadata persistence, validation gates, API posture, and readiness.
- `docs/DATA_PERSISTENCE_BOUNDARY.md`: Store ownership and metadata-only persistence boundary for PostgreSQL, TimescaleDB, DuckDB/Parquet, ClickHouse, Redis, Redis Streams, and Kafka/Redpanda.
- `docs/SYNTHETIC_DATA_SAFETY_AUDIT.md`: Synthetic fixture safety audit for labels, deterministic generation, no live data, disk writes, validation, and API posture.
- `docs/DATA_FOUNDATION_NEXT_PHASE.md`: Prompt 19 completion status and next five-prompt data roadmap.
- `tests/test_data_foundation_audit_docs.py`: Data foundation audit document invariant tests.
- `tests/test_data_foundation_no_real_ingestion.py`: No-real-ingestion and no-external-call invariant tests.
- `tests/test_data_foundation_persistence_boundaries.py`: Metadata-only persistence boundary tests.
- `tests/test_data_foundation_api_safety.py`: Fixture/instrument/batch data API safety tests.
- `tests/test_data_foundation_readiness.py`: Audit/verifier/readiness status tests.

Prompt 17 adds audit documentation, script coverage, and invariant tests only. It does not add real market ingestion, provider calls, scraping, full OHLCV production persistence, TimescaleDB bar writes, ClickHouse writes, DuckDB/Parquet production writes, Redis/Kafka publishing, analytics signals, feature computation, decisions, or execution APIs.

## Prompt 18 TimescaleDB Synthetic OHLCV Storage Artifacts

- `docs/SYNTHETIC_OHLCV_STORAGE_FOUNDATION.md`: Synthetic OHLCV Storage Foundation scope, TimescaleDB/SQLite posture, validation-before-storage, and future ingestion boundary.
- `docs/TIMESCALE_SYNTHETIC_STORAGE_POLICY.md`: Synthetic-only Timescale storage policy, `LOCAL_SAMPLE` expectation, no real market data, no external calls, and no execution APIs.
- `packages/data_platform/stark_terminal_data_platform/repositories/ohlcv_bars.py`: `OHLCVBarRepository` for idempotent synthetic bar upsert/get/list/count/delete using `OHLCVBarORM`.
- `packages/data_platform/stark_terminal_data_platform/services/synthetic_ohlcv_storage.py`: `SyntheticOHLCVStorageService`, `SyntheticOHLCVStorageResult`, validation-before-storage, and health status.
- `apps/api/stark_terminal_api/routes/synthetic_ohlcv_storage.py`: Read-only synthetic OHLCV storage health, sample, and contracts endpoints.
- `tests/test_ohlcv_bar_repository.py`: SQLite repository tests for idempotent upsert/query behavior.
- `tests/test_synthetic_ohlcv_storage_service.py`: Service tests for validation, synthetic-only boundaries, idempotency, and health.
- `tests/test_synthetic_ohlcv_storage_validation.py`: Validation tests proving Prompt 13 validators block invalid bars before storage.
- `tests/test_api_synthetic_ohlcv_storage.py`: API safety tests for the new synthetic storage endpoints.
- `tests/test_synthetic_ohlcv_storage_docs_status.py`: Documentation/status/verifier tests for Prompt 18.

Prompt 18 adds TimescaleDB Synthetic OHLCV Storage Foundation only. It stores validated synthetic bars through an ORM/repository/service boundary for tests/dev and does not add real market data ingestion, external provider calls, scraping, ClickHouse writes, DuckDB/Parquet production writes, Redis/Kafka event publishing, analytics signals, feature computation, backtesting, decisions, or execution APIs.

## Prompt 19 Synthetic OHLCV Research Lake Export Artifacts

- `docs/SYNTHETIC_OHLCV_RESEARCH_LAKE_EXPORT.md`: Synthetic OHLCV Research Lake Export scope, DatasetManifest linkage, validation-before-export, Parquet/DuckDB posture, and future ingestion boundary.
- `docs/OHLCV_EXPORT_MANIFEST_POLICY.md`: Export id, dataset name, DatasetManifest, row count, source reference, synthetic flag, partition, and no-real-data export policy.
- `packages/data_platform/stark_terminal_data_platform/exports/synthetic_ohlcv.py`: `SyntheticOHLCVExportRequest`, `SyntheticOHLCVExportResult`, `SyntheticOHLCVResearchLakeExportService`, DatasetManifest creation, Parquet export, DuckDB readback, health status, and helpers.
- `packages/data_platform/stark_terminal_data_platform/exports/README.md`: Export package boundary and non-scope.
- `apps/api/stark_terminal_api/routes/synthetic_ohlcv_exports.py`: Read-only synthetic OHLCV export health, contracts, and metadata-only sample endpoints.
- `tests/test_synthetic_ohlcv_export_contracts.py`: Contract tests for export request/result safety.
- `tests/test_synthetic_ohlcv_export_service.py`: Service tests for temp-path Parquet export and manifest linkage.
- `tests/test_synthetic_ohlcv_export_validation.py`: Validation tests proving invalid or non-synthetic bars are blocked before export.
- `tests/test_synthetic_ohlcv_export_parquet.py`: Parquet/DuckDB readback tests.
- `tests/test_api_synthetic_ohlcv_exports.py`: API safety tests for export endpoints.
- `tests/test_synthetic_ohlcv_export_docs_status.py`: Documentation/status/verifier tests for Prompt 19.

Prompt 19 adds Synthetic OHLCV to Research Lake Export Contract only. It exports validated synthetic bars to explicit temp/test Parquet research artifacts with DatasetManifest linkage and DuckDB readback. It does not add real market data ingestion, external provider calls, scraping, production research lake writes by default, ClickHouse writes, Redis/Kafka event publishing, analytics signals, feature computation, backtesting, decisions, or execution APIs.

## Prompt 20 Provider Adapter Guardrail Artifacts

- `docs/PROVIDER_ADAPTER_IMPLEMENTATION_PLAN.md`: Provider adapter implementation plan, staged future process, approval prerequisites, and no-real-ingestion boundary.
- `docs/PROVIDER_GUARDRAIL_POLICY.md`: Default provider guardrail policy, ALLOW/WARN/BLOCK behavior, and blocking conditions.
- `docs/PROVIDER_APPROVAL_WORKFLOW.md`: Approval statuses, requested/approved capabilities, reviewer requirements, and production approval boundary.
- `docs/PROVIDER_COMPLIANCE_CHECKLIST.md`: Terms, redistribution, storage, attribution, rate-limit, data quality, and audit checklist policy.
- `packages/data_platform/stark_terminal_data_platform/providers/guardrails.py`: `ProviderGuardrailPolicy`, `ProviderGuardrailResult`, guardrail enums, health status, and evaluation helpers.
- `packages/data_platform/stark_terminal_data_platform/providers/approval.py`: `ProviderApprovalRecord`, `create_provider_approval_record`, `approve_for_design`, and `block_provider`.
- `packages/data_platform/stark_terminal_data_platform/providers/readiness.py`: `ProviderComplianceChecklist`, `ProviderReadinessReport`, and readiness helpers.
- `apps/api/stark_terminal_api/routes/provider_guardrails.py`: Read-only provider guardrail health, contracts, and readiness-template endpoints.
- `tests/test_provider_guardrail_contracts.py`: Guardrail policy and evaluation tests.
- `tests/test_provider_approval_workflow.py`: Approval workflow tests.
- `tests/test_provider_readiness.py`: Compliance and readiness report tests.
- `tests/test_api_provider_guardrails.py`: API safety tests for provider guardrail endpoints.
- `tests/test_provider_guardrail_docs_status.py`: Documentation/status tests for Prompt 20.
- `tests/test_provider_no_external_calls_guardrail.py`: No network/scraping/provider SDK dependency tests.

Prompt 20 adds Data Provider Adapter Implementation Plan and Guardrails only. It does not add real provider clients, provider SDKs, scraping, credentials, external provider calls, real market ingestion, analytics signals, feature computation, backtesting, decisions, or execution APIs.

## Prompt 21 Local Sample Provider Adapter Artifacts

- `docs/LOCAL_SAMPLE_PROVIDER_ADAPTER.md`: Local Sample Provider Adapter v0 purpose, supported/unsupported capabilities, guardrail checks, and Data Quality validation boundary.
- `docs/LOCAL_SAMPLE_PROVIDER_POLICY.md`: Synthetic-only source policy, deterministic bars, `LOCAL_SAMPLE` identity, no-network/no-credentials/no-real-data/no-execution rules, and API labeling.
- `packages/data_platform/stark_terminal_data_platform/providers/local_sample.py`: `LocalSampleProviderAdapter`, health status model, guardrail evaluation, synthetic instrument master response, deterministic synthetic historical bars response, and unsupported capability responses.
- `apps/api/stark_terminal_api/routes/local_sample_provider.py`: Read-only local sample provider health, contracts, synthetic instruments, and tiny synthetic sample-bars endpoints.
- `tests/test_local_sample_provider_adapter.py`: Adapter identity, capability, health, instrument master, deterministic historical bar, and unsupported capability tests.
- `tests/test_local_sample_provider_guardrails.py`: Guardrail allow/block tests and fail-closed settings tests.
- `tests/test_local_sample_provider_validation.py`: Data Quality validation and invalid request handling tests.
- `tests/test_api_local_sample_provider.py`: API safety tests for local sample provider endpoints.
- `tests/test_local_sample_provider_docs_status.py`: Documentation/status tests for Prompt 21.
- `tests/test_local_sample_provider_no_external_calls.py`: Static no-network/no-scraping/no-provider-SDK/no-broker-dependency tests.

Prompt 21 adds Local Sample Provider Adapter v0 only. It is synthetic, local-only, test/dev only, read-only, and guardrail-protected. It does not add real provider clients, provider SDKs, scraping, credentials, external provider calls, real market ingestion, persistence writes, event publishing, analytics signals, feature computation, backtesting, decisions, or execution APIs.

## Prompt 22 Data Foundation Milestone Audit Artifacts

- `docs/DATA_FOUNDATION_MILESTONE_AUDIT.md`: Milestone audit of Prompts 18-21 covering synthetic OHLCV storage, research lake export, provider guardrails, Local Sample Provider Adapter v0, API posture, and readiness.
- `docs/SYNTHETIC_STORAGE_EXPORT_AUDIT.md`: Synthetic storage/export boundary audit for validation-before-storage/export, DatasetManifest linkage, temp/test paths, no live TimescaleDB requirement, no production research lake writes by default, and no analytics/signals/decisions.
- `docs/PROVIDER_GUARDRAIL_AUDIT.md`: Provider guardrail safety audit for fail-closed network, scraping, credentials, execution, approval, compliance, and no-real-provider status.
- `docs/LOCAL_SAMPLE_PROVIDER_AUDIT.md`: Local Sample Provider Adapter v0 audit for supported/unsupported capabilities, synthetic labels, no external calls, no scraping, no credentials, and no real market data.
- `docs/DATA_FOUNDATION_MILESTONE_NEXT_PHASE.md`: Prompt 23 recommendation and next five-prompt sequence.
- `tests/test_data_foundation_milestone_audit_docs.py`: Milestone audit document invariant tests.
- `tests/test_synthetic_storage_export_boundaries.py`: Synthetic storage/export boundary tests.
- `tests/test_provider_guardrail_milestone_safety.py`: Provider guardrail milestone safety tests.
- `tests/test_local_sample_provider_milestone_safety.py`: Local sample provider milestone safety tests.
- `tests/test_data_foundation_milestone_api_safety.py`: API safety tests for Prompt 18-21 endpoints.
- `tests/test_data_foundation_milestone_readiness.py`: Readiness/status/audit/verifier tests for Prompt 22.

Prompt 22 adds audit documentation, script coverage, and invariant tests only. It does not add real market ingestion, external provider calls, scraping, credentials, live provider clients, provider SDKs, production research lake writes by default, production event publishing, analytics signals, feature computation, backtesting, decisions, or execution APIs.

## Prompt 23 Real Provider Readiness Checklist And Candidate Selection Artifacts

- `docs/REAL_PROVIDER_READINESS_CHECKLIST.md`: Readiness checklist purpose, required provider/compliance metadata, and no-real-implementation boundary.
- `docs/PROVIDER_CANDIDATE_SELECTION_POLICY.md`: Candidate status, data access methods, selection process, and blocked real-provider modes.
- `docs/PROVIDER_RISK_SCORING_POLICY.md`: Deterministic scoring model, blockers, warnings, and readiness thresholds.
- `docs/PROVIDER_CAPABILITY_GAP_ANALYSIS.md`: Required vs present capability gap rules and safety boundary.
- `packages/data_platform/stark_terminal_data_platform/providers/candidates.py`: `ProviderCandidateProfile`, `ProviderCandidateChecklist`, provider candidate status/data-access enums, and guardrail blocker helper.
- `packages/data_platform/stark_terminal_data_platform/providers/selection.py`: `ProviderSelectionCriteria`, `ProviderCapabilityGap`, `ProviderCandidateScore`, `ProviderCandidateRegistry`, risk scoring, gap analysis, thresholds, and health status.
- `apps/api/stark_terminal_api/routes/provider_readiness.py`: Read-only provider readiness health, contracts, template, and generic example-score endpoints.
- `tests/test_provider_candidate_profiles.py`: Candidate profile/checklist validation tests.
- `tests/test_provider_selection_criteria.py`: Conservative selection criteria tests.
- `tests/test_provider_risk_scoring.py`: Deterministic scoring and blocker tests.
- `tests/test_provider_capability_gap_analysis.py`: Capability gap analysis tests.
- `tests/test_provider_candidate_registry.py`: In-memory registry tests.
- `tests/test_api_provider_readiness.py`: API safety tests for provider readiness endpoints.
- `tests/test_provider_readiness_docs_status.py`: Documentation/status tests for Prompt 23.
- `tests/test_provider_readiness_no_external_calls.py`: Static no-network/no-SDK/no-scraping/no-broker dependency tests.

Prompt 23 adds Real Provider Readiness Checklist and Candidate Selection only. It does not add real provider clients, provider SDKs, scraping, credentials, external provider calls, real market ingestion, production approval, analytics signals, feature computation, backtesting, decisions, or execution APIs.

## Prompt 24 Local File Provider Adapter Artifacts

- `docs/LOCAL_FILE_PROVIDER_ADAPTER.md`: Local File Provider Adapter v0 purpose, local-file-only behavior, supported formats/capabilities, unsupported capabilities, path safety, guardrail checks, and Data Quality validation boundary.
- `docs/LOCAL_FILE_PROVIDER_POLICY.md`: Local/test/dev-only source policy, explicit file paths, no auto-discovery, no network paths, no credentials, no execution behavior, no trading interpretation, and no arbitrary file read API.
- `docs/LOCAL_FILE_PATH_SAFETY.md`: Allowed root, `pathlib` usage, path traversal rejection, symlink escape handling, file extension allowlist, max rows, and API file-read boundary.
- `packages/data_platform/stark_terminal_data_platform/providers/local_file.py`: `LocalFileSource`, path safety helpers, CSV/Parquet local readers, `LocalFileProviderAdapter`, health status model, guardrail evaluation, local instrument master response, local historical bars response, and unsupported capability responses.
- `apps/api/stark_terminal_api/routes/local_file_provider.py`: Read-only local file provider health and contracts endpoints; no file-read endpoint and no path parameters.
- `tests/test_local_file_provider_contracts.py`: Local file source schema and sanitization tests.
- `tests/test_local_file_provider_path_safety.py`: Allowed-root, traversal, network path, extension, missing file, absolute escape, and symlink escape tests.
- `tests/test_local_file_provider_adapter.py`: Adapter identity, capability, health, instrument master, historical bar, deterministic read, max rows, and unsupported capability tests.
- `tests/test_local_file_provider_validation.py`: Data Quality validation, invalid OHLC, invalid instrument, and invalid request tests.
- `tests/test_api_local_file_provider.py`: API safety tests for local file provider endpoints.
- `tests/test_local_file_provider_docs_status.py`: Documentation/status/verifier tests for Prompt 24.
- `tests/test_local_file_provider_no_external_calls.py`: Static no-network/no-scraping/no-provider-SDK/no-broker-dependency tests.

Prompt 24 adds Local File Provider Adapter v0 only. It is local-file-only, test/dev only, read-only, path-safe, and guardrail-protected. It does not add real provider clients, provider SDKs, scraping, credentials, external provider calls, arbitrary file read API behavior, real market ingestion, persistence writes, event publishing, analytics signals, feature computation, backtesting, decisions, or execution APIs.

## Prompt 25 Provider Adapter Milestone Audit Artifacts

- `docs/PROVIDER_ADAPTER_MILESTONE_AUDIT.md`: Provider milestone audit of Prompts 20-24 covering guardrails, readiness/candidate selection, Local Sample Provider, Local File Provider, API posture, imports/dependencies, path safety, and readiness.
- `docs/PROVIDER_BOUNDARY_AUDIT.md`: Provider boundary audit explaining what provider code can and cannot do today before real provider work.
- `docs/PROVIDER_NO_EXTERNAL_CALLS_AUDIT.md`: No-external-calls audit covering provider imports, dependency posture, network path rejection, API posture, and deterministic tests.
- `docs/PROVIDER_NEXT_PHASE_PLAN.md`: Prompt 26 recommendation and next five-prompt analytics-planning sequence.
- `tests/test_provider_adapter_milestone_audit_docs.py`: Provider milestone audit document invariant tests.
- `tests/test_provider_no_external_calls_milestone.py`: Provider module and API no-external-call invariant tests.
- `tests/test_provider_no_sdk_or_scraping_dependencies.py`: Provider SDK, scraping, and broker/trading dependency boundary tests.
- `tests/test_provider_api_milestone_safety.py`: API safety tests for provider health/contracts/template/sample endpoints.
- `tests/test_provider_boundary_readiness.py`: Provider boundary tests for local sample, local file, readiness governance, production approval, and execution exclusions.
- `tests/test_provider_adapter_milestone_readiness.py`: Audit/verifier/readiness status tests for Prompt 25.

Prompt 25 adds audit documentation, script coverage, and invariant tests only. It does not add real provider clients, provider SDKs, scraping, credentials, external provider calls, real market ingestion, production approval, arbitrary file read API behavior, persistence writes, event publishing, analytics signals, feature computation, backtesting, decisions, or execution APIs.

## Future Modules Not Yet Implemented

- Additional PostgreSQL system-of-record repositories beyond instrument metadata and batch metadata.
- Live TimescaleDB deployment and actual hypertable execution.
- Real market data ingestion into operational time-series storage.
- Real NSE/BSE instrument master ingestion.
- Provider-specific live clients, provider SDKs, and external data calls.
- Real market datasets in DuckDB/Parquet research lake.
- Real analytical ingestion into ClickHouse.
- Production analytical dashboards and rollups.
- Production Kafka or Redpanda event pipelines.
- Feast integration and external feature store backends.
- Real feature computation pipelines and model-ready feature materialization.
- Actual production worker loops, deployment, schedulers, and stream-to-worker wiring.
- Persistent Feature Registry backends beyond the Prompt 10 in-memory registry.
- Production market-data provider adapters and real instrument master ingestion.
- Real ingestion, normalization, feature, regime, options, risk, decision, backtest, paper lab, and audit worker implementations.
- Production validation pipelines and persisted validation report stores.
- Real production sample datasets; Prompt 14 fixtures are synthetic local-only test/dev data.
- Quant analytics, statistical models, ML models, optimization, options analytics, backtesting, risk analytics, and Paper Lab workflows.
- Retail Decision Console, Quant Lab, Options Desk, Backtest Lab, Risk Lab, Data Lab, Journal, Settings, and System Health UI surfaces.

Missing modules are intentionally deferred. Prompt 25 implements only the provider adapter milestone audit. It does not implement real market-data ingestion, real provider calls, provider-specific live clients, provider SDKs, scraping, credentials, production OHLCV ingestion, production research lake writes by default, real ClickHouse table creation, production dashboard analytics, external validation calls, real production worker loops, Redis Streams worker wiring, production Kafka/Redpanda pipelines, production validation pipelines, Feast integration, feature computation, analytics signals, analytics engines, or execution APIs.

The documentation locks the target institutional stack before implementation so later prompts can add systems in a controlled, testable order without scope drift.
