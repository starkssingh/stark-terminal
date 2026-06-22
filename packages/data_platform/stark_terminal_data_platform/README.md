# Stark Terminal Data Platform

This package contains the Prompt 02 SQLAlchemy/Alembic database foundation for metadata persistence, the Prompt 03 TimescaleDB-oriented operational schema foundation, the Prompt 04 DuckDB + Parquet research lake foundation, the Prompt 05 Redis cache foundation, the Prompt 06 Redis Streams foundation, the Prompt 07 Worker System foundation, the Prompt 08 Instrument Master/Provider Contracts foundation, the Prompt 09 ClickHouse Warehouse foundation, the Prompt 10 custom Stark Feature Registry foundation, the Prompt 12 Kafka/Redpanda Event Backbone foundation, the Prompt 13 Data Quality + Validation Framework, the Prompt 14 Synthetic Market Data Fixtures, the Prompt 15 Instrument Metadata Persistence Wiring, the Prompt 16 Market Data Batch Persistence Contracts, the Prompt 18 Synthetic OHLCV Storage Foundation, and the Prompt 19 Synthetic OHLCV Research Lake Export Contract. This package will later contain broader provider adapters and external feature store integrations.

Prompt 14 does not implement real market-data ingestion, provider network calls, scraping, real production worker loops, production dashboards, production Kafka/Redpanda pipelines, production validation pipelines, Feast integration, feature computation, analytics signals, broker integrations, automatic ClickHouse table creation, or execution APIs. Synthetic fixtures are local-only test/dev data, not real market data, not trading data, and not investment advice.

## Prompt 15 Instrument Persistence

The data platform now includes `repositories/` and `services/` packages. `InstrumentRepository` and `InstrumentMetadataService` wire instrument metadata to the SQLAlchemy foundation with validation-before-persistence. This is metadata-only; it does not ingest real market data, persist OHLCV bars, call external providers, compute analytics, or expose execution APIs.

## Prompt 16 Market Data Batch Persistence

`MarketDataBatchRepository` and `MarketDataBatchMetadataService` wire validated synthetic/local `MarketDataBatch` metadata to the SQLAlchemy foundation. This is batch metadata only; it stores no full OHLCV bars, performs no TimescaleDB writes, ClickHouse writes, DuckDB/Parquet production writes, event publishing, real market ingestion, external calls, analytics, or execution APIs.

## Prompt 19 Synthetic OHLCV Research Lake Export

`exports/` contains `SyntheticOHLCVResearchLakeExportService` for synthetic-only Parquet exports from stored synthetic bars to the research lake contract layer with DatasetManifest linkage and DuckDB readback. This is temp/test-oriented and does not export real market data, call providers, scrape, compute analytics, generate signals, generate decisions, publish events, or expose execution APIs.
