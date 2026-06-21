from __future__ import annotations

from pathlib import Path
from typing import Any

import polars as pl
import pyarrow.parquet as pq


SUPPORTED_PARQUET_COMPRESSIONS = {"zstd", "snappy", "gzip", "none"}


def _normalize_compression(compression: str) -> str:
    normalized = compression.strip().lower()
    if normalized not in SUPPORTED_PARQUET_COMPRESSIONS:
        raise ValueError("Unsupported Parquet compression")
    return "uncompressed" if normalized == "none" else normalized


def write_parquet_frame(frame: Any, path: str | Path, compression: str = "zstd") -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    normalized_compression = _normalize_compression(compression)

    if not isinstance(frame, pl.DataFrame):
        frame = pl.DataFrame(frame)
    frame.write_parquet(target, compression=normalized_compression)
    return target


def read_parquet_frame(path: str | Path) -> pl.DataFrame:
    return pl.read_parquet(Path(path))


def inspect_parquet_schema(path: str | Path) -> dict[str, str]:
    schema = pq.read_schema(Path(path))
    return {field.name: str(field.type) for field in schema}


def count_parquet_rows(path: str | Path) -> int:
    metadata = pq.ParquetFile(Path(path)).metadata
    return metadata.num_rows
