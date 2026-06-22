# API Surface Inventory

Prompt 25 audits the current API surface after the Provider Adapter Milestone Audit. All listed endpoints are read-only foundation endpoints. Expected answer for every current endpoint: safe, no external calls, no execution, no raw secrets, and no durable state mutation.

| Endpoint | Purpose | External Calls | Exposes Secrets | Mutates Durable State | Safety Posture |
| --- | --- | --- | --- | --- | --- |
| `/health` | API liveness, version, prompt, and audit marker | No | No | No | no execution APIs |
| `/config` | Safe settings snapshot | No | No | No | raw URLs and credentials omitted |
| `/database/health` | Database foundation health | No required live service | No | No | SQLite fallback/local check only |
| `/timeseries/health` | TimescaleDB capability health | No required live service | No | No | disabled-safe |
| `/research-lake/health` | DuckDB/Parquet lake health | No | No | No by default | directory creation opt-in only |
| `/cache/health` | Redis cache health | No required live service | No | No | memory fallback/local-safe |
| `/streams/health` | Redis Streams health | No required live service | No | No | memory fallback/local-safe |
| `/event-backbone/health` | Kafka/Redpanda Event Backbone health | No required live service | No | No | memory fallback/local-safe |
| `/data-quality/health` | Data Quality + Validation Framework health | No | No | No | deterministic local validators only |
| `/fixtures/health` | Synthetic fixture foundation health | No | No | No | synthetic local-only test/dev data |
| `/instrument-metadata/health` | Instrument Metadata Persistence health | No | No | No | metadata-only repository status |
| `/market-data-batches/health` | Market Data Batch Persistence health | No | No | No | metadata-only repository status; no full OHLCV bars |
| `/synthetic-ohlcv-storage/health` | Synthetic OHLCV Storage health | No | No | No | synthetic-only repository status; no real market data |
| `/synthetic-ohlcv-exports/health` | Synthetic OHLCV Research Lake Export health | No | No | No | synthetic-only export contract status |
| `/provider-guardrails/health` | Provider Adapter Guardrail health | No | No | No | guardrail status only; no provider approval |
| `/provider-readiness/health` | Real Provider Readiness health | No | No | No | governance status only; no real implementation |
| `/local-sample-provider/health` | Local Sample Provider Adapter health | No | No | No | synthetic/local/test-only provider health |
| `/local-file-provider/health` | Local File Provider Adapter health | No | No | No | local-file-only test/dev provider health |
| `/workers/health` | Worker System health | No | No | No | does not start workers |
| `/instruments/health` | Instrument Master contract health | No | No | No | synthetic/local only |
| `/providers/health` | Provider contract health | No | No | No | read-only provider contracts |
| `/warehouse/health` | ClickHouse Warehouse health | No required live service | No | No | memory query recorder fallback |
| `/features/health` | Feature Registry health | No | No | No | metadata/governance only |
| `/warehouse/contracts` | Analytical table contract inventory | No | No | No | returns contracts only |
| `/features/contracts` | Feature registry enum/contract inventory | No | No | No | returns contract metadata only |
| `/event-backbone/topics` | Event backbone topic contract inventory | No | No | No | returns topic names only |
| `/data-quality/contracts` | Data quality enum/contract inventory | No | No | No | returns contract metadata only |
| `/instruments/sample` | Synthetic/local instrument examples | No | No | No | test/local sample data only |
| `/fixtures/catalog` | Synthetic fixture manifest catalog | No | No | No | metadata only, no OHLCV payload |
| `/instrument-metadata/sample` | Synthetic/local instrument examples for persistence layer | No | No | No | synthetic metadata only |
| `/instrument-metadata/list` | Persisted instrument metadata list | No | No | No | fail-safe read-only metadata endpoint |
| `/market-data-batches/sample` | Synthetic market data batch metadata sample | No | No | No | synthetic metadata only; no full OHLCV bars returned |
| `/market-data-batches/list` | Persisted market data batch metadata list | No | No | No | fail-safe read-only metadata endpoint |
| `/synthetic-ohlcv-storage/sample` | Synthetic OHLCV storage validation sample | No | No | No | synthetic/test-only sample result; no storage write |
| `/synthetic-ohlcv-storage/contracts` | Synthetic OHLCV storage contract metadata | No | No | No | idempotency/storage contract only |
| `/synthetic-ohlcv-exports/contracts` | Synthetic OHLCV export contract metadata | No | No | No | DatasetManifest/export contract only |
| `/synthetic-ohlcv-exports/sample` | Synthetic OHLCV export request sample | No | No | No | metadata only, no files and no OHLCV bars |
| `/provider-guardrails/contracts` | Provider guardrail contract metadata | No | No | No | no network, no scraping, no credentials, no execution |
| `/provider-guardrails/readiness-template` | Provider approval/compliance template | No | No | No | template only, no real provider approval |
| `/provider-readiness/contracts` | Provider readiness contract metadata | No | No | No | no real implementation, no external calls, no SDKs |
| `/provider-readiness/template` | Generic provider candidate/checklist template | No | No | No | template only, no real provider approval |
| `/provider-readiness/example-score` | Generic local-file candidate score example | No | No | No | example only, no production approval |
| `/local-sample-provider/contracts` | Local sample provider contract metadata | No | No | No | synthetic-only supported/unsupported capabilities |
| `/local-sample-provider/instruments` | Local sample provider synthetic instruments | No | No | No | synthetic local-only instrument response |
| `/local-sample-provider/sample-bars` | Local sample provider tiny synthetic bars | No | No | No | tiny synthetic sample, not live data |
| `/local-file-provider/contracts` | Local file provider contract metadata | No | No | No | local-file-only supported formats/path safety; no arbitrary file reads |

## Audit Notes

- no execution APIs exist in the current API surface.
- no real market ingestion occurs through any endpoint.
- no broker execution, order placement, live trading, or real-money routing endpoint exists.
- `DATABASE_URL`, `TIMESCALE_DATABASE_URL`, `REDIS_URL`, `CLICKHOUSE_URL`, `CLICKHOUSE_USER`, `CLICKHOUSE_PASSWORD`, API keys, tokens, and broker secrets must not appear in responses.
- Kafka/Redpanda Event Backbone endpoints are contract/health surfaces only; no production event pipelines or topic creation exists.
- Data Quality endpoints are contract/health surfaces only; no production validation pipelines, external validation, analytics signals, or ingestion exists.
- Fixture endpoints are synthetic local-only test/dev surfaces only; no real market data, no external calls, no market data ingestion, and no OHLCV datasets are returned by catalog metadata.
- Instrument Metadata Persistence endpoints are metadata-only. They do not seed automatically, persist OHLCV bars, fetch external providers, or expose execution APIs.
- Market Data Batch Persistence endpoints are metadata-only. They do not seed automatically, persist full OHLCV bars, fetch external providers, write TimescaleDB/ClickHouse/DuckDB/Parquet, publish events, or expose execution APIs.
- Synthetic OHLCV Storage endpoints are synthetic-only. They do not ingest real market data, call providers, write external stores, publish events, compute analytics, generate signals, generate decisions, or expose execution APIs.
- Synthetic OHLCV Research Lake Export endpoints are synthetic-only metadata/contract surfaces. They do not write files, return OHLCV bars, ingest real market data, call providers, compute analytics, generate trading signals, generate decisions, or expose execution APIs.
- Provider Guardrail endpoints are governance/contract surfaces. They do not approve real providers, do not make external calls, do not scrape, do not expose credentials, do not ingest real market data, do not return live data, and do not expose execution APIs.
- Provider Readiness endpoints are governance/contract/template surfaces. They do not approve real providers, do not make external calls, do not scrape, do not add SDKs, do not expose credentials, do not ingest real market data, do not return live data, do not grant production approval, and do not expose execution APIs.
- Local Sample Provider endpoints are synthetic/local/test-only provider surfaces. They do not make external calls, do not scrape, do not expose credentials, do not ingest real market data, do not persist responses, do not publish events, do not generate trading signals, do not generate decisions, and do not expose execution APIs.
- Local File Provider endpoints are local-file-only test/dev provider surfaces. They do not read files through HTTP, do not accept caller-supplied paths, enforce a no arbitrary file read API boundary, do not make external calls, do not scrape, do not expose credentials, do not ingest real market data, do not persist responses, do not publish events, do not generate trading signals, do not generate decisions, and do not expose execution APIs.
- Prompt 23 adds `/provider-readiness/health`, `/provider-readiness/contracts`, `/provider-readiness/template`, and `/provider-readiness/example-score`. These endpoints do not return live market data, do not claim real market data, do not expose secrets, do not make external calls, do not scrape, do not use credentials, do not approve production, and do not generate trading decisions or signals.
- Prompt 24 adds `/local-file-provider/health` and `/local-file-provider/contracts`. These endpoints do not return live market data, do not claim real market data, do not expose secrets, do not make external calls, do not scrape, do not use credentials, do not expose arbitrary file read API behavior, and do not generate trading decisions or signals.
- Prompt 25 audits `/provider-guardrails`, `/provider-readiness`, `/local-sample-provider`, and `/local-file-provider` endpoints together. These endpoints do not make external calls, do not expose secrets, do not return live market data, do not approve production providers, do not accept arbitrary file paths for reads, and do not generate decisions or trading signals.
- Development environment: Mac mini M2 / macOS / Apple Silicon.
- Target desktop product: Windows-native Stark Terminal.
