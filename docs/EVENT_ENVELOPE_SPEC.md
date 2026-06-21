# Event Envelope Specification

EventEnvelope is the typed event contract for the Redis Streams foundation.

## Fields

- `event_id`: Stable event identifier. Helpers default this to a UUID.
- `event_type`: Event type enum such as `INGESTION_REQUESTED`, `FEATURE_COMPUTATION_COMPLETED`, `AUDIT_RECORDED`, or `SYSTEM_HEALTH_RECORDED`.
- `source`: Event source enum such as `API`, `WORKER`, `SCHEDULER`, `SYSTEM`, `TEST`, or `UNKNOWN`.
- `priority`: `LOW`, `NORMAL`, `HIGH`, or `CRITICAL`. Defaults to `NORMAL`.
- `schema_version`: Event schema version. Prompt 06 defaults to `v1`.
- `stream`: Stream name such as `stark:development:system`.
- `payload`: JSON-serializable event payload.
- `correlation_id`: Optional workflow correlation identifier.
- `causation_id`: Optional identifier for the event that caused this event.
- `audit_id`: Optional audit reference.
- `created_at`: UTC event creation timestamp.

## Payload Rules

Payloads must be JSON-serializable. Pydantic models, enums, dates, datetimes, lists, dictionaries, and primitives are supported through serialization helpers.

Forbidden payload keys include secret-like fields such as:

- `password`
- `secret`
- `token`
- `api_key`
- `database_url`
- `redis_url`
- `broker_token`

Payloads must not contain broker credentials, provider credentials, execution credentials, raw URLs with credentials, or production secrets.

## Scope Boundary

EventEnvelope is a coordination contract only in Prompt 06. It does not create workers, market data ingestion, Kafka/Redpanda integration, analytics engines, broker integrations, or execution APIs.
