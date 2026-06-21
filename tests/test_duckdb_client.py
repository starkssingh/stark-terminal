from pathlib import Path

import polars as pl
import pytest

from stark_terminal_data_platform.lake.duckdb_client import DuckDBClient
from stark_terminal_data_platform.lake.parquet_io import write_parquet_frame


def test_duckdb_client_executes_select(tmp_path: Path) -> None:
    with DuckDBClient(tmp_path / "research.duckdb") as client:
        result = client.execute("SELECT 1").fetchone()

    assert result == (1,)


def test_duckdb_client_queries_temporary_parquet(tmp_path: Path) -> None:
    parquet_path = write_parquet_frame(
        pl.DataFrame({"symbol": ["NIFTY", "BANKNIFTY"], "close": [100.0, 200.0]}),
        tmp_path / "sample.parquet",
    )

    with DuckDBClient(tmp_path / "research.duckdb") as client:
        result = client.query_parquet(parquet_path, limit=1)

    assert result.shape == (1, 2)
    assert result["symbol"][0] == "NIFTY"


def test_duckdb_client_limit_validation(tmp_path: Path) -> None:
    with DuckDBClient(tmp_path / "research.duckdb") as client:
        with pytest.raises(ValueError):
            client.query_parquet(tmp_path / "missing.parquet", limit=0)
