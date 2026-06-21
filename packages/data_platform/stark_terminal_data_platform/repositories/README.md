# Repositories

This package contains explicit SQLAlchemy repository classes for Stark Terminal persistence operations.

Prompt 15 adds `InstrumentRepository` for instrument metadata only. It uses a caller-provided SQLAlchemy `Session`, performs no engine creation at import time, makes no external calls, persists no OHLCV bars, and exposes no execution APIs.

Prompt 16 adds `MarketDataBatchRepository` for market data batch metadata only. It uses a caller-provided SQLAlchemy `Session`, performs no engine creation at import time, makes no external calls, stores no full OHLCV bars, and exposes no execution APIs.
