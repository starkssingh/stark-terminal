# Workers Package

This package contains the Worker System Foundation for Stark Terminal.

Prompt 07 implements worker roles, job envelopes, worker results, base worker abstractions, a worker registry, a deterministic in-process harness, safe sample workers, and worker health checks.

Prompt 07 does not implement real production workers, market data ingestion, analytics engines, broker integrations, execution APIs, schedulers, background daemons, or infinite production loops.

Redis Streams integration is future wiring. The in-process harness is local/test-only and uses no external services.

