# Symbol Normalization Policy

Symbol normalization keeps instrument identity deterministic across Stark Terminal infrastructure.

## Rules

- Strip leading and trailing whitespace.
- Uppercase symbols.
- Reject empty values.
- Reject control characters.
- Reject path traversal-like values.
- Reject path separators.
- Reject URL-like values.
- Allow alphanumeric symbols plus safe dots, hyphens, underscores, and ampersands.

## Exchange Normalization

Exchange values normalize to the `Exchange` enum. Prompt 08 supports:

- `NSE`
- `BSE`

## Segment Normalization

Segment values normalize to `MarketSegment`. Prompt 08 uses existing segment contracts such as:

- `NSE_EQUITY`
- `BSE_EQUITY`
- `INDEX`
- `FUTURES`
- `OPTIONS`

## Instrument Key Format

Canonical key format:

```text
EXCHANGE:SYMBOL:SEGMENT
```

Examples:

- `NSE:RELIANCE:NSE_EQUITY`
- `NSE:NIFTY:INDEX`
- `BSE:SENSEX:INDEX`

## Why Stable Identity Matters

Stable identity is required for PostgreSQL metadata, TimescaleDB operational time-series records, Parquet research lake datasets, Redis cache keys, Redis Streams event payloads, Worker System job payloads, future ClickHouse analytical tables, and future Feature Store records.

## Scope Boundary

Symbol normalization is not market data ingestion. It does not scrape NSE/BSE, call external providers, validate real-time listings, create decisions, or enable execution APIs.
