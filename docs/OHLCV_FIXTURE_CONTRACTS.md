# OHLCV Fixture Contracts

Prompt 14 defines local-only synthetic OHLCV fixture contracts.

## SyntheticOHLCVConfig

`SyntheticOHLCVConfig` fields:

- `instrument_id`
- `timeframe`
- `start_timestamp`
- `bar_count`
- `start_price`
- `seed`
- `provider`
- `quality_status`
- `source_data_reference`

`start_timestamp` is normalized to timezone-aware UTC. `bar_count` and `start_price` must be positive. `source_data_reference` must clearly include synthetic, local, and test semantics.

## MarketDataBar Generation

Synthetic bars use existing `MarketDataBar` contracts. Generated bars preserve stable `InstrumentId`, declared timeframe, UTC timestamps, `LOCAL_SAMPLE` provider metadata, quality status, and synthetic source data references.

OHLC constraints:

- high is greater than or equal to open, close, and low.
- low is less than or equal to open, close, and high.
- prices are positive.
- volume and open interest are non-negative.

## MarketDataBatch Generation

`generate_synthetic_market_data_batch` wraps deterministic bars in the existing `MarketDataBatch` contract.

Supported timeframes in Prompt 14:

- `DAILY`
- `FIFTEEN_MINUTE`
- `FIVE_MINUTE`

Unsupported timeframes fail closed.

## Validation

Generated fixtures validate through the Prompt 13 Data Quality Framework, especially `MarketDataBarValidator`. Fixture validation is local and deterministic. It makes no external calls, performs no market data ingestion, computes no analytics signals, and enables no execution APIs.

Development environment remains Mac mini M2 / macOS / Apple Silicon. Target desktop product remains Windows-native Stark Terminal.
