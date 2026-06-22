# Repositories

This package contains explicit SQLAlchemy repository classes for Stark Terminal persistence operations.

Prompt 15 adds `InstrumentRepository` for instrument metadata only. It uses a caller-provided SQLAlchemy `Session`, performs no engine creation at import time, makes no external calls, persists no OHLCV bars, and exposes no execution APIs.

Prompt 16 adds `MarketDataBatchRepository` for market data batch metadata only. It uses a caller-provided SQLAlchemy `Session`, performs no engine creation at import time, makes no external calls, stores no full OHLCV bars, and exposes no execution APIs.

Prompt 18 adds `OHLCVBarRepository` for synthetic-only OHLCV bars using the existing operational time-series ORM. It remains session-scoped, commits nothing by itself, makes no external calls, and is only used by the synthetic storage service boundary.
