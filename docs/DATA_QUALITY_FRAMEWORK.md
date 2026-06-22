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

## Prompt 14 Synthetic Fixture Relationship

Prompt 14 synthetic OHLCV fixtures validate through this Data Quality Framework, especially `MarketDataBarValidator`. Generated fixture bars are synthetic, local-only, test/dev only, and carry `synthetic-local-test-only` source references. Fixture validation remains deterministic, local, and side-effect free. It makes no external calls, performs no market data ingestion, computes no analytics signals, and enables no execution APIs.

Development environment remains Mac mini M2 / macOS / Apple Silicon. Target desktop product remains Windows-native Stark Terminal.

## Prompt 16 Batch Metadata Gate

Market Data Batch Persistence uses Data Quality validators before writing metadata. Generated synthetic fixture batches must pass local deterministic validation before `MarketDataBatchMetadataService` persists their batch metadata.

Validation failure blocks persistence. This gate does not compute analytics signals, does not run real ingestion, does not make external calls, and does not enable execution APIs.

## Prompt 18 Synthetic OHLCV Storage Gate

Synthetic OHLCV storage uses `MarketDataBarValidator` before storage. `SyntheticOHLCVStorageService` blocks invalid OHLC relationships, negative volume/open interest, missing or non-synthetic source references, and non-`LOCAL_SAMPLE` provider identity before writing through `OHLCVBarRepository`.

This validation-before-storage gate remains deterministic and local. It does not run real ingestion, call providers, publish events, compute analytics signals, generate decisions, or enable execution APIs.

## Prompt 19 Synthetic OHLCV Export Gate

Synthetic OHLCV research lake export uses `MarketDataBarValidator` before Parquet export. `SyntheticOHLCVResearchLakeExportService` blocks empty exports, invalid OHLC relationships, non-synthetic source references, rows over the configured limit, and non-`LOCAL_SAMPLE` provider identity before writing a temporary Parquet artifact.

This validation-before-export gate remains deterministic and local. It does not run real ingestion, call providers, publish events, compute analytics signals, generate decisions, or enable execution APIs.

## Prompt 21 Local Sample Provider Validation

Local Sample Provider Adapter v0 validates synthetic provider responses where practical before returning them. Historical bars are generated through the synthetic OHLCV fixture contracts, carry `LOCAL_SAMPLE` provider identity and `synthetic-local-test-only` source references, and are checked through the Data Quality Framework.

This validation remains deterministic and local. It does not call external providers, scrape, ingest real market data, persist responses, publish events, compute analytics signals, generate decisions, or enable execution APIs.

## Prompt 24 Local File Provider Validation

Local File Provider Adapter v0 validates local/test/dev provider responses where practical before returning them. Historical bars read from explicit CSV/Parquet `LocalFileSource` objects carry `MANUAL` provider identity and `local-file-test-dev-only` source references, and are checked through the Data Quality Framework.

Invalid file rows, missing required columns, unsafe paths, unsupported formats, and invalid OHLC relationships return sanitized errors instead of successful provider responses. This validation remains deterministic and local. It does not call external providers, scrape, ingest real market data, persist responses, publish events, compute analytics signals, generate decisions, or enable execution APIs.
