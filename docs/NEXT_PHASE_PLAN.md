# Next Phase Plan

## Recommended Next Prompt

Prompt 17 - Data Foundation Audit and Readiness Check.

## Why This Follows

Prompts 00-10 establish typed contracts, safety boundaries, data platform foundations, cache/stream primitives, worker contracts, instrument/provider contracts, analytical warehouse contracts, and Feature Registry governance. Prompt 11 audits and consolidates that foundation. Prompt 12 adds the durable event backbone layer. Prompt 13 adds deterministic Data Quality + Validation Framework contracts. Prompt 14 adds synthetic local-only OHLCV fixtures.

Prompt 15 completed Instrument Metadata Persistence Wiring so canonical instruments can be stored through the PostgreSQL-ready ORM foundation with SQLite test fallback and validation gates. Prompt 16 completed Market Data Batch Persistence Contracts so validated synthetic/local `MarketDataBatch` metadata can be persisted without storing full production OHLCV history. The next institutional step is an audit and readiness check across Prompts 14-16 before planning future TimescaleDB synthetic OHLCV storage.

## Proposed Phase After Audit

The next phase should remain infrastructure-first and safety-bounded:

1. Prompt 17 - Data Foundation Audit and Readiness Check.
2. Prompt 18 - Provider Adapter Contract Hardening.
3. Prompt 19 - Operational Dataset Lineage Foundation.
4. Prompt 20 - Research Dataset Versioning Foundation.
5. Prompt 21 - Market Calendar + Session Contract Foundation.
6. Prompt 22 - Data Readiness Dashboard Contracts.
7. Prompt 23 - Provider Sandbox Adapter Foundation.
8. Prompt 24 - Data Quality Persistence Planning.
9. Prompt 25 - Synthetic Provider Sandbox Replay Contracts.
10. Prompt 26 - TimescaleDB Synthetic OHLCV Storage Planning.

## Still Forbidden

- no execution APIs.
- no broker execution.
- no order placement.
- no real-money routing.
- no broker credential handling.
- no real market ingestion.
- no provider-specific live clients.
- no NSE/BSE scraping.
- no production Kafka/Redpanda pipelines.
- no production validation pipelines.
- no full OHLCV production persistence.
- no analytics engines, ML models, feature computation, backtesting engine, options pricing engine, or paper-to-strategy implementation.

## Platform Notes

Development and tests currently run on Mac mini M2 / macOS / Apple Silicon. The target desktop product remains Windows-native Stark Terminal. Backend target remains Oracle Cloud deployment.
