from __future__ import annotations

from pathlib import Path
from typing import Any

import duckdb


class DuckDBClient:
    def __init__(
        self,
        database_path: str | Path | None = None,
        read_only: bool = False,
    ) -> None:
        self.database_path = Path(database_path) if database_path is not None else Path(":memory:")
        self.read_only = read_only
        self._connection: duckdb.DuckDBPyConnection | None = None

    def connect(
        self,
        database_path: str | Path | None = None,
        read_only: bool | None = None,
    ) -> DuckDBClient:
        if database_path is not None:
            self.database_path = Path(database_path)
        if read_only is not None:
            self.read_only = read_only
        if str(self.database_path) != ":memory:":
            self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = duckdb.connect(str(self.database_path), read_only=self.read_only)
        return self

    @property
    def connection(self) -> duckdb.DuckDBPyConnection:
        if self._connection is None:
            self.connect()
        assert self._connection is not None
        return self._connection

    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def execute(self, query: str, parameters: list[Any] | tuple[Any, ...] | None = None) -> Any:
        if parameters is None:
            return self.connection.execute(query)
        return self.connection.execute(query, parameters)

    def query_df(self, query: str, parameters: list[Any] | tuple[Any, ...] | None = None) -> Any:
        return self.execute(query, parameters).pl()

    def query_parquet(self, path_or_glob: str | Path, limit: int | None = None) -> Any:
        if limit is not None and limit <= 0:
            raise ValueError("limit must be positive when provided")
        query = "SELECT * FROM read_parquet(?)"
        parameters: list[Any] = [str(path_or_glob)]
        if limit is not None:
            query = f"{query} LIMIT ?"
            parameters.append(limit)
        return self.query_df(query, parameters)

    def __enter__(self) -> DuckDBClient:
        return self.connect()

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()
