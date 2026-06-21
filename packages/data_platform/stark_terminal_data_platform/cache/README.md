# Cache Package

This package contains the Redis cache foundation for Stark Terminal.

Prompt 05 implements cache key policy helpers, JSON serialization, a small Redis client wrapper, an in-memory local/test fallback, and safe cache health checks.

Redis is a low-latency cache only. It is not the system of record. PostgreSQL remains the system of record, TimescaleDB remains the operational time-series layer, and DuckDB/Parquet remains the research lake.

Prompt 05 does not implement Redis Streams, event pipelines, market-data ingestion, broker integrations, or execution APIs.

The in-memory fallback is for local development and deterministic tests only. It is not durable storage.
