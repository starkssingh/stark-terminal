# Job Envelope Specification

JobEnvelope is the typed job contract for the Worker System foundation.

## Fields

- `job_id`: Stable job identifier. Helpers default this to a UUID.
- `worker_role`: WorkerRole enum.
- `job_type`: Human-readable job type string.
- `payload`: JSON-serializable job payload.
- `priority`: `LOW`, `NORMAL`, `HIGH`, or `CRITICAL`. Defaults to `NORMAL`.
- `queue`: Queue name for future routing.
- `schema_version`: Worker job schema version. Prompt 07 defaults to `v1`.
- `correlation_id`: Optional workflow correlation identifier.
- `causation_id`: Optional identifier for the triggering job or event.
- `audit_id`: Optional audit reference.
- `created_at`: UTC job creation timestamp.

## Payload Rules

Payloads must be JSON-serializable. Pydantic models, enums, dates, datetimes, lists, dictionaries, and primitives are supported through existing serialization helpers.

Forbidden payload keys include:

- `password`
- `secret`
- `token`
- `api_key`
- `database_url`
- `redis_url`
- `broker_token`
- `broker_secret`

Payloads must not contain broker credentials, provider credentials, execution credentials, raw URLs with credentials, or production secrets.

## Forbidden Jobs

Job types and worker roles that imply execution, broker interaction, order placement, live trading, real-money routing, or credential handling are forbidden. Prompt 07 has no execution APIs and no broker behavior.
