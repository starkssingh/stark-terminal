# Retail Decision Console Manual Smoke Test

Use this checklist after automated verification to confirm the local static/demo
preview is safe and visibly unavailable.

This smoke test is lighter than the full manual acceptance checklist. Use
`docs/runbooks/retail_decision_console_manual_acceptance_checklist.md` when a
human reviewer needs to accept or reject the static/demo product surface before
local internal sharing.

Use `docs/runbooks/retail_decision_console_internal_preview_package.md` after
acceptance when a reviewer needs the shareable internal preview package. The
package remains demo/static/unavailable and is not production, trading,
recommendation, or execution readiness.

## Preflight

- [ ] `.venv/bin/python -m pip install -e .` passes.
- [ ] `.venv/bin/python scripts/audit_foundation.py` passes.
- [ ] `.venv/bin/python scripts/verify_foundation.py` passes.
- [ ] `.venv/bin/pytest` passes.
- [ ] `git diff --check` passes.

## Launch

- [ ] `.venv/bin/python scripts/preview_retail_decision_console.py --no-gui`
      launches safely.
- [ ] `.venv/bin/python scripts/preview_retail_decision_console.py` launches
      the GUI only when PySide6 is available.
- [ ] No credentials are requested.
- [ ] No network, provider, or broker prompt appears.
- [ ] Missing PySide6 fallback is safe and prints a descriptor/view-model
      summary.

## Visual Checks

- [ ] Title shows `Stark Terminal — Retail Decision Console`.
- [ ] Safety banner is visible.
- [ ] Demo/static/unavailable label is visible.
- [ ] Header/status banner section is visible.
- [ ] Instrument selector placeholder is visible.
- [ ] Timeframe selector placeholder is visible.
- [ ] Market/session placeholder is visible.
- [ ] Disabled refresh placeholder is visible.
- [ ] Decision summary placeholder is visible.
- [ ] Regime/state placeholder is visible.
- [ ] Evidence panel placeholder is visible.
- [ ] Risk/invalidation placeholder is visible.
- [ ] Options context placeholder is visible.
- [ ] Research context placeholder is visible.
- [ ] Journal placeholder is visible.
- [ ] Settings placeholder is visible.

## Visual Layout Checks

- [ ] Top banner is highly visible.
- [ ] Control row is visible.
- [ ] Primary decision summary placeholder is visible.
- [ ] Secondary evidence and risk sections are visible.
- [ ] Context sections are visible.
- [ ] Journal/settings shell is visible.
- [ ] No active decision widgets are visible.
- [ ] No broker/order controls are visible.

## Static Interaction Checks

- [ ] Static interaction summary appears in `--no-gui` output.
- [ ] Section toggle placeholder appears if implemented.
- [ ] Static tab or placeholder-zone selection appears if implemented.
- [ ] Unavailable reason placeholder appears.
- [ ] Provenance/demo label placeholder appears.
- [ ] Safety information placeholder appears.
- [ ] Local placeholder refresh is clearly demo/static/unavailable.
- [ ] Static instrument/timeframe placeholder selection remains local-only.
- [ ] Interactions do not fetch data.
- [ ] Interactions do not create decisions.
- [ ] Interactions do not expose broker/order/execution controls.

## Snapshot Export Checks

- [ ] `.venv/bin/python scripts/preview_retail_decision_console.py --print-snapshot`
      prints a local preview snapshot.
- [ ] `.venv/bin/python scripts/preview_retail_decision_console.py --export-snapshot tmp/preview_snapshots/retail_decision_console_snapshot.json --snapshot-format json`
      writes a local JSON file.
- [ ] The snapshot states `demo_only: true`.
- [ ] The snapshot states `unavailable: true`.
- [ ] The snapshot states `local_only: true`.
- [ ] The snapshot states `read_only: true`.
- [ ] The snapshot states no live data.
- [ ] The snapshot states no recommendations.
- [ ] The snapshot states no confidence scoring.
- [ ] The snapshot states no active DecisionObjects.
- [ ] The snapshot states no broker controls.
- [ ] The snapshot states no order buttons.
- [ ] The snapshot states no execution.
- [ ] The snapshot contains no secrets.
- [ ] The snapshot contains no credentials.
- [ ] Local snapshot files are removed after smoke testing unless intentionally retained outside versioned source.

## Local QA Bundle Checks

- [ ] `.venv/bin/python scripts/build_retail_decision_console_qa_bundle.py --output-dir tmp/retail_decision_console_qa_bundle --clean --print-manifest`
      writes a local QA bundle.
- [ ] `manifest.json` exists.
- [ ] `preview_snapshot.json` exists.
- [ ] `preview_snapshot.md` exists.
- [ ] `no_gui_preview.txt` exists.
- [ ] `safety_summary.txt` exists.
- [ ] Local preview runbook copy exists.
- [ ] Manual smoke test runbook copy exists.
- [ ] All generated files state demo/static/unavailable or preserve
      demo-only/unavailable/read-only flags.
- [ ] All generated files state no live data.
- [ ] All generated files state no recommendations.
- [ ] All generated files state no confidence scoring.
- [ ] All generated files state no active DecisionObjects.
- [ ] All generated files state no broker controls.
- [ ] All generated files state no order buttons.
- [ ] All generated files state no execution.
- [ ] Generated files contain no secrets.
- [ ] Generated files contain no credentials.

## Manual Acceptance Reference

- [ ] Full acceptance review uses `docs/runbooks/retail_decision_console_manual_acceptance_checklist.md`.
- [ ] Internal preview sharing uses `docs/runbooks/retail_decision_console_internal_preview_package.md`.
- [ ] Smoke-test results are treated as input to acceptance review, not as
      production readiness, trading readiness, recommendation readiness, or
      execution readiness.

## Safety Checks

- [ ] No buy button exists.
- [ ] No sell button exists.
- [ ] No execute button exists.
- [ ] No place order button exists.
- [ ] No broker connect button exists.
- [ ] No live signal is shown.
- [ ] No active recommendation is shown.
- [ ] No confidence score is shown.
- [ ] No active DecisionObject is shown.
- [ ] No order controls exist.
- [ ] No execution controls exist.
- [ ] The preview states no live data.
- [ ] The preview states no recommendations.
- [ ] The preview states no confidence scoring.
- [ ] The preview states no active DecisionObjects.
- [ ] The preview states no broker controls.
- [ ] The preview states no order buttons.
- [ ] The preview states no execution.

## Exit

- [ ] Preview closes cleanly.
- [ ] No background thread remains.
- [ ] No local secret file is created.
- [ ] No local cache file is created.
- [ ] No provider call is made.
- [ ] No broker call is made.
