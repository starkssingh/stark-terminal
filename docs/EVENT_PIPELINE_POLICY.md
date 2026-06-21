# Event Pipeline Policy

Redis Streams provide the first lightweight event pipeline foundation for Stark Terminal. The pipeline is for coordination and replayable application workflow boundaries, not durable truth.

## Canonical Stream Name Format

```text
stark:{environment}:{namespace}
```

The `stark` prefix comes from `STREAM_KEY_PREFIX`. The environment segment comes from `STREAM_ENVIRONMENT_NAMESPACE`. Both must be safe slug-like strings.

Examples:

- `stark:development:ingestion`
- `stark:development:features`
- `stark:development:decisions`
- `stark:development:system`

## Stream Namespaces

Prompt 06 defines these stream namespaces:

- `ingestion`
- `normalization`
- `features`
- `regime`
- `options`
- `risk`
- `decisions`
- `backtests`
- `paper_lab`
- `audit`
- `system`

## Event Lifecycle

1. Create an EventEnvelope with event type, source, payload, schema version, stream name, and timestamp.
2. Publish the event through the stream producer.
3. Consume the event through the stream consumer.
4. Acknowledge the event when handled.
5. Persist audit records later through explicit audit contracts.

Prompt 06 does not implement worker loops or real ingestion. Prompt 07 adds worker lifecycle contracts, but actual event-to-worker production wiring is still future work.

## Priority Rules

Event priority can be `LOW`, `NORMAL`, `HIGH`, or `CRITICAL`. Priority is metadata only in Prompt 06. It does not create scheduling, execution, or trading behavior.

## Correlation And Causation

`correlation_id` links related events in a workflow. `causation_id` identifies the event that caused a later event. Both prepare auditability and replay without implementing durable event replay yet.

## Payload Safety

Payloads must be JSON-serializable and must not contain secrets, credentials, raw URLs, provider tokens, API keys, broker tokens, or execution credentials.

No execution events are implemented in Prompt 06. Execution APIs remain forbidden until a future safety milestone explicitly unlocks them.

Kafka/Redpanda deferred to a later prompt for durable institutional event replay.
