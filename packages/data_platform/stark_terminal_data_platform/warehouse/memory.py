from __future__ import annotations

from copy import deepcopy
from typing import Any


class InMemoryWarehouseQueryRecorder:
    def __init__(self) -> None:
        self._queries: list[dict[str, Any]] = []

    def record(self, query: str, parameters: dict[str, Any] | None = None) -> None:
        if not query.strip():
            raise ValueError("warehouse query cannot be empty")
        self._queries.append({"query": query, "parameters": deepcopy(parameters) if parameters else None})

    def list_queries(self) -> list[dict[str, Any]]:
        return deepcopy(self._queries)

    def clear(self) -> None:
        self._queries.clear()

    def last_query(self) -> dict[str, Any] | None:
        if not self._queries:
            return None
        return deepcopy(self._queries[-1])

    def count(self) -> int:
        return len(self._queries)
