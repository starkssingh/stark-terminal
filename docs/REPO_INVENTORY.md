# Repo Inventory

This repo inventory captures the Prompt 11 Milestone A/B audit baseline. It should be updated during future milestone audits.

## Apps API Inventory

- `apps/api/stark_terminal_api/main.py`: FastAPI app construction and router registration.
- `apps/api/stark_terminal_api/routes/health.py`: `GET /health`.
- `apps/api/stark_terminal_api/routes/config.py`: `GET /config`.
- `apps/api/stark_terminal_api/routes/database.py`: `GET /database/health`.
- `apps/api/stark_terminal_api/routes/timeseries.py`: `GET /timeseries/health`.
- `apps/api/stark_terminal_api/routes/research_lake.py`: `GET /research-lake/health`.
- `apps/api/stark_terminal_api/routes/cache.py`: `GET /cache/health`.
- `apps/api/stark_terminal_api/routes/streams.py`: `GET /streams/health`.
- `apps/api/stark_terminal_api/routes/event_backbone.py`: `GET /event-backbone/health`, `GET /event-backbone/topics`.
- `apps/api/stark_terminal_api/routes/data_quality.py`: `GET /data-quality/health`, `GET /data-quality/contracts`.
- `apps/api/stark_terminal_api/routes/fixtures.py`: `GET /fixtures/health`, `GET /fixtures/catalog`.
- `apps/api/stark_terminal_api/routes/instrument_metadata.py`: `GET /instrument-metadata/health`, `GET /instrument-metadata/sample`, `GET /instrument-metadata/list`.
- `apps/api/stark_terminal_api/routes/market_data_batches.py`: `GET /market-data-batches/health`, `GET /market-data-batches/sample`, `GET /market-data-batches/list`.
- `apps/api/stark_terminal_api/routes/synthetic_ohlcv_storage.py`: `GET /synthetic-ohlcv-storage/health`, `GET /synthetic-ohlcv-storage/sample`, `GET /synthetic-ohlcv-storage/contracts`.
- `apps/api/stark_terminal_api/routes/synthetic_ohlcv_exports.py`: `GET /synthetic-ohlcv-exports/health`, `GET /synthetic-ohlcv-exports/contracts`, `GET /synthetic-ohlcv-exports/sample`.
- `apps/api/stark_terminal_api/routes/workers.py`: `GET /workers/health`.
- `apps/api/stark_terminal_api/routes/instruments.py`: `GET /instruments/health`, `GET /providers/health`, `GET /instruments/sample`.
- `apps/api/stark_terminal_api/routes/warehouse.py`: `GET /warehouse/health`, `GET /warehouse/contracts`.
- `apps/api/stark_terminal_api/routes/features.py`: `GET /features/health`, `GET /features/contracts`.

## Apps Desktop Inventory

- `apps/desktop/stark_terminal_desktop/main.py`: portable PySide6 shell placeholder with fallback behavior when PySide6 is not installed.

## Core Package Inventory

- `packages/core/stark_terminal_core/config/settings.py`: typed settings and safe settings snapshot.
- `packages/core/stark_terminal_core/domain/`: enums, identifiers, instrument, market data, market data batch metadata, market data contracts, derivatives, options, audit metadata, and DecisionObject schema.
- `packages/core/stark_terminal_core/serialization/json.py`: JSON-safe serialization helpers.

## Data Platform Inventory

- `db`: SQLAlchemy/Alembic metadata foundation and health checks.
- `timeseries`: TimescaleDB capability checks and hypertable SQL helpers.
- `lake`: DuckDB/Parquet research lake paths, zones, manifests, IO, registry, and health checks.
- `cache`: Redis cache key policy, serialization, memory fallback, client wrapper, and health checks.
- `streams`: Redis Streams naming, EventEnvelope, serialization, memory fallback, producer/consumer wrappers, and health checks.
- `event_backbone`: Kafka/Redpanda topic naming, DurableEventEnvelope compatibility helpers, serialization, memory fallback, producer/consumer wrappers, and health checks.
- `quality`: Data Quality + Validation Framework enums, issues, rules, results, reports, gates, validators, built-ins, registry, and health checks.
- `fixtures`: synthetic fixture manifests, deterministic OHLCV generation, catalog, validation helpers, tiny explicit Parquet test roundtrips, and health checks.
- `repositories`: explicit SQLAlchemy repositories, currently `InstrumentRepository` for metadata-only instrument persistence, `MarketDataBatchRepository` for metadata-only batch records, and `OHLCVBarRepository` for synthetic-only bar storage.
- `services`: service-layer workflows, currently `InstrumentMetadataService` for validation-before-persistence and synthetic instrument seeding, `MarketDataBatchMetadataService` for validation-gated synthetic/local batch metadata persistence, and `SyntheticOHLCVStorageService` for synthetic-only OHLCV storage.
- `exports`: synthetic-only research lake export contracts, currently `SyntheticOHLCVResearchLakeExportService` for Parquet/DatasetManifest exports and DuckDB readback.
- `workers`: worker roles, job/result schemas, base workers, registry, in-process harness, and health checks.
- `instruments`: symbol normalization, synthetic fixtures, local master, universe contracts, and health checks.
- `providers`: read-only provider contracts, local sample provider, registry, and health checks.
- `warehouse`: ClickHouse analytical table contracts, DDL helpers, client wrapper, memory query recorder, and health checks.
- `features`: Feature Registry definitions, feature sets, values, quality, lineage, in-memory registry, and health checks.

## Docs Inventory

Documentation covers North Star status, architecture, stack locks, safety, data policy, configuration, domain model, decision object spec, database foundation, TimescaleDB, research lake, Redis cache, Redis Streams, Kafka/Redpanda Event Backbone, Data Quality + Validation Framework, Synthetic Market Data Fixtures, Instrument Metadata Persistence, Market Data Batch Persistence, Synthetic OHLCV Storage, Synthetic OHLCV Research Lake Export, Worker System, Instrument Master, Market Data Provider contracts, ClickHouse Warehouse, Feature Registry, and Prompt 11 audit artifacts.

Prompt 11 audit docs:

- `docs/MILESTONE_A_B_AUDIT.md`
- `docs/REPO_INVENTORY.md`
- `docs/API_SURFACE_INVENTORY.md`
- `docs/SAFETY_AUDIT.md`
- `docs/NEXT_PHASE_PLAN.md`

## Scripts Inventory

- `scripts/verify_foundation.py`: verifies required files, stack keywords, audit checks, and pytest.
- `scripts/audit_foundation.py`: deterministic local Milestone A/B audit script.

## Tests Inventory

Tests cover settings, domain contracts, database foundations, TimescaleDB schemas, research lake helpers, Redis cache, Redis Streams, Kafka/Redpanda Event Backbone, Data Quality + Validation Framework, Synthetic Fixture foundation, instrument metadata persistence, market data batch metadata persistence, synthetic OHLCV storage, synthetic OHLCV research lake export, Worker System, Instrument Master/Provider contracts, ClickHouse Warehouse, Feature Registry, API health endpoints, documentation status, and Prompt 11 audit invariants.

The repository remains cross-platform-safe: use `pathlib`, avoid hardcoded macOS or Windows paths, build on Mac mini M2 during development, and preserve the Windows-native Stark Terminal target.

Kafka/Redpanda Event Backbone and Data Quality + Validation Framework foundations are implemented as contracts only. Synthetic Fixtures are local-only test/dev data only. Market Data Batch Persistence stores batch metadata only and no full OHLCV bars. Synthetic OHLCV Research Lake Export writes only explicit synthetic/temp artifacts. no execution APIs. no real market ingestion. no external calls. no analytics signals.
