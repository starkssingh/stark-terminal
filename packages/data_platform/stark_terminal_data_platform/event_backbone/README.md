# Event Backbone Package

This package contains the Kafka/Redpanda Event Backbone Foundation for Stark Terminal.

Prompt 12 does not implement real production pipelines, real market data ingestion, analytics engines, broker/execution behavior, schema registry integration, ClickHouse ingestion, or Feature Store computation pipelines.

Kafka/Redpanda is the durable institutional event backbone for future replayable, high-throughput, multi-consumer workflows. Redis Streams remains the lightweight event pipeline foundation for local coordination semantics. PostgreSQL remains the system of record.

The in-memory event backbone is local/test-only. It is deterministic and useful for unit tests, but it is not durable storage and must not be treated as production infrastructure.
