# Data Quality Report Spec

Validation reports are the auditable output of the Data Quality + Validation Framework.

## Report Fields

- `report_id`: stable report identifier
- `scope`: contract or dataset scope
- `subject_id`: validated subject identifier
- `status`: PASS, WARN, FAIL, BLOCKED, or UNKNOWN
- `results`: validation results
- `issue_count`: total issues
- `warning_count`: warning issues
- `error_count`: error issues
- `critical_count`: critical issues
- `generated_at`: UTC generation timestamp
- `schema_version`: validation report schema version
- `source_data_reference`: optional source/audit reference
- `notes`: optional notes

## Counting And Status

Issue counts must match result issues. ERROR issues produce FAIL reports. CRITICAL issues or blocked validation paths produce BLOCKED reports. WARNING issues produce WARN reports unless stronger failures exist.

## Source References

Reports can carry source data references so future ingestion, research lake datasets, warehouse loads, feature snapshots, backtests, and decision-support evidence remain auditable. Source reference requirements are enforced through validators and quality gates, not by uncontrolled external validation.

## Schema Versioning And Auditability

Reports carry schema version and generated timestamp fields so later persistence or event publication can audit which validation framework produced a report. Prompt 13 keeps reports local and serializable. Future prompts may persist reports in PostgreSQL, attach them to dataset manifests, or route summary events through Redis Streams or Kafka/Redpanda after explicit implementation.

Prompt 13 performs no external validation, no real market ingestion, no analytics signals, no feature computation, no ML model training, and no execution APIs.

Development environment remains Mac mini M2 / macOS / Apple Silicon. Target desktop product remains Windows-native Stark Terminal.
