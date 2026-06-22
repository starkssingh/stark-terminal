# OHLCV Export Manifest Policy

Prompt 19 requires every synthetic OHLCV research lake export to produce a `DatasetManifest`.

## Export Identity

- `export_id` must be stable, non-empty, and safe.
- `dataset_name` and `version` must be safe identifiers with no traversal.
- Export requests must be synthetic-only.
- `source_data_reference` must clearly include synthetic/local/test semantics.

## DatasetManifest Requirements

Each exported synthetic OHLCV dataset must record:

- dataset id mapped from `export_id`
- dataset name and version
- kind `OHLCV`
- format `PARQUET`
- zone, normally `RESEARCH_ARTIFACTS`
- row count
- relative output path
- schema map
- source data reference
- partitions such as exchange, symbol, and timeframe

## Storage Policy

Prompt 19 performs no production research lake writes by default. Tests must write only to temporary paths. Exported files must be DuckDB-readable and Parquet schema must include instrument, symbol, exchange, segment, timeframe, timestamp, OHLCV fields, provider identity, quality status, and source data reference.

## Safety Policy

Prompt 19 allows no real-market-data exports, no external calls, no scraping, no execution APIs, no analytics, no trading signals, and no trading interpretation of exported datasets. Synthetic exports are local/test artifacts only.

The implementation is developed on Mac mini M2 / macOS / Apple Silicon and remains path-portable for the Windows-native Stark Terminal target.
