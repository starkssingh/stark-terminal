# Durable Event Envelope Specification

DurableEventEnvelope is the typed Kafka/Redpanda event contract for the Prompt 12 Event Backbone foundation.

## Fields

- `event_id`: Stable event identifier. Helpers default this to a UUID.
- `event_type`: Existing EventType enum reused from Redis Streams EventEnvelope.
- `source`: Existing EventSource enum reused from Redis Streams EventEnvelope.
- `priority`: Existing EventPriority enum. Defaults to `NORMAL`.
- `schema_version`: Durable event schema version. Prompt 12 defaults to `v1`.
- `topic`: Kafka/Redpanda topic name.
- `payload`: JSON-serializable event payload.
- `key`: Optional Kafka/Redpanda message key. Must not contain secrets.
- `partition`: Optional non-negative partition.
- `correlation_id`: Optional workflow correlation identifier.
- `causation_id`: Optional identifier for the event that caused this event.
- `audit_id`: Optional audit reference.
- `created_at`: UTC event creation timestamp.

## Redis Streams Compatibility

Prompt 12 reuses EventType, EventSource, and EventPriority from Prompt 06. `from_stream_event()` converts a Redis Streams EventEnvelope into a DurableEventEnvelope only when an explicit Kafka/Redpanda topic is supplied. `to_stream_event()` converts a DurableEventEnvelope into a Redis Streams EventEnvelope only when an explicit Redis stream name is supplied.

Conversions preserve `event_id`, `correlation_id`, `causation_id`, `audit_id`, priority, source, event type, payload, and created timestamp where practical. Kafka topic names and Redis stream names are not implicitly interchangeable.

## Payload Rules

Payloads must be JSON-serializable. Pydantic models, enums, dates, datetimes, lists, dictionaries, and primitives are supported through serialization helpers.

Forbidden payload keys include:

- `password`
- `secret`
- `token`
- `api_key`
- `database_url`
- `redis_url`
- `clickhouse_url`
- `kafka_bootstrap_servers`
- `broker_token`
- `broker_secret`

Payloads must not contain broker credentials, provider credentials, execution credentials, raw URLs with credentials, production secrets, execution/order/broker/live-trading events, or real-money routing instructions.

## Scope Boundary

DurableEventEnvelope is a contract only in Prompt 12. It does not create production pipelines, market data ingestion, schema registry integration, analytics engines, broker integrations, or execution APIs.

Development environment remains Mac mini M2 / macOS / Apple Silicon. Target desktop product remains Windows-native Stark Terminal.
