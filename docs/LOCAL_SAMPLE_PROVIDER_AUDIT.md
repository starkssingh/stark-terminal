# Local Sample Provider Audit

Prompt 22 audits Local Sample Provider Adapter v0 from Prompt 21.

## Adapter Status

Local Sample Provider Adapter v0 was the only implemented provider adapter at the Prompt 22 audit point. After Prompt 24, Local File Provider Adapter v0 is also implemented as a local/test/dev-only adapter. Local Sample remains synthetic, local-only, test/dev only, read-only, and guardrail-protected.

It uses:

- synthetic/local instrument fixtures.
- deterministic synthetic OHLCV generation.
- `LOCAL_SAMPLE` provider identity.
- `synthetic-local-test-only` source references.
- Data Quality validation where practical.
- provider guardrail evaluation before use.

## Supported Capabilities

Supported capabilities:

- instrument master.
- historical bars.
- health check.

These capabilities return synthetic/local/test responses only. They are not live data, not real market data, not provider-sourced data, not trading data, not investment advice, not analytics signals, and not decisions.

## Unsupported Capabilities

Unsupported capabilities:

- real latest bar.
- real options chain.
- real futures chain.
- corporate actions.
- broker execution.
- order placement.
- live trading.
- real-money routing.
- credentials or provider account access.

Unsupported behavior must return safe unavailable/error responses. It must not call external providers or pretend to have real data.

## Safety Verdict

Local Sample Provider Adapter v0 passes the milestone boundary if tests pass:

- no external calls.
- no scraping.
- no credentials.
- no provider SDKs.
- no real market data.
- no real market ingestion.
- no persistence writes.
- no event publishing.
- no analytics/signals/decisions.
- no execution APIs.

API responses must keep `synthetic: true` and `real_market_data: false` where applicable and must not claim live market data.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
