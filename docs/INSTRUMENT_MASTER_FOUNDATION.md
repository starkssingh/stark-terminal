# Instrument Master Foundation

The Instrument Master defines stable instrument identity for Stark Terminal. It is the contract layer that future PostgreSQL records, TimescaleDB bars, Parquet datasets, Redis keys, Redis Streams events, ClickHouse tables, and Feature Store records will reference.

## Prompt 08 Scope

Prompt 08 implements:

- Symbol normalization rules.
- Exchange and segment normalization helpers.
- Stable instrument key format.
- Instrument universe snapshot contracts.
- LocalInstrumentMaster for deterministic local/test use.
- Synthetic/local sample instruments.
- Instrument Master health checks.

Prompt 08 does not implement real market data ingestion, real NSE/BSE instrument loading, scraping, external provider calls, provider SDKs, broker integrations, or execution APIs.

## Stable Identity

Instrument identity uses:

```text
EXCHANGE:SYMBOL:SEGMENT
```

Examples:

- `NSE:RELIANCE:NSE_EQUITY`
- `NSE:NIFTY:INDEX`
- `BSE:SENSEX:INDEX`

Stable identity prevents drift between operational storage, research datasets, cache keys, events, workers, analytics, and audit records.

## Synthetic Fixtures

Prompt 08 includes tiny synthetic/local fixtures for tests only. They do not imply live correctness, production universe membership, current listing status, or real-time market data.

## Future Path

Future prompts may connect these contracts to PostgreSQL instrument metadata and read-only provider adapters. No ingestion occurs without explicit provider implementation, data quality checks, source references, provider terms review, and audit policy.

## Safety

Instrument Master contracts do not create trade calls. They do not route orders, store broker credentials, execute trades, or bypass the Stark Terminal safety exclusions.

## Next Step

Prompt 09 should implement the ClickHouse Analytical Warehouse Foundation unless the roadmap changes through documented architecture review.
