# Retail Decision Console Internal Preview Package Runbook

## Purpose

This runbook builds a shareable internal preview package for the current
Retail Decision Console static/demo surface. The package collects the local
preview runbook, manual smoke test, local QA bundle runbook, manual acceptance
checklist, preview snapshot artifacts, no-GUI preview summary, safety summary,
and internal review notes template into one local directory.

The package is for internal demo review only. It is not production ready, not
trading ready, not recommendation ready, and not execution ready.

## Safety Posture

The internal preview package has:

- no live data
- no recommendations
- no action generation
- no confidence scoring
- no active DecisionObjects
- no broker controls
- no order buttons
- no execution

It does not require credentials, provider setup, broker setup, live market
data, an API server, production packaging, signed binaries, deployment, or a
Windows installer.

## Exact Commands

Run standard verification first:

```bash
.venv/bin/python -m pip install -e .
.venv/bin/python scripts/audit_foundation.py
.venv/bin/python scripts/verify_foundation.py
.venv/bin/pytest
git diff --check
```

Build the local internal preview package:

```bash
.venv/bin/python scripts/build_retail_decision_console_internal_preview.py --output-dir tmp/retail_decision_console_internal_preview --clean --print-manifest
```

Inspect command help:

```bash
.venv/bin/python scripts/build_retail_decision_console_internal_preview.py --help
```

Smoke-verify the built local package:

```bash
.venv/bin/python scripts/smoke_verify_retail_decision_console_internal_preview.py --help
.venv/bin/python scripts/smoke_verify_retail_decision_console_internal_preview.py --package-dir tmp/retail_decision_console_internal_preview --print-summary
```

## Output Directory

The default output directory is:

```text
tmp/retail_decision_console_internal_preview
```

The script writes local files only. It does not require the API server and
does not fetch external data.

## Generated Artifacts

The package writes:

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

## How To Inspect The Package

Inspect `README_INTERNAL_PREVIEW.md` and `internal_preview_manifest.json`
first. They must state:

- `stage: internal_preview_package`
- `demo_only: true`
- `unavailable: true`
- `local_only: true`
- `read_only: true`
- `not_production_ready: true`
- `not_trading_ready: true`
- `not_recommendation_ready: true`
- `not_execution_ready: true`
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

Inspect `safety_summary.txt`. It must clearly state not production ready, not
trading ready, not recommendation ready, not execution ready, no live data, no
recommendations, no confidence scoring, no active DecisionObjects, no broker
controls, no order buttons, and no execution.

## How To Share Internally

Share the generated local directory only after the manual acceptance checklist
has been completed for internal demo review. The package may be zipped or
copied manually by the reviewer, but this runbook does not create an
installer, signed binary, deployment artifact, or production release.

Reviewers should read:

- `README_INTERNAL_PREVIEW.md`
- `manual_acceptance_checklist.md`
- `manual_smoke_test.md`
- `safety_summary.txt`
- `internal_review_notes.md`

## Reviewer Checks

Reviewers should verify:

- the safety banner is visible in README, manifest, no-GUI output, and safety summary
- snapshot artifacts state demo-only, unavailable, local-only, and read-only
- QA evidence exists through the copied runbooks and snapshot artifacts
- the acceptance checklist is included
- internal review notes include an internal-demo-only verdict
- no artifact implies production readiness
- no artifact implies trading readiness
- no artifact implies recommendation readiness
- no artifact implies execution readiness

## Smoke Verification

Prompt 106 adds local smoke verification for the internal preview package.
Smoke verification checks:

- package directory exists
- `internal_preview_manifest.json` exists
- `README_INTERNAL_PREVIEW.md` exists
- `preview_snapshot.json` exists
- `preview_snapshot.md` exists
- `no_gui_preview.txt` exists
- `safety_summary.txt` exists
- `manual_acceptance_checklist.md` exists
- `manual_smoke_test.md` exists
- `local_preview_runbook.md` exists
- `local_qa_bundle_runbook.md` exists
- `internal_review_notes.md` exists
- manifest says `demo_only: true`
- manifest says `unavailable: true`
- manifest says `local_only: true`
- manifest says `read_only: true`
- manifest says `not_production_ready: true`
- manifest says `not_trading_ready: true`
- manifest says `not_recommendation_ready: true`
- manifest says `not_execution_ready: true`
- dangerous flags remain false
- artifacts contain no secrets, credentials, live decision content,
  recommendation output, confidence score output, active DecisionObject
  output, broker controls, order buttons, or execution controls

Expected smoke output includes:

```text
Retail Decision Console internal preview smoke verification - demo/static only, no live data, no recommendations, no execution
Passed: true
```

Smoke verification is local QA only. It does not certify production readiness,
trading readiness, recommendation readiness, confidence readiness,
DecisionObject readiness, broker readiness, order readiness, or execution
readiness.

Smoke verification fails if any required artifact is missing, the manifest
does not validate, dangerous flags are true, package artifact paths escape the
selected package directory, secret/credential markers appear, or any artifact
implies live data, recommendations, confidence scoring, active DecisionObjects,
broker controls, order buttons, or execution controls.

## QA Bundle Checks

Reviewers should verify:

- QA bundle guidance is included in `local_qa_bundle_runbook.md`
- preview snapshot JSON and Markdown are present
- no-GUI preview summary is present
- safety summary is present
- all QA-derived artifacts remain demo/static/unavailable
- no QA-derived artifact contains secrets, credentials, live data,
  recommendations, confidence scoring, active DecisionObjects, broker
  controls, order controls, or execution data

## Acceptance Checklist Checks

Reviewers should verify:

- `manual_acceptance_checklist.md` is present
- the checklist states it is not production acceptance
- the checklist states it is not trading-readiness acceptance
- the checklist states it is not recommendation-readiness acceptance
- the checklist states it is not execution-readiness acceptance
- internal review notes capture accepted/rejected for internal demo review only

## Cleanup

Generated internal preview packages are disposable local artifacts. Remove
them after review unless they are intentionally kept outside versioned source:

```bash
rm -rf tmp/retail_decision_console_internal_preview
```

Smoke verification creates no separate retained artifact by default.

## Limitations

The internal preview package does not create production packaging, a Windows
installer, signed binaries, deployment, auto-updates, live market data,
provider integrations, recommendation logic, confidence scoring,
DecisionObject generation, broker controls, order controls, or execution.

## Next Development Step

Prompt 107 - Retail Decision Console Internal Preview Milestone Closure closes
the internal preview milestone after verification. Commit/push is recommended
before Prompt 108 - Retail Decision Console Post-Preview UX Backlog and Next
Product Phase Selection. Prompt 108 should do no live data, recommendation,
confidence, DecisionObject, broker, order, or execution work.
