# Validation Rule Spec

Prompt 13 defines the validation contracts used by Stark Terminal's Data Quality + Validation Framework.

## ValidationIssue

ValidationIssue fields:

- `code`: stable issue code
- `severity`: INFO, WARNING, ERROR, or CRITICAL
- `message`: sanitized human-readable message
- `field`: optional field name
- `scope`: validation scope
- `value_preview`: optional short sanitized preview
- `remediation`: optional sanitized remediation note

Issues must not leak secrets, credentials, tokens, raw URLs, broker secrets, or provider credentials.

## ValidationRule

ValidationRule fields:

- `rule_id`
- `name`
- `rule_type`
- `scope`
- `severity`
- `description`
- `enabled`
- `parameters`
- `schema_version`

Parameters must be JSON-serializable and must not contain secret-like keys.

## ValidationResult

ValidationResult fields:

- `status`
- `scope`
- `subject_id`
- `rule_id`
- `issues`
- `checked_at`
- `metadata`

PASS results cannot contain issues. FAIL and BLOCKED results require ERROR or CRITICAL issues.

## ValidationReport

ValidationReport fields:

- `report_id`
- `scope`
- `subject_id`
- `status`
- `results`
- `issue_count`
- `warning_count`
- `error_count`
- `critical_count`
- `generated_at`
- `schema_version`
- `source_data_reference`
- `notes`

Report counts must match result issues.

## Statuses, Severities, Scopes, And Rule Types

Statuses: PASS, WARN, FAIL, BLOCKED, UNKNOWN.

Severities: INFO, WARNING, ERROR, CRITICAL.

Scopes include instruments, universes, market data bars, market data requests/responses, options snapshots, dataset manifests, feature snapshots, feature quality reports, warehouse table contracts, provider responses, and UNKNOWN.

Rule types include required fields, range checks, consistency checks, uniqueness checks, timestamp checks, source reference checks, schema checks, contract checks, security checks, and custom checks.

Future rules may validate provider response completeness, adjusted bar continuity, research lake manifests, point-in-time dataset integrity, warehouse contract compatibility, and feature snapshot freshness. Prompt 13 implements local contracts only and no production validation pipelines.

No execution APIs. No market data ingestion. No analytics signals.
