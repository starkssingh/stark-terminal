# Parquet Data Zones

The research lake uses explicit data zones. These zones organize future datasets by transformation and reproducibility state. Prompt 04 creates contracts only; it does not ingest market data.

## raw

Purpose: Provider-native or minimally transformed extracts.

Future examples: Raw exchange bhavcopy files, vendor bar exports, option-chain snapshots, corporate action source files.

Not allowed yet: Real provider ingestion, scraping, credentials, or generated market datasets checked into the repo.

Expectations: Every future raw dataset needs source reference, provider identity, ingestion timestamp, and terms-compliant acquisition.

## cleaned

Purpose: Data after basic cleanup such as type correction, duplicate handling, and obvious malformed-row rejection.

Future examples: Cleaned OHLCV bars, cleaned instrument files, cleaned option snapshots.

Not allowed yet: Provider-specific cleaning pipelines before adapter contracts exist.

Expectations: Cleaning rules must be versioned and auditable.

## normalized

Purpose: Canonical Stark schemas aligned across providers and exchanges.

Future examples: Normalized instruments, bars, derivatives contracts, market-state snapshots.

Not allowed yet: Canonical live market datasets without provider adapter and quality contracts.

Expectations: Normalized datasets must link back to raw/cleaned inputs.

## feature_ready

Purpose: Datasets prepared for feature computation and model/research workflows.

Future examples: Aligned bars, corporate-action adjusted panels, joined instrument metadata, factor inputs.

Not allowed yet: Feature store implementation or model training pipelines.

Expectations: Feature-ready data must include transformation lineage and schema versions.

## backtest_ready

Purpose: Deterministic datasets suitable for reproducible backtesting.

Future examples: Point-in-time bars, adjusted panels, survivorship-controlled universes, validated options snapshots.

Not allowed yet: Backtesting engine implementation or strategy results in Prompt 04.

Expectations: Backtest-ready datasets must be deterministic and auditable.

## research_artifacts

Purpose: Research outputs, experiment artifacts, notebooks exports, manifests, and reports.

Current synthetic examples: Prompt 19 synthetic OHLCV Parquet exports with DatasetManifest linkage, validation-before-export, and DuckDB readback verification in temporary test paths.

Future examples: Experiment summaries, feature studies, validation reports, synthetic test fixtures.

Not allowed yet: Production strategy promotion or execution artifacts.

Expectations: Artifacts should reference input datasets, code/rule version, and audit context where applicable.

Prompt 19 exports are synthetic-only. They are not real market data, not real market ingestion, not provider-sourced data, not analytics signals, not trading decisions, and not execution APIs.
