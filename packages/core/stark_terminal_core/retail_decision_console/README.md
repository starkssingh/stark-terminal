# Retail Decision Console

Retail Decision Console is the flagship product surface planning package for
Stark Terminal. It defines productization, UI shell boundary, navigation,
section, card, unavailable-state, readiness, and health contracts.

The package is productization-plan-only. It does not implement live decisions,
recommendations, action generation, confidence scoring, active DecisionObject
generation, live market data display, broker controls, order buttons, or
execution APIs.

Prompt 96 adds UI shell skeleton descriptors and safety helpers only. The
desktop shell remains static/skeleton-only and exposes no live data, no
recommendations, no confidence scores, no active DecisionObjects, no broker
controls, no order buttons, and no execution path.

Prompt 97 adds deterministic demo/static state contracts and safety helpers
only. Demo state is local, static, unavailable, and read-only; it exposes no
live market data, recommendations, action generation, confidence scoring,
active DecisionObjects, broker controls, order buttons, or execution path.

Prompt 98 wires the demo/static state into a shell view-model and desktop
fallback/window rendering path. The wiring remains demo-only, unavailable, and
non-executive; it adds no live data, recommendation, action generation,
confidence scoring, active DecisionObject, broker control, order button, or
execution path.

Prompt 99 adds local preview and manual smoke test runbooks plus a safe
preview helper script. The preview uses the existing static/demo shell path,
requires no API server or credentials, and adds no live data, recommendation,
confidence scoring, active DecisionObject, broker control, order button, or
execution path.

Prompt 100 adds visual layout descriptors, layout zones, section grouping,
card ordering metadata, improved static desktop grouping, and clearer
descriptor preview output. The shell remains demo/static, unavailable, and
non-executive; it adds no live data, recommendation, action generation,
confidence scoring, active DecisionObject, broker control, order button, or
execution path.

Prompt 101 adds static interaction placeholders for local-only section
toggles, static tab selection, unavailable reasons, provenance labels, safety
information, placeholder refresh, and static instrument/timeframe placeholder
selection. Interactions remain demo-only, unavailable, read-only, and local;
they add no live data, recommendation, action generation, confidence scoring,
active DecisionObject, broker control, order button, or execution path.

Prompt 102 adds local preview snapshot export for QA and documentation. The
snapshot is generated from the static shell view-model, supports JSON,
Markdown, and text output, and remains demo-only, unavailable, local-only, and
read-only. It contains no secrets, credentials, live data, recommendations,
confidence scores, active DecisionObjects, broker controls, order buttons, or
execution path.

Prompt 103 adds a local QA bundle for review readiness. The bundle collects a
manifest, preview snapshot JSON, preview snapshot Markdown, no-GUI preview
summary, safety summary, and runbook copies under a local output directory.
It remains demo-only, unavailable, local-only, and read-only. It contains no
secrets, credentials, live data, recommendations, confidence scores, active
DecisionObjects, broker controls, order buttons, or execution path.

Prompt 104 adds the manual acceptance checklist for the static/demo product
surface. Acceptance remains local-demo-review only; it does not certify
production readiness, trading readiness, recommendation readiness, confidence
readiness, DecisionObject readiness, broker readiness, order readiness, or
execution readiness.

Prompt 105 adds a shareable internal preview package for internal demo review.
The package writes a manifest, README, preview snapshots, no-GUI summary,
safety summary, copied runbooks/checklists, and internal review notes under a
local output directory. It remains demo-only, unavailable, local-only, and
read-only. It contains no secrets, credentials, live data, recommendations,
confidence scores, active DecisionObjects, broker controls, order buttons, or
execution path, and it is not production/trading/recommendation/execution
ready.

Prompt 106 adds local smoke verification for the internal preview package. The
smoke verifier checks required package artifacts, manifest safety flags,
readiness-blocking markers, snapshot/runbook inclusion, and sensitive-content
markers. It remains local-only and verification-only; it adds no live data,
recommendations, confidence scoring, active DecisionObjects, broker controls,
order buttons, production package, installer, or execution path.

Prompt 107 closes the Retail Decision Console internal preview milestone. The
closed milestone is safe for internal local preview only and remains
static/demo, unavailable, local-only, read-only, not production ready, not
trading ready, not recommendation ready, and not execution ready. It adds no
live data, recommendations, confidence scoring, active DecisionObjects, broker
controls, order buttons, production package, installer, deployment, or
execution path.
