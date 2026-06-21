# Stark Terminal Research Lake

This package contains the DuckDB + Parquet research lake foundation.

Prompt 04 does not ingest real data and does not implement analytics engines. Operational TimescaleDB storage is for application time-series state; the research lake is for reproducible analytical datasets, temporary local research queries, and future backtest/feature-ready data products.

The dataset registry is an in-memory placeholder. Persistent registry storage will come later, likely through PostgreSQL and the Stark Feature Registry.
