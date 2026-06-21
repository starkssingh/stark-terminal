# Quality Gate Policy

Quality gates convert validation reports into conservative decisions for future workflows.

## QualityGatePolicy

QualityGatePolicy fields:

- `policy_id`
- `name`
- `scope`
- `fail_on_error`
- `fail_on_warning`
- `require_source_reference`
- `max_allowed_warnings`
- `max_allowed_errors`
- `schema_version`

Defaults are conservative: errors block, source references are required, and warnings are surfaced for review.

## QualityGateResult

QualityGateResult fields:

- `decision`: ALLOW, WARN, BLOCK, or UNKNOWN
- `policy_id`
- `report_id`
- `reason`
- `evaluated_at`
- `blocking_issues`

## Decisions

- ALLOW: validation report passed the configured gate.
- WARN: validation warnings exist and require review but do not block under the policy.
- BLOCK: validation errors, missing source references, warning/error thresholds, or BLOCKED reports prevent progression.

## Conservative Behavior

Validation failure must never silently pass. Source reference requirements protect auditability. Warning and error thresholds allow future pipelines to fail closed before data reaches ingestion, features, backtests, analytics, or decision-support systems.

No quality gate can enable execution APIs, order placement, broker execution, live trading, real-money routing, or trading execution flows.

Prompt 13 does not run production validation pipelines, does not make external calls, and does not compute analytics signals.
