# Feature Quality Policy

Feature quality reports make future features auditable before they are used in analytics, decisions, backtests, or models.

## Quality Report Fields

FeatureQualityReport includes:

- `report_id`
- `feature_set_name`
- `feature_set_version`
- `status`
- `row_count`
- `missing_value_count`
- `stale_value_count`
- `invalid_value_count`
- `warnings`
- `errors`
- `generated_at`
- `source_data_reference`

Counts must be non-negative. PASS reports cannot contain errors.

## Status Meaning

- `PASS`: No blocking errors were found.
- `WARN`: Quality issues exist but may be reviewable.
- `FAIL`: Quality issues are blocking.
- `UNKNOWN`: Quality has not been established.

## Warning And Error Handling

Warnings and errors must be sanitized. They must not contain credentials, tokens, API keys, broker references, or other secrets.

## Why Quality Matters

Features cannot be trusted without quality reports. Later versions must not promote a feature into decision evidence, model training, regime analysis, or backtesting unless source references, freshness, missingness, validity, and lineage are available.

## Prompt 10 Boundary

Prompt 10 creates quality report contracts only. It does not compute features, scan market data, calculate missingness from real datasets, implement model training, or create trade calls.

## Prompt 13 Validation Framework Link

Prompt 13 adds the broader Data Quality + Validation Framework around these contracts. It can validate FeatureQualityReport and FeatureSnapshot objects locally and deterministically, but it still does not compute features, run production validation pipelines, generate analytics signals, or create trade calls.
