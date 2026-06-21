# Event Backbone Topic Policy

Kafka/Redpanda topic names are deterministic and namespaced. Prompt 12 only renders topic names and lists default contracts. It does not create topics automatically.

## Canonical Topic Name Format

```text
stark.{environment}.{namespace}
```

Examples:

- `stark.development.ingestion`
- `stark.development.features`
- `stark.development.decisions`
- `stark.development.system`
- `stark.development.warehouse`

## Namespace Rules

Prompt 12 defines these default namespaces:

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
- `warehouse`
- `research_lake`

The prefix comes from `KAFKA_TOPIC_PREFIX`. The environment namespace comes from `KAFKA_ENVIRONMENT_NAMESPACE`. Both must be safe slug-like strings.

## Allowed And Disallowed Topic Parts

Allowed topic parts are lower-case slug-like strings using letters, numbers, underscores, and hyphens. Disallowed values include:

- empty or whitespace-only values
- control characters
- path traversal values such as `../`
- slashes and backslashes
- raw URLs
- semicolons, quotes, backticks, and injection-like tokens
- secrets, credentials, or bootstrap server values
- execution/order/broker/live-trading topic concepts

Topic names must not include raw secrets or URLs. Topic creation is not automatic in Prompt 12.

## Redis Streams Relationship

Redis Streams use colon-separated stream names such as `stark:development:system`. Kafka/Redpanda uses dot-separated topic names such as `stark.development.system`. Mapping between Redis Streams and Kafka/Redpanda is explicit through durable event compatibility helpers; there is no implicit bridge or production pipeline in Prompt 12.

## Safety Boundary

no execution APIs. no market data ingestion. no execution/order/broker/live-trading topics.
