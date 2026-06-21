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
- `packages/data_platform/`: SQLAlchemy/Alembic database foundation, TimescaleDB schema helpers, DuckDB/Parquet lake helpers, Redis cache foundation, Redis Streams foundation, Kafka/Redpanda Event Backbone foundation, Data Quality + Validation Framework, Worker System foundation, Instrument Master/Market Data Provider Contracts, ClickHouse Warehouse foundation, and Feature Registry foundation.
- `packages/analytics/`: Placeholder for future numerical, statistical, ML, optimization, options, risk, and backtesting analytics.
- `packages/research/`: Placeholder for future Paper Lab, StrategyCandidate generation, experiment tracking, and research artifact logic.
- `tests/`: Foundation, typed settings, API, domain contract, and audit invariant tests.
- `scripts/`: Repository audit and verification scripts.

## Current Implemented Modules

- `stark_terminal_api.main`: Creates the FastAPI `app` and registers health/config/database/timeseries/research-lake/cache/streams/event-backbone/data-quality/workers/instruments/warehouse/features routers.
- `stark_terminal_api.routes.health`: Implements `GET /health`.
- `stark_terminal_api.routes.config`: Implements safe `GET /config`.
- `stark_terminal_api.routes.database`: Implements safe `GET /database/health`.
- `stark_terminal_api.routes.research_lake`: Implements safe `GET /research-lake/health`.
- `stark_terminal_api.routes.timeseries`: Implements safe `GET /timeseries/health`.
- `stark_terminal_api.routes.cache`: Implements safe `GET /cache/health`.
- `stark_terminal_api.routes.streams`: Implements safe `GET /streams/health`.
- `stark_terminal_api.routes.event_backbone`: Implements safe `GET /event-backbone/health` and `GET /event-backbone/topics`.
- `stark_terminal_api.routes.data_quality`: Implements safe `GET /data-quality/health` and `GET /data-quality/contracts`.
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
- `scripts/audit_foundation.py`: Runs deterministic local Milestone A/B audit checks for docs, package directories, route files, forbidden route names, safety phrases, prompt log, and North Star status.
- `scripts/verify_foundation.py`: Verifies required files, institutional keywords, audit checks, and pytest.

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

## Future Modules Not Yet Implemented

- PostgreSQL system-of-record repositories.
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
- Production instrument master persistence and market-data provider adapters.
- Real ingestion, normalization, feature, regime, options, risk, decision, backtest, paper lab, and audit worker implementations.
- Production validation pipelines and persisted validation report stores.
- Quant analytics, statistical models, ML models, optimization, options analytics, backtesting, risk analytics, and Paper Lab workflows.
- Retail Decision Console, Quant Lab, Options Desk, Backtest Lab, Risk Lab, Data Lab, Journal, Settings, and System Health UI surfaces.

Missing modules are intentionally deferred. Prompt 13 implements Data Quality + Validation Framework contracts only. It does not implement real market-data ingestion, real ClickHouse table creation, production dashboard analytics, external validation calls, external provider calls, scraping, real production worker loops, Redis Streams worker wiring, production Kafka/Redpanda pipelines, production validation pipelines, Feast integration, feature computation, analytics signals, analytics engines, or execution APIs.

The documentation locks the target institutional stack before implementation so later prompts can add systems in a controlled, testable order without scope drift.
