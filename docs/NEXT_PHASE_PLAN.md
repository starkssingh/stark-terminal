# Next Phase Plan

## Recommended Next Prompt

Prompt 14 - Sample Market Data Fixtures + Synthetic OHLCV Contracts.

## Why This Follows

Prompts 00-10 establish typed contracts, safety boundaries, data platform foundations, cache/stream primitives, worker contracts, instrument/provider contracts, analytical warehouse contracts, and Feature Registry governance. Prompt 11 audits and consolidates that foundation. Prompt 12 adds the durable event backbone layer. Prompt 13 adds deterministic Data Quality + Validation Framework contracts.

Prompt 12 completed the Kafka/Redpanda Event Backbone foundation with configuration contracts, topic naming policy, durable event envelope compatibility, producer/consumer wrapper interfaces with local memory fallback, and safe health checks. Prompt 13 completed deterministic data quality and validation contracts before any real market ingestion. The next institutional gap is deterministic synthetic OHLCV fixture contracts so later ingestion and validator work has local, audited sample data.

## Proposed Phase After Audit

The next phase should remain infrastructure-first and safety-bounded:

1. Prompt 14 - Sample Market Data Fixtures + Synthetic OHLCV Contracts.
2. Prompt 15 - Instrument Metadata Persistence Wiring.
3. Prompt 16 - Milestone C Audit.
4. Prompt 17 - Provider Adapter Contract Hardening.
5. Prompt 18 - Operational Dataset Lineage Foundation.
6. Prompt 19 - Research Dataset Versioning Foundation.
7. Prompt 20 - Market Calendar + Session Contract Foundation.
8. Prompt 21 - Data Readiness Dashboard Contracts.
9. Prompt 22 - Provider Sandbox Adapter Foundation.
10. Prompt 23 - Data Quality Persistence Planning.

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
- no analytics engines, ML models, feature computation, backtesting engine, options pricing engine, or paper-to-strategy implementation.

## Platform Notes

Development and tests currently run on Mac mini M2 / macOS / Apple Silicon. The target desktop product remains Windows-native Stark Terminal. Backend target remains Oracle Cloud deployment.
