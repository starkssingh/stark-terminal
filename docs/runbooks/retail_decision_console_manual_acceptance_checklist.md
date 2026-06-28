# Retail Decision Console Manual Acceptance Checklist

## Purpose

This checklist is the manual acceptance checklist for the current static/demo
Retail Decision Console product surface.

It is not production acceptance. It is not trading-readiness acceptance. It is
not recommendation-readiness acceptance. It is not execution-readiness
acceptance.

Verifier phrases: not production acceptance; not trading-readiness acceptance;
not recommendation-readiness acceptance; not execution-readiness acceptance.

Implementation stage marker: `manual_acceptance_checklist`.

Acceptance scope: local demo preview only. The accepted surface must remain
demo/static, unavailable, local-only, read-only, and non-executive.

## Preflight Checks

Run these commands before any preview review:

```bash
.venv/bin/python -m pip install -e .
.venv/bin/python scripts/audit_foundation.py
.venv/bin/python scripts/verify_foundation.py
.venv/bin/pytest
git diff --check
```

Acceptance requires every preflight command to pass.

## Preview Checks

Run these preview commands:

```bash
.venv/bin/python scripts/preview_retail_decision_console.py --help
.venv/bin/python scripts/preview_retail_decision_console.py --no-gui
.venv/bin/python scripts/preview_retail_decision_console.py --print-snapshot
.venv/bin/python scripts/preview_retail_decision_console.py --export-snapshot tmp/preview_snapshots/retail_decision_console_snapshot.json --snapshot-format json
```

The preview must remain demo/static/unavailable. It must not request
credentials, call providers, call brokers, fetch market data, generate
recommendations, calculate confidence, generate DecisionObjects, expose order
controls, or expose execution controls.

## QA Bundle Checks

Run these QA bundle commands:

```bash
.venv/bin/python scripts/build_retail_decision_console_qa_bundle.py --help
.venv/bin/python scripts/build_retail_decision_console_qa_bundle.py --output-dir tmp/retail_decision_console_qa_bundle --clean --print-manifest
```

The QA bundle must be local-only and must contain only demo/static review
artifacts.

## Internal Preview Package Reference

After acceptance, use the internal preview package runbook when the static/demo
surface needs a shareable internal review package:

```bash
.venv/bin/python scripts/build_retail_decision_console_internal_preview.py --help
.venv/bin/python scripts/build_retail_decision_console_internal_preview.py --output-dir tmp/retail_decision_console_internal_preview --clean --print-manifest
```

The acceptance checklist should be included in the internal preview package.
The package remains internal-demo-review only and does not certify production,
trading, recommendation, confidence, DecisionObject, broker, order, or
execution readiness.

Smoke-verify the built package before sharing it internally:

```bash
.venv/bin/python scripts/smoke_verify_retail_decision_console_internal_preview.py --package-dir tmp/retail_decision_console_internal_preview --print-summary
```

Smoke verification must pass without changing the acceptance scope. It remains
local QA only and does not certify production, trading, recommendation,
confidence, DecisionObject, broker, order, or execution readiness.

## Visual Acceptance Checks

- [ ] Title visible: `Stark Terminal — Retail Decision Console`.
- [ ] Safety banner visible.
- [ ] Demo/static/unavailable status visible.
- [ ] No-live-data notice visible.
- [ ] Layout zones visible.
- [ ] Static sections visible.
- [ ] Static cards visible.
- [ ] Static interactions visible.
- [ ] No active decision widget appears.
- [ ] No broker/order/execution control appears.

## Safety Acceptance Checks

- [ ] No live data.
- [ ] No recommendations.
- [ ] No action generation.
- [ ] No confidence scoring.
- [ ] No active DecisionObjects.
- [ ] No broker controls.
- [ ] No order buttons.
- [ ] No execution.
- [ ] No credentials requested.
- [ ] No provider setup requested.
- [ ] No broker setup requested.
- [ ] No background thread/fetch at import.
- [ ] No API call at import.

## Snapshot Acceptance Checks

- [ ] Snapshot exists.
- [ ] Snapshot says `demo_only: true`.
- [ ] Snapshot says `unavailable: true`.
- [ ] Snapshot says `local_only: true`.
- [ ] Snapshot says `read_only: true`.
- [ ] Dangerous flags are false.
- [ ] Snapshot contains no secrets.
- [ ] Snapshot contains no credentials.
- [ ] Snapshot contains no live data.
- [ ] Snapshot contains no recommendation.
- [ ] Snapshot contains no confidence.
- [ ] Snapshot contains no DecisionObject.
- [ ] Snapshot contains no broker/order/execution content.

## QA Bundle Acceptance Checks

- [ ] `manifest.json` exists.
- [ ] `preview_snapshot.json` exists.
- [ ] Preview snapshot Markdown or text exists.
- [ ] `no_gui_preview.txt` exists.
- [ ] `safety_summary.txt` exists.
- [ ] All artifacts state demo/static/unavailable.
- [ ] No artifact contains secrets.
- [ ] No artifact contains credentials.
- [ ] No artifact contains live decision content.
- [ ] No artifact contains live data.
- [ ] No artifact contains recommendations.
- [ ] No artifact contains confidence scoring.
- [ ] No artifact contains active DecisionObjects.
- [ ] No artifact contains broker controls.
- [ ] No artifact contains order buttons.
- [ ] No artifact contains execution data.

## Failure Criteria

Any of these findings fails manual acceptance:

- Buy, sell, execute, order, or broker active control appears.
- Recommendation or confidence appears as output.
- Live market data is claimed.
- API, provider, or broker call is required.
- Credentials are requested.
- Execution path appears.
- Snapshot contains secrets.
- QA bundle contains decision or trading content.

## Acceptance Verdict Template

```text
Accepted / Rejected:
Date/time:
Commit SHA if available:
Tester:
Commands run:
Observed issues:
Safety verdict:
Next action:
```

## Cleanup

Generated local preview and QA artifacts are disposable. Remove them after
acceptance review unless intentionally kept outside versioned source:

```bash
rm -rf tmp/preview_snapshots tmp/retail_decision_console_qa_bundle
```

## Next Step

Prompt 105 - Retail Decision Console Shareable Internal Preview Package should
create a safe internal preview package structure that references this
checklist, runbooks, QA bundle outputs, and static/demo snapshot artifacts
without adding production packaging, live data, recommendations, confidence
scoring, active DecisionObjects, broker controls, order buttons, or execution.
