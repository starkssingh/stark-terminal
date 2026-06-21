from __future__ import annotations

from pathlib import Path

import polars as pl

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.domain.market_data import MarketDataBar
from stark_terminal_data_platform.lake.parquet_io import read_parquet_frame, write_parquet_frame


def bars_to_polars_frame(bars: list[MarketDataBar]) -> pl.DataFrame:
    rows = []
    for bar in bars:
        provider = bar.provider
        rows.append(
            {
                "instrument_id": str(bar.instrument_id),
                "symbol": bar.instrument_id.symbol,
                "exchange": bar.instrument_id.exchange.value,
                "segment": bar.instrument_id.segment.value,
                "timeframe": bar.timeframe.value,
                "timestamp": bar.timestamp,
                "open": bar.open,
                "high": bar.high,
                "low": bar.low,
                "close": bar.close,
                "volume": bar.volume,
                "open_interest": bar.open_interest,
                "provider_name": provider.name if provider else None,
                "provider_type": provider.provider_type.value if provider else None,
                "quality_status": bar.quality_status.value,
                "source_data_reference": bar.source_data_reference,
            }
        )
    return pl.DataFrame(rows)


def _target_is_configured_output_root(path: Path, settings: Settings) -> bool:
    target = path.resolve(strict=False)
    root = Path(settings.synthetic_fixture_output_root).resolve(strict=False)
    return target == root or root in target.parents


def write_fixture_bars_to_parquet(
    bars: list[MarketDataBar],
    path: str | Path,
    compression: str | None = None,
    settings: Settings | None = None,
) -> Path:
    resolved = settings or get_settings()
    target = Path(path)
    if not resolved.synthetic_fixture_allow_disk_writes and _target_is_configured_output_root(target, resolved):
        raise ValueError("synthetic fixture disk writes are disabled for configured output root")
    frame = bars_to_polars_frame(bars)
    return write_parquet_frame(frame, target, compression=compression or resolved.parquet_compression)


def read_fixture_bars_from_parquet(path: str | Path) -> pl.DataFrame:
    return read_parquet_frame(path)
