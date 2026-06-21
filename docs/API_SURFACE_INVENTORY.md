# API Surface Inventory

Prompt 11 audits the current API surface. All listed endpoints are read-only foundation endpoints. Expected answer for every current endpoint: safe, no external calls, no execution, no raw secrets, and no durable state mutation.

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

## Audit Notes

- no execution APIs exist in the current API surface.
- no real market ingestion occurs through any endpoint.
- no broker execution, order placement, live trading, or real-money routing endpoint exists.
- `DATABASE_URL`, `TIMESCALE_DATABASE_URL`, `REDIS_URL`, `CLICKHOUSE_URL`, `CLICKHOUSE_USER`, `CLICKHOUSE_PASSWORD`, API keys, tokens, and broker secrets must not appear in responses.
- Kafka/Redpanda Event Backbone endpoints are contract/health surfaces only; no production event pipelines or topic creation exists.
- Data Quality endpoints are contract/health surfaces only; no production validation pipelines, external validation, analytics signals, or ingestion exists.
- Development environment: Mac mini M2 / macOS / Apple Silicon.
- Target desktop product: Windows-native Stark Terminal.
