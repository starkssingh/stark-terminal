# Local File Path Safety

Prompt 24 adds path safety for the Local File Provider Adapter v0.

## Allowed Root

Local files must resolve under `LOCAL_FILE_PROVIDER_ALLOWED_ROOT`, which defaults to `data/local_files`. The implementation uses `pathlib` and resolves paths before reading.

The allowed root may be overridden in tests and local development, but it must not contain credentials, tokens, secrets, or provider account material.

## Rejections

The adapter rejects:

- path traversal such as `..`
- absolute paths outside the allowed root
- network paths such as HTTP, S3, GS, FTP, UNC, and `file://`
- unsupported file extensions
- symlink escape outside the allowed root
- symlink use by default
- missing files
- directories
- secret-like path text

Allowed file extensions are `.csv` and `.parquet` only. Row count is capped by `LOCAL_FILE_PROVIDER_MAX_ROWS`, which defaults to `10000`.

## API Safety

Prompt 24 does not expose arbitrary file read API behavior. API callers cannot pass file paths to read local files. The HTTP surface is limited to safe health/contracts metadata.

Local file data is test/dev only. It is not live data, not real market data, not a trading signal, not investment advice, and cannot enable execution APIs.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
