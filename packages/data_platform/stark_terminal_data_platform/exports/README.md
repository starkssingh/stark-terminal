# Stark Terminal Synthetic OHLCV Exports

This package contains the Prompt 19 Synthetic OHLCV to Research Lake Export Contract.

The export path is synthetic-only. It reads validated local/test OHLCV bars from the synthetic storage repository and writes explicit Parquet research artifacts only when a caller provides a safe output path, normally a temporary test directory.

Prompt 19 does not implement real market data ingestion, external provider calls, scraping, analytics, indicators, features, signals, decisions, backtests, production research lake writes, or execution APIs.
