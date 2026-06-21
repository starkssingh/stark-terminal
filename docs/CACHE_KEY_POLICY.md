# Cache Key Policy

Stark Terminal cache keys are deterministic, namespaced, and environment-aware.

## Canonical Format

```text
stark:{environment}:{namespace}:{part1}:{part2}
```

The `stark` prefix comes from `CACHE_KEY_PREFIX`. The environment segment comes from `CACHE_ENVIRONMENT_NAMESPACE`. Both must be safe slug-like strings.

## Namespaces

Prompt 05 defines these cache namespaces:

- `health`
- `config`
- `market_state`
- `decision_object`
- `research_lake`
- `timeseries`
- `database`
- `temporary`

## Allowed Key Parts

Key parts must be non-empty strings. They may represent safe identifiers such as exchange, symbol, timeframe, service name, or local status scope.

Disallowed key parts:

- Empty or whitespace-only values.
- Control characters.
- Path traversal values such as `../` or `..\`.
- URL-like values containing `://`.
- Raw secrets, credentials, tokens, or full infrastructure URLs.

## TTL Rules

Prompt 05 uses `CACHE_DEFAULT_TTL_SECONDS=300` when the caller does not provide a TTL. Callers should use explicit TTLs for short-lived values where practical. Redis is cache, not durable truth.

## Examples

- `stark:development:health:api`
- `stark:development:database:health`
- `stark:development:timeseries:health`
- `stark:development:research_lake:health`
- `stark:development:decision_object:NSE:RELIANCE:DAILY`

Redis Streams keys and stream naming rules are deferred to Prompt 06.
