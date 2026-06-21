# Synthetic Fixtures Package

This package contains local synthetic fixtures for Stark Terminal tests and development.

Prompt 14 fixtures are:

- synthetic
- local-only
- test/dev only
- not real market data
- not trading or investment data
- not sourced from an external provider

Prompt 14 does not ingest real data, scrape exchanges, call provider APIs, compute analytics signals, compute features, run backtests, generate decisions, or expose execution APIs.

Disk writes are disabled by default for the configured fixture output root. Tests may explicitly write tiny Parquet roundtrips to temporary directories.

Future real ingestion must use read-only provider adapters, data-policy review, source references, and Data Quality Framework gates.
