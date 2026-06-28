# Stark Terminal Test Policy

Status: documentation/test consolidation interlude.

Tests remain required for Stark Terminal. The project is shifting from prompt-number test sprawl toward grouped phase and boundary coverage so the suite stays useful for product development while preserving safety.

Verifier keyword lock: tests remain required.

## Policy

- Tests should be grouped by phase and boundary rather than creating excessive one-off prompt-number files.
- New prompts should avoid creating excessive one-off test files unless a new risk surface genuinely needs separate coverage.
- Safety-critical behavior must remain tested.
- Feature-development prompts should include focused tests for the changed module, contract, or endpoint.
- Test result counts should be tracked at milestone or phase level.
- `skip` and `xfail` must not be used as cleanup substitutes.
- Existing granular tests may remain as historical coverage until a later cleanup proves grouped tests fully preserve the same checks.
- Archived tests are historical references, not active suite members.
- Grouped boundary tests are authoritative for consolidated safety boundaries unless a feature-specific test is needed.
- Future prompts should not recreate granular audit sprawl after an archive pass.

## Boundary Coverage That Must Not Weaken

The grouped tests must continue to protect these constraints:

- no execution APIs
- no broker controls
- no readiness-to-trade
- no hidden trade interpretation
- no recommendation, action, confidence, or active DecisionObject generation
- no active UI, frontend, or desktop implementation where only backend contracts exist
- no active ingestion or persistent storage
- no file upload, download, or preview behavior
- no indexing, search, ranking, retrieval, embedding, or vector-store implementation where only planning/contracts exist
- no paper parsing, PDF parsing, arXiv ingestion, or LLM paper analysis
- no strategy generation or backtesting

## Future Default

For normal prompts, prefer one core doc, one explicit safety section, and one focused test file per meaningful feature/module. Add broader grouped boundary tests only when the feature creates a new boundary surface.

## Phase-Based Default For Future Prompts

Future prompts must prefer phase-level tests. Do not add one test file per forbidden capability. Use grouped boundary tests for repeated safety rules.
Add feature tests only when actual product behavior changes. Avoid audit-only prompts unless closing a real phase.

Prompt 93 reinforces this as the forward default: future prompts should use
phase-based docs/tests only, avoid prompt-by-prompt audit/test/doc sprawl,
avoid the one-test-file-per-forbidden-capability pattern, and add feature
behavior tests only when actual product behavior changes. Audit-only prompts should be rare and reserved for real phase closure, material safety gates, or compliance-critical transitions.

Prompt 94 reinforces the product-development default: tests should remain
phase-level, behavior tests are preferred when real product behavior is added,
audit-only tests should not dominate future prompts, and repeated safety
checks should live in grouped boundary tests rather than one file per
forbidden capability.

## Archived Tests

Archived prompt-level audit tests live under `tests/archive/prompt_audits/`
with the `.py.archived` suffix. They preserve traceability but are not collected
by pytest. Their active replacements are grouped tests under `tests/phases/`
and `tests/boundaries/`.

Archive Pass 2 extends this policy to older Strategy Research Workspace and
Research Artifact Registry `NO_*` micro-audit tests. Grouped phase and boundary
tests are now authoritative for those consolidated safety boundaries, while
archived tests remain historical references only.

Archive Pass 2 archived older phase micro-audit docs and tests only after
grouped coverage was present.

## Grouped Reports Are Authoritative

After the aggressive deletion pass, grouped phase/boundary tests and grouped
report files under `docs/reports/` are authoritative for deleted micro-audit
details. Old micro-audit sprawl should not be recreated. Feature and product
tests remain direct, focused tests and should not be over-consolidated when
they validate settings, schemas, API behavior, contracts, calculations,
storage, workers, providers, analytics, serialization, health endpoints, or
package invariants.
