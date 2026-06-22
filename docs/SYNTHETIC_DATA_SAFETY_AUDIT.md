# Synthetic Data Safety Audit

Prompt 17 audits the synthetic data posture introduced in Prompt 14 and used by Prompts 15-16.

## Synthetic Fixture Status

Synthetic fixtures remain local-only test/dev data. They are not real market data, not live data, not trading data, not investment advice, and not a provider source.

Default labels and source references use `synthetic-local-test-only`. Fixture manifests must include synthetic/local/test semantics. Fixture API responses mark `synthetic: true` and `real_market_data: false`.

## Deterministic Generation

Synthetic OHLCV generation uses explicit seeds, tiny row counts by default, timezone-aware UTC timestamps, and deterministic price paths. The same seed/config produces the same bars; different seeds can produce different synthetic bars.

## No Live Data

Prompt 14 fixtures do not:

- scrape NSE/BSE.
- call provider APIs.
- use live market data.
- include production data files.
- claim tradability.
- publish events.
- write production datasets.
- compute indicators.
- compute features.
- generate analytics signals.
- generate decisions or recommendations.
- expose execution APIs.

## Disk Write Posture

Synthetic fixture disk writes are disabled by default for the configured output root. Parquet helper writes are explicit and tests use temporary directories. No generated fixture datasets should be committed.

## Validation Posture

Synthetic bars and batches validate through the Data Quality + Validation Framework. Validation failures must not silently pass. Future storage prompts must keep validation-before-persistence enabled.

## API Posture

Fixture endpoints provide health and catalog metadata only. They do not return large OHLCV datasets, do not claim live or real market data, do not expose secrets, do not make external calls, and do not generate decisions.

## Safety Verdict

Prompt 17 confirms synthetic fixtures are suitable for deterministic local tests and development demos. They are not suitable for trading, investment decisions, production analytics, or live data display.
