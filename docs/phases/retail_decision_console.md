# Retail Decision Console

Status: Prompt 107 Internal Preview Milestone Closure complete after verification.

## Purpose

The Retail Decision Console is the flagship Stark Terminal product surface. It
will eventually compress quant analytics, regime context, options context,
risk, invalidation, evidence, research context, and journaling into a retail
decision-support console.

Prompt 95 defines the product surface and UI shell boundary only. It does not
create an active trading decision surface and does not generate real decisions.

## Productization-Plan-Only Posture

Prompt 95 implements Retail Decision Console Productization Plan and UI Shell Boundary.

The current phase is productization plan and UI shell boundary only:

- planning-only productization contracts
- read-only UI shell boundary contracts
- section, card, and navigation placeholders
- unavailable/demo-state contracts
- readiness metadata for the next UI shell skeleton phase
- GET-only product metadata endpoints

Verifier lock: Retail Decision Console Status: productization plan and UI shell boundary only.

## Prompt 96 UI Shell Skeleton

Prompt 96 implements Retail Decision Console UI Shell Skeleton.
Historical transition reference: Prompt 96 - Retail Decision Console UI Shell Skeleton.
Implementation stage marker: `ui_shell_skeleton`.

The UI shell skeleton is static/skeleton only. It creates testable shell
descriptors, section descriptors, unavailable placeholder states, boundary
assert helpers, and an import-safe desktop module. The desktop shell scope is
limited to labels, placeholders, and a visible safety banner:

`Skeleton only - no live data, no recommendations, no execution`

The shell title is `Stark Terminal - Retail Decision Console` in ASCII docs
and `Stark Terminal — Retail Decision Console` in the UI descriptor.

Verifier lock: Retail Decision Console Status: UI shell skeleton only; no live data, recommendations, confidence scoring, active DecisionObjects, broker controls, or execution.

## Prompt 97 Demo Data Contract and Static State Model

Prompt 97 implements Retail Decision Console Demo Data Contract and Static
State Model.

Implementation stage marker: `demo_static_state`.

The static state scope is deterministic, local, demo-only, unavailable, and
read-only. It creates static state contracts, deterministic demo state
factories, provenance/demo/unavailable labels, section state placeholders,
card state placeholders, and fail-closed state safety helpers. It may connect
to the existing shell descriptor later, but Prompt 97 does not wire visible
state into the desktop shell.

Verifier lock: Retail Decision Console Status: UI shell skeleton plus demo/static state only; no live data, recommendations, confidence scoring, active DecisionObjects, broker controls, order buttons, or execution.

## Prompt 98 Static State Wiring into Desktop Shell

Prompt 98 implements Retail Decision Console Static State Wiring into Desktop
Shell.

Implementation stage marker: `static_state_wired_shell`.

The desktop shell wiring scope is limited to mapping the Prompt 97
demo/static state into a testable shell view-model and desktop fallback/window
rendering path. The wiring is local, deterministic, unavailable, and
demo-only. It does not fetch data, call APIs, start background jobs, run
timers, compute indicators, detect regimes, generate recommendations, score
confidence, generate active DecisionObjects, expose broker controls, create
order buttons, or expose execution APIs.

Verifier lock: Retail Decision Console Status: UI shell skeleton with demo/static state wired; no live data, recommendations, confidence scoring, active DecisionObjects, broker controls, order buttons, or execution.

## Prompt 99 Local Preview Runbook and Manual Smoke Test

Prompt 99 implements Retail Decision Console Local Preview Runbook and Manual
Smoke Test.

Implementation stage marker: `local_preview_runbook`.

The local preview scope is documentation and QA-readiness only. It creates a
safe local preview runbook, a manual smoke test checklist, and a helper script
for launching or describing the existing static/demo shell. The helper does
not require the API server, credentials, live providers, broker setup, live
market data, background workers, order controls, or execution paths.

Verifier lock: Retail Decision Console Status: static/demo shell previewable locally; no live data, recommendations, confidence scoring, active DecisionObjects, broker controls, order buttons, or execution.

## Prompt 100 Visual Polish and Section Layout Pass

Prompt 100 implements Retail Decision Console Visual Polish and Section
Layout Pass.

Implementation stage marker: `visual_layout_pass`.

The visual layout scope is product-surface polish only. It adds a static
layout descriptor, layout zones, section/card ordering metadata, improved
desktop grouping, and an expanded `--no-gui` preview summary. It does not add
live data, data fetching, generated recommendations, action generation,
confidence scoring, active DecisionObject generation, broker controls, order
buttons, execution APIs, or hidden trading logic.

Verifier lock: Retail Decision Console Status: static/demo shell with polished layout; no live data, recommendations, confidence scoring, active DecisionObjects, broker controls, order buttons, or execution.

## Prompt 101 Static Interaction Placeholders

Prompt 101 implements Retail Decision Console Static Interaction
Placeholders.
Historical transition reference: Prompt 101 - Retail Decision Console Static Interaction Placeholders.

Implementation stage marker: `static_interaction_placeholders`.

The static interaction scope is local product-surface UX only. It adds a
static interaction descriptor model, allowed interaction types, forbidden
interaction type rejection, view-model exposure, desktop placeholder display,
and expanded `--no-gui` preview output. It does not add live data, data
fetching, generated recommendations, action generation, confidence scoring,
active DecisionObject generation, broker controls, order buttons, execution
APIs, or hidden trading logic.

Verifier lock: Retail Decision Console Status: static/demo shell with polished layout and local-only placeholder interactions; no live data, recommendations, confidence scoring, active DecisionObjects, broker controls, order buttons, or execution.

## Static Interaction Scope

Prompt 101 adds:

- `packages/core/stark_terminal_core/retail_decision_console/interactions.py`
- static interaction descriptors on the shell view-model
- a static interaction placeholder panel in the desktop shell
- static interaction reporting in `scripts/preview_retail_decision_console.py --no-gui`

Static interactions remain demo-only, unavailable, local-only, read-only, and
non-executive. They are not data fetches, not decision refreshes, not
recommendation triggers, not confidence recalculations, not DecisionObject
generation, not broker controls, not order controls, and not execution.

## Allowed Static Interactions

The allowed static interactions are:

- section toggle placeholders
- static/demo tab selection placeholders
- unavailable reason display placeholders
- provenance label display placeholders
- safety information display placeholders
- local placeholder refresh that performs no fetch
- static instrument placeholder selection
- static timeframe placeholder selection

Each interaction carries an interaction id, label, interaction type, target
section id, demo/unavailable/local/read-only flags, safety note, and false
dangerous flags.

## Forbidden Interaction Types

The forbidden interaction types are explicitly rejected:

- live data refresh
- recommendation refresh
- action generation
- confidence recalculation
- DecisionObject generation
- broker connect
- order preview
- order place
- execution
- approval
- override
- auto trade

These terms may appear only as forbidden/disallowed concepts in documentation
or validation rules. They must never appear as active card titles, buttons,
badges, tabs, outputs, or controls.

## Static Interaction View-Model Exposure

The shell view-model now exposes:

- layout zones
- sections
- cards
- static interactions
- safety banner
- demo/unavailable state
- provenance/demo labels

The view-model preserves `demo_only: true`, `unavailable: true`,
`read_only: true`, local-only interaction flags, and false dangerous flags.

## Static Interaction Preview Behavior

The local `--no-gui` preview now prints:

- `Static interactions:`
- each static interaction type
- each static interaction label
- each target section id
- `demo-only unavailable local-only`

GUI rendering, when PySide6 is available, may display static labels for the
interaction placeholders. These labels are not executable controls and do not
fetch data or create decisions.

## Prompt 102 Preview Snapshot Export

Prompt 102 implements Retail Decision Console Preview Snapshot Export.
Historical transition reference: Prompt 102 - Retail Decision Console Preview Snapshot Export.

Implementation stage marker: `preview_snapshot_export`.

The snapshot/export scope is local QA and documentation only. It adds a safe
snapshot descriptor, JSON/Markdown/Text serialization helpers, local file
writing, `--print-snapshot`, and `--export-snapshot` support in the preview
script. The snapshot is generated from the static/demo shell view-model and
does not fetch data, call APIs, start background jobs, run timers, compute
indicators, detect regimes, generate recommendations, score confidence,
generate active DecisionObjects, expose broker controls, create order
buttons, or expose execution APIs.

Verifier lock: Retail Decision Console Status: static/demo shell with layout, local placeholder interactions, and safe local snapshot export; no live data, recommendations, confidence scoring, active DecisionObjects, broker controls, order buttons, or execution.

## Snapshot Export Scope

Prompt 102 adds:

- `packages/core/stark_terminal_core/retail_decision_console/snapshot_export.py`
- local snapshot printing with `scripts/preview_retail_decision_console.py --print-snapshot`
- local snapshot writing with `scripts/preview_retail_decision_console.py --export-snapshot`
- JSON, Markdown, and text snapshot formats
- grouped phase, boundary, and preview-script tests

The export is local-only, static/demo-only, unavailable-labeled, read-only,
and non-executive. It is not a screenshot pipeline, not a packaging step, not
a production report, not data ingestion, not market intelligence, and not a
decision output.

## Allowed Snapshot Formats

Prompt 102 supports these local snapshot formats:

- `json`
- `markdown`
- `text`

The snapshot includes a safety banner, layout summary, section summary, card
summary, static interaction summary, provenance/demo labels, false dangerous
flags, no secrets marker, no credentials marker, no live data marker, no
recommendation marker, and no execution marker.

## Preview Script Snapshot Flags

The preview helper supports:

- `.venv/bin/python scripts/preview_retail_decision_console.py --print-snapshot`
- `.venv/bin/python scripts/preview_retail_decision_console.py --export-snapshot tmp/preview_snapshots/retail_decision_console_snapshot.json --snapshot-format json`
- `.venv/bin/python scripts/preview_retail_decision_console.py --snapshot-format markdown --print-snapshot`
- `.venv/bin/python scripts/preview_retail_decision_console.py --snapshot-format text --print-snapshot`

The `--no-gui` path still prints the safe static preview summary and does not
start a GUI. The snapshot paths do not require an API server, credentials,
live providers, broker setup, live market data, background workers, order
controls, or execution paths.

## Snapshot Safety Posture

Every preview snapshot must preserve:

- `demo_only: true`
- `unavailable: true`
- `local_only: true`
- `read_only: true`
- no secrets
- no credentials
- no live data
- no generated recommendations
- no action generation
- no confidence scoring
- no active DecisionObject generation
- no broker controls
- no order buttons
- no execution APIs

Snapshot export must not make the static/demo shell appear live, validated,
actionable, or executable.

## Prompt 103 Local QA Bundle

Prompt 103 implements Retail Decision Console Local QA Bundle.
Historical transition reference: Prompt 103 - Retail Decision Console Local QA Bundle.

Implementation stage marker: `local_qa_bundle`.

The local QA bundle scope is QA/product-surface artifact generation only. It
adds a safe local QA bundle model, a local bundle build script, a bundle
runbook, grouped tests, and status/audit updates. The bundle collects review
artifacts from the current static/demo shell without adding live data,
recommendations, action generation, confidence scoring, active DecisionObject
generation, broker controls, order buttons, execution APIs, packaging, or an
installer.

Verifier lock: Retail Decision Console Status: static/demo shell with layout, local placeholder interactions, snapshot export, and local QA bundle; no live data, recommendations, confidence scoring, active DecisionObjects, broker controls, order buttons, or execution.

## Local QA Bundle Artifacts

Prompt 103 adds:

- `packages/core/stark_terminal_core/retail_decision_console/qa_bundle.py`
- `scripts/build_retail_decision_console_qa_bundle.py`
- `docs/runbooks/retail_decision_console_local_qa_bundle.md`
- grouped phase, boundary, and script tests

The QA bundle writes these local artifacts under the selected output
directory:

- `manifest.json`
- `preview_snapshot.json`
- `preview_snapshot.md`
- `no_gui_preview.txt`
- `safety_summary.txt`
- local preview runbook copy
- manual smoke test runbook copy

Every artifact remains local, demo-only, unavailable, read-only, and
non-executive.

## Local QA Purpose

The QA bundle helps reviewers confirm:

- the preview command works
- the no-GUI preview summary exists
- snapshot export works
- runbooks are present
- safety boundaries remain visible
- no live data, recommendation, confidence scoring, DecisionObject, broker,
  order, or execution behavior exists

The QA bundle is not production packaging, not a Windows installer, not
deployment, not live market data, not data ingestion, not a decision engine,
not a recommendation engine, not a confidence report, not an active
DecisionObject, not broker integration, not order infrastructure, and not an
execution surface.

## Local QA Safety Posture

The local QA bundle must preserve:

- `demo_only: true`
- `unavailable: true`
- `local_only: true`
- `read_only: true`
- no secrets
- no credentials
- no live data
- no generated recommendations
- no action generation
- no confidence scoring
- no active DecisionObject generation
- no broker controls
- no order buttons
- no execution APIs

Generated QA artifacts must not be treated as live market intelligence,
validated research, recommendations, confidence output, DecisionObjects,
broker/order controls, or execution artifacts.

## Prompt 104 Manual Acceptance Checklist

Prompt 104 implements Retail Decision Console Manual Acceptance Checklist.
Historical transition reference: Prompt 104 - Retail Decision Console Manual Acceptance Checklist.

Implementation stage marker: `manual_acceptance_checklist`.

The manual acceptance scope is local demo preview only. It adds a human
acceptance checklist for the current static/demo product surface before local
internal sharing or review. It is not production acceptance, not
trading-readiness acceptance, not recommendation-readiness acceptance, and not
execution-readiness acceptance.

Verifier phrases: not production acceptance; not trading-readiness acceptance;
not recommendation-readiness acceptance; not execution-readiness acceptance.

Checklist path:

- `docs/runbooks/retail_decision_console_manual_acceptance_checklist.md`

Verifier lock: Retail Decision Console Status: static/demo shell with layout, local placeholder interactions, snapshot export, local QA bundle, and manual acceptance checklist; no live data, recommendations, confidence scoring, active DecisionObjects, broker controls, order buttons, or execution.

## Manual Acceptance Scope

The checklist covers:

- preflight commands for install, audit, verifier, full pytest, and `git diff --check`
- preview commands for `--help`, `--no-gui`, `--print-snapshot`, and local JSON snapshot export
- QA bundle commands for `--help` and local bundle creation
- visual acceptance criteria for title, safety banner, demo/unavailable state, layout zones, sections, cards, and static interactions
- safety acceptance criteria for no live data, recommendations, action generation, confidence scoring, active DecisionObjects, broker controls, order buttons, execution, credentials, provider setup, broker setup, background fetches, or API calls at import
- snapshot acceptance criteria for demo/unavailable/local/read-only flags, false dangerous flags, and no secret/credential/live decision content
- QA bundle acceptance criteria for manifest, snapshot, no-GUI, and safety summary artifacts
- failure criteria and a copy-paste acceptance verdict template

## Manual Acceptance Failure Criteria

Manual acceptance fails if any active buy, sell, execute, order, or broker
control appears; if recommendation or confidence appears as output; if live
market data is claimed; if an API, provider, or broker call is required; if
credentials are requested; if an execution path appears; if a snapshot
contains secrets; or if a QA bundle contains decision or trading content.

## Manual Acceptance Safety Posture

Manual acceptance does not certify production readiness, trading readiness,
recommendation readiness, strategy readiness, data-quality readiness, live
provider readiness, broker readiness, order readiness, or execution readiness.

It preserves:

- no live data
- no generated recommendations
- no action generation
- no confidence scoring
- no active DecisionObjects
- no broker controls
- no order buttons
- no execution APIs

Prompt 104 adds no product runtime behavior, no production package, no Windows
installer, no market-data integration, no decision intelligence, no broker
integration, and no execution path.

## Prompt 104 Documentation And Test Policy

Prompt 104 follows the phase-level docs/tests policy. It updates this
canonical phase doc, adds one manual acceptance checklist runbook, and adds
grouped phase/boundary tests only. It does not create prompt-level audit docs,
one doc per forbidden capability, or one test file per forbidden capability.

## Prompt 105 Shareable Internal Preview Package

Prompt 105 implements Retail Decision Console Shareable Internal Preview
Package.
Historical transition reference: Prompt 105 - Retail Decision Console Shareable Internal Preview Package.

Implementation stage marker: `internal_preview_package`.

The internal preview package scope is local internal demo review only. It adds
a safe package manifest model, local internal preview builder script, internal
preview runbook, internal review notes template, grouped tests, and status/audit
updates. The package collects runbooks, QA bundle outputs, the manual
acceptance checklist, static/demo preview snapshot references, no-GUI preview
summary, safety summary, README, and review notes into one local output
directory.

Verifier lock: Retail Decision Console Status: static/demo shell with layout, local placeholder interactions, snapshot export, local QA bundle, manual acceptance checklist, and shareable internal preview package; no live data, recommendations, confidence scoring, active DecisionObjects, broker controls, order buttons, or execution.

## Internal Preview Package Artifacts

Prompt 105 adds:

- `packages/core/stark_terminal_core/retail_decision_console/internal_preview_package.py`
- `scripts/build_retail_decision_console_internal_preview.py`
- `docs/runbooks/retail_decision_console_internal_preview_package.md`
- `docs/templates/retail_decision_console_internal_review_notes.md`
- grouped phase, boundary, and script tests

The internal preview package writes these local artifacts under the selected
output directory:

- `internal_preview_manifest.json`
- `README_INTERNAL_PREVIEW.md`
- `preview_snapshot.json`
- `preview_snapshot.md`
- `no_gui_preview.txt`
- `safety_summary.txt`
- `manual_acceptance_checklist.md`
- `manual_smoke_test.md`
- `local_preview_runbook.md`
- `local_qa_bundle_runbook.md`
- `internal_review_notes.md`

Every artifact remains local, demo-only, unavailable, read-only, and
non-executive.

## Internal Preview Purpose

The internal preview package helps reviewers confirm:

- preview documentation exists
- manual smoke testing guidance exists
- local QA bundle guidance exists
- manual acceptance checklist is included
- generated snapshot artifacts are present
- no-GUI preview output is present
- safety summary is present
- internal review notes template is present
- safety boundaries remain visible
- no live data, recommendation, confidence scoring, DecisionObject, broker,
  order, or execution behavior exists

The internal preview package is not a production package, not a Windows
installer, not a signed binary, not deployment, not live market data, not data
ingestion, not a decision engine, not a recommendation engine, not a
confidence report, not an active DecisionObject, not broker integration, not
order infrastructure, and not an execution surface.

## Internal Preview Safety Posture

The internal preview package must preserve:

- `demo_only: true`
- `unavailable: true`
- `local_only: true`
- `read_only: true`
- `not_production_ready: true`
- `not_trading_ready: true`
- `not_recommendation_ready: true`
- `not_execution_ready: true`
- no secrets
- no credentials
- no live data
- no generated recommendations
- no action generation
- no confidence scoring
- no active DecisionObject generation
- no broker controls
- no order buttons
- no execution APIs

Generated internal preview artifacts must not be treated as production
readiness, trading readiness, recommendation readiness, confidence output,
DecisionObjects, broker/order controls, or execution artifacts.

## Prompt 105 Documentation And Test Policy

Prompt 105 follows the grouped docs/tests policy. It adds one internal
preview package module, one internal preview package builder script, one
internal preview package runbook, one internal review notes template, grouped
phase/boundary/script tests, one concise prompt-log entry, and concise
safety/status updates. It adds no micro-audit docs and no one-test-file per
forbidden capability.

## Prompt 106 Internal Preview Package Smoke Verification

Prompt 106 implements Retail Decision Console Internal Preview Package Smoke
Verification.
Historical transition reference: Prompt 106 - Retail Decision Console Internal Preview Package Smoke Verification.

Implementation stage marker: `internal_preview_smoke_verification`.

The smoke verification scope is local QA only. It adds a smoke verification
model, a local smoke verification script, grouped tests, and status/audit
updates for the existing internal preview package. It does not create a
production package, Windows installer, signed binary, deployment automation,
live market data, recommendation engine, confidence scoring, active
DecisionObjects, broker controls, order buttons, execution APIs, or runtime
decision capability.

Verifier lock: Retail Decision Console Status: internal preview package smoke-verified; still static/demo/unavailable only; no live data, recommendations, confidence scoring, active DecisionObjects, broker controls, order buttons, or execution.

## Internal Preview Smoke Artifacts Verified

Prompt 106 verifies these local package artifacts:

- `internal_preview_manifest.json`
- `README_INTERNAL_PREVIEW.md`
- `preview_snapshot.json`
- `preview_snapshot.md`
- `no_gui_preview.txt`
- `safety_summary.txt`
- `manual_acceptance_checklist.md`
- `manual_smoke_test.md`
- `local_preview_runbook.md`
- `local_qa_bundle_runbook.md`
- `internal_review_notes.md`

The smoke verification helper is:

- `packages/core/stark_terminal_core/retail_decision_console/internal_preview_smoke.py`

The smoke verification script is:

- `scripts/smoke_verify_retail_decision_console_internal_preview.py`

## Internal Preview Smoke Safety Checks

Smoke verification checks:

- package directory exists
- every required package artifact exists
- manifest JSON loads and validates
- manifest says `demo_only: true`
- manifest says `unavailable: true`
- manifest says `local_only: true`
- manifest says `read_only: true`
- manifest says `not_production_ready: true`
- manifest says `not_trading_ready: true`
- manifest says `not_recommendation_ready: true`
- manifest says `not_execution_ready: true`
- dangerous flags remain false
- artifact paths stay under the selected package directory
- artifacts include no secrets, credentials, live decision content, active
  recommendations, confidence score output, active DecisionObject output,
  broker controls, order buttons, or execution controls

## Internal Preview Smoke Commands

Use these commands after building the internal preview package:

```bash
.venv/bin/python scripts/smoke_verify_retail_decision_console_internal_preview.py --help
.venv/bin/python scripts/smoke_verify_retail_decision_console_internal_preview.py --package-dir tmp/retail_decision_console_internal_preview --print-summary
```

The smoke command is local-only. It does not require the API server, live data,
credentials, provider setup, broker setup, market data fetching, background
workers, order controls, or execution paths.

## Prompt 106 Documentation And Test Policy

Prompt 106 follows the grouped docs/tests policy. It updates this canonical
phase doc, updates the internal preview package runbook, adds one smoke
verification helper, one safe smoke verification script, and grouped tests
only. It does not create prompt-level audit docs, one doc per forbidden
capability, or one test file per forbidden capability.

## Prompt 107 Internal Preview Milestone Closure

Prompt 107 implements Retail Decision Console Internal Preview Milestone
Closure.
Historical transition reference: Prompt 107 - Retail Decision Console Internal Preview Milestone Closure.

Implementation stage marker: `internal_preview_milestone_closed`.

The Retail Decision Console internal preview milestone is closed. The current
preview is static/demo/unavailable/read-only and is safe for internal local
preview only. It is not production ready, not trading ready, not
recommendation ready, and not execution ready.

Verifier lock: Retail Decision Console Status: internal preview milestone closed; static/demo/unavailable/read-only only; no live data, recommendations, confidence scoring, active DecisionObjects, broker controls, order buttons, or execution.

## Internal Preview Milestone Scope

The closed internal preview milestone covers:

- Prompt 95 productization plan and UI shell boundary
- Prompt 96 UI shell skeleton
- Prompt 97 demo/static state model
- Prompt 98 static state wiring into desktop shell
- Prompt 99 local preview runbook and manual smoke test
- Prompt 100 visual polish and section layout pass
- Prompt 101 static interaction placeholders
- Prompt 102 preview snapshot export
- Prompt 103 local QA bundle
- Prompt 104 manual acceptance checklist
- Prompt 105 shareable internal preview package
- Prompt 106 internal preview smoke verification
- Prompt 107 milestone closure

## Closed Milestone Artifact Inventory

The internal preview milestone inventory includes:

- desktop shell module: `apps/desktop/stark_terminal_desktop/retail_decision_console.py`
- demo/static state modules: `static_state.py`, `demo_state.py`, and `state_safety.py`
- layout module: `layout.py`
- interaction module: `interactions.py`
- snapshot export module: `snapshot_export.py`
- QA bundle module: `qa_bundle.py`
- internal preview package module: `internal_preview_package.py`
- internal preview smoke module: `internal_preview_smoke.py`
- preview script: `scripts/preview_retail_decision_console.py`
- QA bundle script: `scripts/build_retail_decision_console_qa_bundle.py`
- internal preview package script: `scripts/build_retail_decision_console_internal_preview.py`
- smoke verification script: `scripts/smoke_verify_retail_decision_console_internal_preview.py`
- local preview runbook: `docs/runbooks/retail_decision_console_local_preview.md`
- manual smoke test runbook: `docs/runbooks/retail_decision_console_manual_smoke_test.md`
- local QA bundle runbook: `docs/runbooks/retail_decision_console_local_qa_bundle.md`
- manual acceptance checklist: `docs/runbooks/retail_decision_console_manual_acceptance_checklist.md`
- internal preview package runbook: `docs/runbooks/retail_decision_console_internal_preview_package.md`
- internal review notes template: `docs/templates/retail_decision_console_internal_review_notes.md`
- grouped phase, boundary, API, desktop, script, package, smoke, and milestone tests

## Milestone Closure Safety Verdict

The closed internal preview remains:

- static/demo only
- unavailable
- local-only
- read-only
- safe for internal local preview only
- not production ready
- not trading ready
- not recommendation ready
- not execution ready

It has:

- no live data
- no recommendations
- no action generation
- no confidence scoring
- no active DecisionObjects
- no broker controls
- no order buttons
- no execution APIs

Internal preview artifacts must not be treated as live market intelligence,
validated research, recommendations, confidence output, active DecisionObjects,
broker/order controls, or execution artifacts.

## Prompt 107 Documentation And Test Policy

Prompt 107 follows the grouped docs/tests policy. It updates this canonical
phase doc and status/audit docs, adds grouped phase and boundary closure tests
only, and creates no prompt-level audit docs, no one-doc-per-forbidden-
capability files, and no one-test-file-per-forbidden-capability files.

## Commit And Push Recommendation

After verification passes, commit and push before starting the next phase:

```bash
git status
git add .
git commit -m "Close retail decision console internal preview milestone"
git push
```

## Prompt 107 Next Phase Recommendation

Prompt 108 - Retail Decision Console Post-Preview UX Backlog and Next Product
Phase Selection should start only after commit/push. It should choose the next
safe product phase from Retail Console UX polish v2, Data Quality Surface,
Instrument Universe Readiness Surface, Regime/State Display Contract, or
Decision Candidate Future Contract while adding no live data, recommendations,
confidence scoring, active DecisionObjects, broker controls, order buttons, or
execution.

## Visual Layout Scope

Prompt 100 adds:

- `packages/core/stark_terminal_core/retail_decision_console/layout.py`
- visual layout metadata on the static shell view-model
- grouped section rendering in the desktop shell
- layout zone reporting in `scripts/preview_retail_decision_console.py --no-gui`

The layout descriptor remains demo-only, unavailable, read-only, and local.
It is not a data source, not decision intelligence, not a recommendation
engine, not broker infrastructure, and not an execution surface.

## Layout Zones

The static/demo shell now describes these layout zones:

- `HEADER` for app title, safety banner, demo/unavailable status, and no-live-data notice
- `CONTROLS` for instrument, timeframe, market/session, and disabled refresh placeholders
- `PRIMARY` for decision summary and regime/state placeholders
- `SECONDARY` for evidence and risk/invalidation placeholders
- `CONTEXT` for options and research context placeholders
- `FOOTER` for journal and settings/help placeholders

Every layout section carries section id, title, subtitle, zone, priority,
placeholder text, demo/unavailable labels, provenance labels, and false
dangerous flags.

## Section And Card Ordering

Prompt 100 orders the visible shell as:

1. Top zone and safety banner.
2. Control placeholder row.
3. Primary decision shell.
4. Evidence and risk shell.
5. Context shell.
6. Journal and settings shell.

Cards remain unavailable demo placeholders. Visual polish must not make
demo/static state appear live, validated, actionable, or executable.

## Visual Preview Behavior

The local preview keeps the same safe commands:

- `.venv/bin/python scripts/preview_retail_decision_console.py --no-gui`
- `.venv/bin/python scripts/preview_retail_decision_console.py`

The `--no-gui` summary now prints the visual layout stage, layout zones, and
section grouping. GUI rendering, when PySide6 is available, groups static
labels into header, controls, primary, secondary, context, and footer zones.

No API server, credentials, live provider, broker setup, live market data,
background worker, timer, order control, or execution path is required.

## Local Preview Runbook Scope

Prompt 99 adds:

- `docs/runbooks/retail_decision_console_local_preview.md`
- `docs/runbooks/retail_decision_console_manual_smoke_test.md`
- `scripts/preview_retail_decision_console.py`

The preview helper prints this safety banner:

`Demo/static preview only - no live data, no recommendations, no execution`

The script can print the descriptor/view-model summary with `--no-gui` and can
launch the static/demo desktop shell only when PySide6 is available. It starts
no event loop at import, starts no timers or threads at import, fetches no data
at import, and calls no APIs at import.

## Manual Smoke Test Scope

The smoke test checklist covers:

- automated preflight verification
- safe preview launch
- missing PySide6 fallback
- title and safety banner checks
- section and card visibility checks
- demo/static/unavailable labels
- no live data
- no recommendations
- no action generation
- no confidence scoring
- no active DecisionObjects
- no broker controls
- no order buttons
- no execution
- clean exit with no provider or broker call

The checklist is a manual QA aid only. It does not add decision intelligence,
data ingestion, live market data, recommendations, confidence scoring, broker
controls, order buttons, or execution.

## Static State View-Model Scope

Prompt 98 creates:

- `RetailDecisionConsoleShellViewModel`
- `RetailDecisionConsoleSectionViewModel`
- `RetailDecisionConsoleCardViewModel`
- `retail_decision_console_state_view_model()`
- `map_demo_state_to_shell_descriptor()`
- `map_demo_sections_to_ui_sections()`
- `map_demo_cards_to_ui_cards()`

The state-to-view mapping preserves:

- `demo_only: true`
- `unavailable: true`
- read-only posture
- demo/static/unavailable provenance labels
- no live data
- no recommendations
- no action generation
- no confidence scoring
- no active DecisionObject generation
- no broker controls
- no order buttons
- no execution

Every mapped section/card carries a title, placeholder text,
unavailable/demo label, provenance/demo label, and safety flags. The safety
flags remain false for live data, recommendations, action generation,
confidence scoring, active DecisionObject generation, broker controls, order
buttons, and execution.

## Visible Shell Behavior

When a QApplication exists, the desktop shell may render static labels and
placeholder cards from the view-model. When PySide6 is unavailable, or when no
QApplication is running, the desktop module returns an import-safe fallback
containing the shell descriptor and static/demo view-model.

The visible shell banner is:

`Demo/static shell only - no live data, no recommendations, no execution`

The shell must remain a product surface skeleton. It contains no timers, no
background threads, no API fetches at import, no live provider calls, no
broker/order controls, and no active decision labels.

## Static State View-Model Endpoint Posture

Prompt 98 adds one GET-only/read-only metadata endpoint:

- `/retail-decision-console/static-state-view-model`

The endpoint returns the static/demo shell view-model only. It exposes no POST
endpoints, no recommendation endpoint, no confidence endpoint, no broker
endpoint, no order endpoint, and no execution endpoint.

## Local Preview Endpoint Posture

Prompt 99 adds no API endpoint. Existing Retail Decision Console endpoints
remain GET-only and read-only. The local preview helper uses the local
descriptor/view-model path and does not require an API server.

## Demo Static State Scope

Prompt 97 creates:

- `RetailDecisionConsoleStaticState`
- `RetailDecisionConsoleSectionState`
- `RetailDecisionConsoleCardState`
- `RetailDecisionConsoleProvenanceState`
- `RetailDecisionConsoleUnavailableReason`
- deterministic `retail_decision_console_demo_state()`
- grouped state safety helpers
- GET `/retail-decision-console/demo-state`

All generated values are static placeholders. They are not live market data,
not real instrument data, not indicator outputs, not regime detection, not
options analytics, not strategy output, and not decision-support output.

## Demo And Unavailable Provenance Rules

The demo state provenance must clearly state demo/static/unavailable. It must
not imply source validation, data-quality validation, live market intelligence,
trusted research status, or decision readiness.

Every section and card state must remain:

- demo only
- unavailable
- local/static only
- no live data
- no recommendation
- no action generation
- no confidence score
- no active DecisionObject
- no broker control
- no order button
- no execution

## Section And Card State Placeholders

Prompt 97 static state includes placeholders for:

- header/status banner
- instrument selector placeholder
- timeframe selector placeholder
- market/session placeholder
- disabled refresh placeholder
- decision summary placeholder
- regime/state placeholder
- evidence panel placeholder
- risk/invalidation placeholder
- options context placeholder
- research context placeholder
- journal placeholder
- settings placeholder

Cards are unavailable demo placeholders only. They cannot contain active
decision labels, confidence-like numeric scores, recommendations, broker
controls, order buttons, or execution controls.

## Demo State Endpoint Posture

Prompt 97 adds one GET-only/read-only metadata endpoint:

- `/retail-decision-console/demo-state`

The endpoint returns demo/static/unavailable state metadata only. It exposes
no POST endpoints, no recommendation endpoint, no confidence endpoint, no
broker endpoint, no order endpoint, and no execution endpoint.

## Desktop Shell Scope

The desktop shell scope includes:

- `apps/desktop/stark_terminal_desktop/retail_decision_console.py`
- import-safe PySide6 detection
- fallback descriptor mode when PySide6 is unavailable or no QApplication is running
- static labels only when a QApplication exists
- no live API calls
- no background threads
- no timers fetching data
- no market data requests
- no active buttons that imply orders, broker actions, recommendations, or execution

## UI Shell Sections

Prompt 96 UI shell sections are:

- header/status banner
- instrument selector placeholder
- timeframe selector placeholder
- market/session placeholder
- disabled refresh placeholder
- decision summary placeholder
- regime/state placeholder
- evidence panel placeholder
- risk/invalidation placeholder
- options context placeholder
- research context placeholder
- journal placeholder
- settings placeholder

Each section is unavailable and skeleton/demo only. Each section states no live
data, no recommendation, no generated action state, no confidence score, no
active DecisionObject, no broker control, and no execution.

## What Appears In The Shell

The shell may show:

- the title
- the safety banner
- static placeholder section titles
- static unavailable/demo descriptions
- settings, journal, and help/about placeholders as non-executive concepts

It must not show active trading controls, generated action labels,
recommendation cards, confidence/probability scores, broker controls, order
buttons, or live market data claims.

## UI Shell Unavailable Rules

The following must remain unavailable:

- live data
- generated recommendations
- action generation
- confidence scoring
- active DecisionObjects
- live market data claims
- broker controls
- order buttons
- execution APIs

## Relationship To Decision Desk

The Retail Decision Console is the user-facing productization layer for the
Decision Desk direction. Decision Desk remains the deeper decision-support
architecture and safety model. Retail Decision Console turns that architecture
into a future desktop-facing shell without bypassing evidence validation,
human review, data-quality checks, or execution prohibitions.

Decision candidate is not a trade. The console must never create a direct
signal-to-trade path.

## Intended Future User Flow

The intended future user flow is:

1. Open the console shell.
2. Select an instrument and timeframe.
3. See unavailable/demo status until validated data and decision evidence exist.
4. Review future decision summary, evidence, risk, invalidation, regime,
   options, research, and journal sections.
5. Record context for review without generating actions, confidence scores,
   broker controls, order buttons, or execution.

## Intended Future Surface Sections

The safe shell boundary allows placeholder concepts for:

- app frame placeholder
- top navigation placeholder
- instrument selector placeholder
- timeframe selector placeholder
- status banner placeholder
- decision summary placeholder
- evidence panel placeholder
- risk/invalidation placeholder
- regime/state placeholder
- options context placeholder
- research context placeholder
- journal link placeholder
- settings link placeholder

These are placeholders only and do not render an active UI with live decision
support.

## UI Shell Boundary

The UI shell boundary forbids:

- active recommendation cards
- active buy/sell/hold/watch/avoid generation
- confidence scoring
- active DecisionObjects
- broker controls
- order buttons
- execution controls
- live market data claims

No active UI implementation is added by Prompt 95. The backend metadata route
exists only to describe the safe future shell surface.

## Placeholders Created

Prompt 95 creates placeholders for:

- productization plan
- UI shell boundary
- navigation items
- decision summary, evidence, risk/invalidation, regime/state, options,
  research, and journal sections
- decision bias, evidence, risk, invalidation, regime, options context, and
  research context cards
- unavailable/demo state
- readiness and health metadata

Cards and sections cannot display active generated recommendations, generated
confidence scores, active DecisionObjects, live market data, broker controls,
or execution controls.

## Unavailable And Demo-State Rules

Retail Decision Console output remains unavailable by default. Demo or shell
states must be labeled as unavailable/skeleton/demo until data quality,
provenance, and decision validation are implemented.

The unavailable state requires:

- unavailable: true
- allowed_stage: productization_plan
- live decisions disabled
- recommendations disabled
- action generation disabled
- confidence scoring disabled
- active DecisionObject generation disabled
- live market data disabled
- broker controls disabled
- order buttons disabled
- execution disabled

## Readiness Rules

The phase is ready for:

- productization plan
- UI shell skeleton

The phase is not ready for:

- live decisions
- recommendations
- action generation
- confidence scoring
- active DecisionObject generation
- live market data display or live market data claims
- broker controls
- order buttons
- execution

## Read-Only Endpoint Posture

Prompt 95 adds GET-only/read-only metadata endpoints:

- `/retail-decision-console/health`
- `/retail-decision-console/productization-plan`
- `/retail-decision-console/ui-boundary`
- `/retail-decision-console/readiness`
- `/retail-decision-console/unavailable-state`
- `/retail-decision-console/navigation-placeholder`
- `/retail-decision-console/section-placeholder`
- `/retail-decision-console/card-placeholder`
- `/retail-decision-console/demo-state`
- `/retail-decision-console/static-state-view-model`

No POST endpoints exist for the Retail Decision Console route family.

## What Remains Forbidden

The following remain forbidden:

- live decisions
- active recommendations
- buy/sell/hold/watch/avoid output
- action generation
- confidence scoring
- active DecisionObject generation
- live market data claims
- treating synthetic/local data as trusted live market intelligence
- broker controls
- order buttons
- execution APIs
- order placement
- approvals/overrides
- readiness-to-trade
- hidden trading logic
- active strategy/backtest recommendations

Verifier lock: no live decisions, no active recommendations, no action generation, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs.

## Safety Verdict

Prompt 95 adds productization and UI shell boundary metadata only. It adds no
runtime decision capability, no fake recommendations, no fake confidence, no
live data claims, no broker controls, no order buttons, and no active trading.

Execution APIs remain forbidden.

## Phase-Based Docs/Tests Policy

Prompt 96 follows the phase-based docs/tests policy. It adds UI descriptor
modules, one desktop shell module, grouped phase/boundary/desktop tests, one
concise prompt-log entry, and concise safety/status updates. It adds no
micro-audit docs and no one-test-file per forbidden capability.

Prompt 97 follows the phase-based docs/tests policy. It adds static/demo state
modules, one GET-only metadata endpoint, grouped phase/boundary/API tests, one
concise prompt-log entry, and concise safety/status updates. It adds no
micro-audit docs and no one-test-file per forbidden capability.

Prompt 98 follows the grouped docs/tests policy. It adds one state view-model
module, one GET-only metadata endpoint, grouped phase/boundary/desktop/API
tests, one concise prompt-log entry, and concise safety/status updates. It
adds no micro-audit docs and no one-test-file per forbidden capability.

Prompt 99 follows the grouped docs/tests policy. It adds two runbooks, one
safe preview helper script, grouped phase/boundary/script tests, one concise
prompt-log entry, and concise safety/status updates. It adds no micro-audit
docs and no one-test-file per forbidden capability.

Prompt 100 follows the grouped docs/tests policy. It adds one layout
descriptor module, grouped phase/boundary/desktop tests, one concise
prompt-log entry, and concise safety/status updates. It adds no micro-audit
docs and no one-test-file per forbidden capability.

Prompt 101 follows the grouped docs/tests policy. It adds one static
interaction descriptor module, grouped phase/boundary/desktop tests, one
concise prompt-log entry, and concise safety/status updates. It adds no
micro-audit docs and no one-test-file per forbidden capability.

Prompt 102 follows the grouped docs/tests policy. It adds one snapshot export
module, preview-script snapshot flags, grouped phase/boundary/script tests,
one concise prompt-log entry, and concise safety/status updates. It adds no
micro-audit docs and no one-test-file per forbidden capability.

Prompt 103 follows the grouped docs/tests policy. It adds one QA bundle
module, one local QA bundle script, one runbook, grouped
phase/boundary/script tests, one concise prompt-log entry, and concise
safety/status updates. It adds no micro-audit docs and no one-test-file per
forbidden capability.

Prompt 104 follows the grouped docs/tests policy. It adds one manual
acceptance checklist runbook, grouped phase/boundary tests, one concise
prompt-log entry, and concise safety/status updates. It adds no micro-audit
docs and no one-test-file per forbidden capability.

Prompt 105 follows the grouped docs/tests policy. It adds one internal
preview package module, one internal preview package builder script, one
internal preview package runbook, one internal review notes template, grouped
phase/boundary/script tests, one concise prompt-log entry, and concise
safety/status updates. It adds no micro-audit docs and no one-test-file per
forbidden capability.

Prompt 95 follows the phase-based docs/tests policy. It adds one canonical
phase doc, grouped phase/boundary/API tests, one concise prompt-log entry, and
concise safety/status updates. It adds no micro-audit docs and no one-test-file
per forbidden capability.

## Next Phase Recommendation

Prompt 108 - Retail Decision Console Post-Preview UX Backlog and Next Product
Phase Selection.

Prompt 108 should start only after commit/push. It should decide the next
product phase while keeping the current Retail Decision Console preview
static/demo/unavailable/read-only and adding no live data, recommendations,
confidence scoring, active DecisionObjects, broker controls, order buttons, or
execution.
