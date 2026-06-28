# Product Surface Reorientation

Status: Prompt 94 complete after verification.

Prompt 95 completed the next step after this reorientation by starting Retail
Decision Console productization as productization plan and UI shell boundary
only.

## Purpose

Prompt 94 reorients Stark Terminal from extended research-contract and audit
phases back toward concrete product surface development. It is a planning and
roadmap prompt only. It adds no product runtime capability, no API route, no
package, no UI component, no database object, and no execution path.

## Reason For Reorientation

The recent Research Artifact Index, Research Metadata Graph, and Research
Knowledge Map phases created useful planning, API contract, display contract,
and safety boundaries. Those phases are now closed and remain non-active. The
project should stop extending research abstractions and move toward the
flagship user-facing surface while preserving the same safety posture.

Future work should prioritize product surfaces over audit-only research
abstractions. Audit-only prompts should be rare and reserved for real phase
closures, material safety gates, or compliance-critical transitions.

Verifier lock: Future work should prioritize product surfaces over audit-only research abstractions.

## Current Product State

Stark Terminal has broad foundation coverage:

- Backend health, configuration, safe settings snapshots, and FastAPI route
  shells.
- PostgreSQL, SQLAlchemy, Alembic, TimescaleDB-oriented time-series schema,
  DuckDB, Parquet research lake, Redis cache, Redis Streams, Kafka/Redpanda
  event backbone, worker harness, provider guardrails, warehouse, feature
  registry, data-quality, synthetic fixtures, analytics, regime, and decision
  skeleton foundations.
- Local sample and local file provider contracts for synthetic/local
  development data only.
- Decision Desk planning, DecisionObject evidence bundle contracts, decision
  safety, readiness/display/API skeletons, evidence validation, human-review
  workflow placeholders, system boundary hardening, and API/display
  integration readiness.
- Retail Dashboard planning/API/display/safety/milestone/boundary/integration
  readiness phases.
- Retail Trader Experience planning/API/display/safety/milestone/boundary/
  integration readiness phases.
- Strategy Research Workspace planning/API/display/safety/milestone/boundary/
  integration readiness phases.
- Research Artifact Registry, Research Artifact Index, Research Metadata
  Graph, and Research Knowledge Map phases, all closed or completed as
  planning/API/display/safety layers only.

## Current Safety Posture

Execution APIs remain forbidden. Broker controls, order placement, real-money
routing, approvals/overrides, readiness-to-trade, active recommendations,
action generation, confidence scoring, and active DecisionObject generation
remain forbidden.

Decision candidate is not a trade. No direct signal-to-trade path is allowed.
No user-facing surface may treat synthetic or local data as trusted live
market intelligence.

## Product Gaps

The repo still does not contain:

- active trading
- broker execution
- active recommendations
- final DecisionObject generation
- live provider ingestion
- production deployment
- a production Retail Decision Console
- active UI implementation beyond skeletons, placeholders, and shell/contract
  boundaries
- validated data-quality-to-decision product behavior

## Recommended Next Product Surface

The next surface should be Retail Decision Console / Decision Desk
productization.

Verifier lock: Retail Decision Console / Decision Desk productization.

This is the flagship product surface because it can compress deeper quant,
regime, evidence, options, risk, and research layers into a user-facing
decision-support console while keeping execution disabled. It should expose
structure, context, and review posture before it exposes recommendation-like
output.

## Prompt 95 Recommendation

Prompt 95 - Retail Decision Console Productization Plan and UI Shell Boundary.

Prompt 95 should:

- define the actual Retail Decision Console product surface
- create a Windows-native desktop UI shell plan or backend UI contract based
  on the current repo state
- keep execution disabled
- keep outputs unavailable, demo-only, or skeleton-only until data quality and
  decision validation exist
- use phase-level docs/tests only
- avoid audit sprawl
- focus on product surface construction instead of more research indexing

## What Remains Forbidden

Prompt 94 does not implement product capability and does not permit later
work to bypass safety. The following remain forbidden:

- execution APIs
- broker controls
- live trading
- fake recommendations
- fake confidence scores
- active DecisionObject generation
- treating synthetic/local data as trusted live market intelligence
- strategy generation or backtesting
- graph/search/retrieval/vector-store implementation through the closed
  research phases
- active UI behavior that implies validated decision support before validation
  exists

## Phase-Based Docs/Tests Policy

Future prompts must remain phase-based:

- one canonical phase doc where possible
- grouped phase tests
- grouped boundary/API tests only when needed
- concise prompt-log entries
- concise safety/audit updates
- no prompt-by-prompt audit/test/doc sprawl
- no one-test-file-per-forbidden-capability pattern

Feature behavior tests are preferred when actual product behavior changes.
