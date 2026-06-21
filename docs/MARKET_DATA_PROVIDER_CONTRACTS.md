# Market Data Provider Contracts

Market Data Provider contracts define the read-only adapter boundary for future market data sources. Prompt 08 creates interfaces and local synthetic behavior only.

## Read-Only Provider Rule

Provider adapters are read-only. They must not place orders, route money, manage broker credentials, trigger execution, or create autonomous trading behavior. Broker execution remains forbidden.

## Prompt 08 Scope

Prompt 08 implements:

- `MarketDataRequest`
- `MarketDataResponse`
- `ProviderCapabilityReport`
- `MarketDataProvider` base contract
- `LocalSampleMarketDataProvider`
- `ProviderRegistry`
- Provider contract health checks

Prompt 08 does not implement provider SDKs, NSE/BSE clients, scraping, external API calls, real data loading, production ingestion, analytics engines, or execution APIs. It is explicitly no scraping and no external calls.

## Network Calls

Network calls are disabled by default:

- `ALLOW_EXTERNAL_MARKET_DATA_CALLS=false`
- `ALLOW_PROVIDER_NETWORK_CALLS=false`

Prompt 08 settings fail closed if these flags are enabled. Future provider implementations require explicit prompt scope and data policy review.

## Capabilities

Provider capabilities are declared explicitly:

- Instrument master
- Historical bars
- Latest bar
- Options chain
- Futures chain
- Corporate actions
- Health check

The local sample provider supports only instrument master and health check using synthetic fixtures.

## Request / Response Schema

Market data requests must declare request kind, schema version, instrument, timeframe, start/end where required, provider identity, and adjustment mode. Historical bar requests require instrument, timeframe, start, and end.

Responses must include bars, instruments, or sanitized errors. Responses also carry provider metadata, quality status, source data reference where available, and received timestamp.

## Credentials And Terms

No credentials, tokens, API keys, raw URLs with secrets, broker tokens, or provider secrets may be committed or exposed. Provider terms must be respected before any future implementation.
