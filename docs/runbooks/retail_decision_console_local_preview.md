# Retail Decision Console Local Preview Runbook

## Purpose

This runbook launches the Retail Decision Console static/demo desktop shell for
local preview. The preview is for product-surface QA only. It is demo/static,
unavailable, read-only, and non-executive.

## Safety Posture

The local preview has:

- no live data
- no recommendations
- no action generation
- no confidence scoring
- no active DecisionObjects
- no broker controls
- no order buttons
- no execution

It does not require credentials, provider setup, broker setup, live market
data, an API server, or production deployment.

## Prerequisites

- Python virtual environment created in `.venv`.
- Editable install completed.
- Optional PySide6 desktop dependency if a GUI window is desired.
- No credentials, provider tokens, broker accounts, or live market data feeds
  are required.

## Automated Verification First

Run the standard project verification before previewing:

```bash
.venv/bin/python -m pip install -e .
.venv/bin/python scripts/audit_foundation.py
.venv/bin/python scripts/verify_foundation.py
.venv/bin/pytest
git diff --check
```

## Launch The Static/Demo Preview

Use the safe descriptor-only preview first:

```bash
.venv/bin/python scripts/preview_retail_decision_console.py --no-gui
```

If PySide6 is installed and a local GUI preview is desired, run:

```bash
.venv/bin/python scripts/preview_retail_decision_console.py
```

The script prints or displays:

```text
Demo/static preview only — no live data, no recommendations, no execution
```

The `--no-gui` output also prints `Layout stage: visual_layout_pass`,
`Static interactions:`, the static interaction placeholders, the layout
zones, and the static section grouping.

## Export A Local Preview Snapshot

Prompt 102 adds local preview snapshot export for QA documentation. The
snapshot is generated from the static/demo shell view-model and remains
demo-only, unavailable, local-only, read-only, and non-executive.

Print a JSON snapshot to stdout:

```bash
.venv/bin/python scripts/preview_retail_decision_console.py --print-snapshot
```

Print a Markdown snapshot to stdout:

```bash
.venv/bin/python scripts/preview_retail_decision_console.py --print-snapshot --snapshot-format markdown
```

Write a local JSON snapshot:

```bash
.venv/bin/python scripts/preview_retail_decision_console.py --export-snapshot tmp/preview_snapshots/retail_decision_console_snapshot.json --snapshot-format json
```

Markdown and text exports are also supported with `--snapshot-format markdown`
or `--snapshot-format text`.

## Build A Local QA Bundle

Prompt 103 adds a local QA bundle that collects the manifest, preview
snapshot, no-GUI output, safety summary, and runbook copies into one local
directory:

```bash
.venv/bin/python scripts/build_retail_decision_console_qa_bundle.py --output-dir tmp/retail_decision_console_qa_bundle --clean --print-manifest
```

Use this runbook when you only need to launch or inspect the preview. Use
`docs/runbooks/retail_decision_console_local_qa_bundle.md` when you need a
reviewable local artifact set for QA.

Use `docs/runbooks/retail_decision_console_manual_acceptance_checklist.md`
when the static/demo product surface needs a full human acceptance review
before local internal sharing. The local preview runbook is for launch and
inspection; the manual acceptance checklist is the broader review gate.

Use `docs/runbooks/retail_decision_console_internal_preview_package.md` when
the accepted static/demo surface needs a shareable internal review package.
The internal preview package wraps local preview, QA bundle, smoke test, and
acceptance checklist artifacts; it is still not production, trading,
recommendation, or execution readiness.

The QA bundle remains demo/static, unavailable, local-only, read-only, and
non-executive. It adds no live data, recommendations, confidence scoring,
active DecisionObjects, broker controls, order buttons, or execution.

## Verify Snapshot Safety

Every exported snapshot must state:

- demo_only true
- unavailable true
- local_only true
- read_only true
- no secrets
- no credentials
- no live data
- no recommendations
- no confidence scoring
- no active DecisionObjects
- no broker controls
- no order buttons
- no execution

The snapshot is a local QA artifact only. It must not be treated as market
intelligence, a recommendation, a confidence report, a DecisionObject, or an
execution artifact.

## Clean Up Local Snapshots

Generated local snapshots are disposable preview artifacts. Remove them after
manual verification unless they are intentionally kept outside versioned
source:

```bash
rm -rf tmp/preview_snapshots
```

## Verify The Safety Banner

Confirm the preview shows or prints the banner:

- Demo/static preview only
- no live data
- no recommendations
- no execution

The shell must not imply validated decision support.

## Verify Sections And Cards

Confirm the preview exposes these static/demo sections:

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

Every section and card must be labeled demo/static/unavailable.

## Verify Static Interaction Placeholders

Confirm the `--no-gui` output lists static interactions such as:

- section toggle placeholder
- static tab placeholder
- unavailable reason placeholder
- provenance label placeholder
- safety info placeholder
- local placeholder refresh
- static instrument placeholder select
- static timeframe placeholder select

Each line must state `demo-only unavailable local-only`. The interactions must
not fetch data, generate recommendations, recalculate confidence, create
DecisionObjects, expose order controls, or execute anything.

## Expected Visual Zones

Prompt 100 groups the static/demo shell into:

- top zone with title, safety banner, demo/unavailable status, and no-live-data notice
- control placeholder row with instrument, timeframe, market/session, and disabled refresh placeholders
- primary decision shell
- evidence and risk shell
- context shell for options and research
- journal and settings shell

The visual polish must not make placeholder state appear live, validated,
actionable, or executable.

## Verify Demo/Unavailable State

Check that all displayed state remains:

- demo only
- static
- unavailable
- read-only
- not live market intelligence
- not a recommendation
- not an action state
- not a confidence score
- not an active DecisionObject
- not a broker control
- not an order button
- not execution-ready

## Exit Safely

Close the preview window normally, or press `Ctrl+C` in the terminal if only
the descriptor summary was printed. The preview must leave no background
thread, provider call, broker call, credential file, cache file, or execution
state behind.

## Missing PySide6

If PySide6 is unavailable, the helper prints the safe descriptor/view-model
summary and exits successfully. This is expected on environments that have not
installed desktop extras.

Optional GUI dependency install remains:

```bash
.venv/bin/python -m pip install -e ".[desktop]"
```

## Expected Limitations

The preview does not fetch market data, compute indicators, detect regimes,
run options analytics, generate recommendations, score confidence, create
DecisionObjects, connect to brokers, expose order buttons, or execute trades.

## Next Development Step

Prompt 104 - Retail Decision Console Manual Acceptance Checklist should define
the human acceptance checklist for the current demo/static product surface.
It must add no live data, recommendations, confidence scoring, active
DecisionObjects, broker controls, order buttons, or execution.
