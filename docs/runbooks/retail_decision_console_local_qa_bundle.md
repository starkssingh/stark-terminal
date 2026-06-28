# Retail Decision Console Local QA Bundle Runbook

## Purpose

This runbook builds a local QA bundle for the Retail Decision Console
static/demo shell. The bundle collects review artifacts for local product QA:
manifest, preview snapshot, no-GUI preview output, safety summary, and runbook
copies.

The bundle is demo/static, unavailable, local-only, read-only, and
non-executive. It is not packaging, an installer, deployment, live market
data, recommendation logic, confidence scoring, DecisionObject generation,
broker control, order control, or execution.

## Safety Posture

The local QA bundle has:

- no live data
- no recommendations
- no action generation
- no confidence scoring
- no active DecisionObjects
- no broker controls
- no order buttons
- no execution

It does not require credentials, provider setup, broker setup, live market
data, an API server, packaging tools, or production deployment.

## Exact Commands

Run standard verification first:

```bash
.venv/bin/python -m pip install -e .
.venv/bin/python scripts/audit_foundation.py
.venv/bin/python scripts/verify_foundation.py
.venv/bin/pytest
git diff --check
```

Build the local QA bundle:

```bash
.venv/bin/python scripts/build_retail_decision_console_qa_bundle.py --output-dir tmp/retail_decision_console_qa_bundle --clean --print-manifest
```

Inspect command help:

```bash
.venv/bin/python scripts/build_retail_decision_console_qa_bundle.py --help
```

## Output Directory

The default output directory is:

```text
tmp/retail_decision_console_qa_bundle
```

The script writes local files only. It does not require the API server and
does not fetch external data.

## Generated Artifacts

The bundle writes:

- `manifest.json`
- `preview_snapshot.json`
- `preview_snapshot.md`
- `no_gui_preview.txt`
- `safety_summary.txt`
- `retail_decision_console_local_preview.md`
- `retail_decision_console_manual_smoke_test.md`

## What To Inspect

Inspect `manifest.json` first. It must state:

- `stage: local_qa_bundle`
- `demo_only: true`
- `unavailable: true`
- `local_only: true`
- `read_only: true`
- false dangerous flags
- no secrets marker
- no credentials marker
- no live data marker
- no recommendation marker
- no execution marker

Inspect `preview_snapshot.json` and `preview_snapshot.md` next. They must
remain static/demo snapshots and must not contain live market data,
recommendations, confidence scores, active DecisionObjects, broker controls,
order controls, or execution data.

Inspect `no_gui_preview.txt`. It must include the safety banner and the static
layout/interaction summary only.

Inspect `safety_summary.txt`. It must clearly state no live data, no
recommendations, no confidence scoring, no active DecisionObjects, no broker
controls, no order buttons, and no execution.

The generated artifacts feed the manual acceptance review in
`docs/runbooks/retail_decision_console_manual_acceptance_checklist.md`. The QA
bundle collects evidence for review; it does not certify production readiness,
trading readiness, recommendation readiness, or execution readiness.

Prompt 105 adds `docs/runbooks/retail_decision_console_internal_preview_package.md`.
The internal preview package wraps or references QA bundle artifacts alongside
the local preview runbook, manual smoke test, manual acceptance checklist,
preview snapshot, no-GUI summary, safety summary, and internal review notes.
It remains a local internal demo review package only.

## Safety Banner Checks

The bundle output must include:

```text
Retail Decision Console QA bundle — demo/static only, no live data, no recommendations, no execution
```

The no-GUI preview artifact must also include:

```text
Demo/static preview only — no live data, no recommendations, no execution
```

## Snapshot Checks

Confirm the snapshot artifacts state:

- demo_only true
- unavailable true
- local_only true
- read_only true
- no live data
- no recommendations
- no confidence scoring
- no active DecisionObjects
- no broker controls
- no order buttons
- no execution
- no secrets
- no credentials

## No-GUI Summary Checks

Confirm `no_gui_preview.txt` lists:

- shell title
- static state stage
- visual layout stage
- static interaction count
- layout zones
- static/demo sections

Every item must remain demo/static/unavailable. The summary must not imply
live decision support.

## Cleanup

Generated QA bundles are disposable local artifacts. Remove them after review
unless they are intentionally kept outside versioned source:

```bash
rm -rf tmp/retail_decision_console_qa_bundle
```

## Limitations

The local QA bundle does not create a production package, Windows installer,
signed binary, deployment artifact, live market-data integration, decision
engine, recommendation engine, confidence scoring engine, DecisionObject
generator, broker integration, order surface, or execution path.

## Next Development Step

Prompt 104 - Retail Decision Console Manual Acceptance Checklist defines the
human acceptance checklist for the current demo/static product surface before
sharing the preview internally.

Prompt 105 - Retail Decision Console Shareable Internal Preview Package should
create a safe internal preview package structure using the runbooks, QA bundle
outputs, acceptance checklist template, and static/demo snapshot references
without adding live data, recommendations, confidence scoring, active
DecisionObjects, broker controls, order buttons, or execution.
