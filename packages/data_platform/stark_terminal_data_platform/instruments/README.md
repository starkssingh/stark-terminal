# Instrument Master Package

This package contains Instrument Master contracts for Stark Terminal.

Prompt 08 uses only synthetic/local fixtures. It does not perform external calls, scrape exchanges, ingest real market data, persist instrument universes, call provider APIs, or expose trading/execution APIs.

Future prompts may connect these contracts to PostgreSQL instrument metadata and explicit provider adapters after data policy review.
