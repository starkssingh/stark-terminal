# Sample Data Policy

Prompt 14 sample data must be synthetic unless a future prompt explicitly documents otherwise.

## Rules

- no real production data checked into the repository.
- no scraping.
- no API calls.
- no provider SDK calls.
- no live-data claims.
- no trading decisions from sample data.
- no sample data as trade signal.
- no execution APIs.
- disk writes are disabled by default for the configured synthetic fixture output root.

Synthetic fixtures are local-only and test/dev only. They are not real market data, not trading data, not investment advice, and have no external provider source.

## Disk Writes

Prompt 14 writes fixture data only when explicitly called. Tests must use temporary directories for tiny Parquet roundtrips. No generated fixture datasets should be committed to the repository.

## Future Real Data

Future real data requires read-only provider adapters, data policy review, provider terms review, source references, Data Quality Framework gates, audit metadata, and an explicit implementation prompt.

Until then, no real market data ingestion, no NSE/BSE scraping, no external provider calls, no analytics signals, no feature computation, no generated decisions, and no broker or trading execution behavior are allowed.

Development environment remains Mac mini M2 / macOS / Apple Silicon. Target desktop product remains Windows-native Stark Terminal.
