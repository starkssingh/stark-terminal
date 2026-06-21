from pathlib import Path

import polars as pl
import pytest

from stark_terminal_data_platform.lake.parquet_io import (
    count_parquet_rows,
    inspect_parquet_schema,
    read_parquet_frame,
    write_parquet_frame,
)


def test_parquet_roundtrip_with_polars_frame(tmp_path: Path) -> None:
    frame = pl.DataFrame({"symbol": ["NIFTY", "RELIANCE"], "close": [100.5, 2500.0]})
    path = tmp_path / "nested" / "sample.parquet"

    written_path = write_parquet_frame(frame, path, compression="zstd")
    restored = read_parquet_frame(written_path)
    schema = inspect_parquet_schema(written_path)

    assert written_path.exists()
    assert restored.shape == (2, 2)
    assert count_parquet_rows(written_path) == 2
    assert "symbol" in schema
    assert "close" in schema


def test_write_parquet_rejects_unsupported_compression(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        write_parquet_frame(pl.DataFrame({"x": [1]}), tmp_path / "x.parquet", compression="zip")
