# Streams Package

This package contains the Redis Streams event pipeline foundation for Stark Terminal.

Prompt 06 implements stream naming policy, typed event envelopes, stream serialization, producer and consumer wrappers, an in-memory local/test fallback, and safe stream health checks.

Redis Streams are for event coordination only. They are not the system of record. PostgreSQL remains the system of record, TimescaleDB remains the operational time-series layer, DuckDB/Parquet remains the research lake, and the Redis cache foundation remains separate from stream semantics.

Prompt 06 does not implement real workers, market-data ingestion, provider clients, Kafka/Redpanda, broker integrations, or execution APIs.

The in-memory stream fallback is for local development and deterministic tests only. It is not durable storage.

