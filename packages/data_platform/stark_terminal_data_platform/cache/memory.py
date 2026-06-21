from __future__ import annotations

from time import monotonic
from typing import Any


class InMemoryCache:
    """Local/test cache fallback. This is not durable storage."""

    def __init__(self) -> None:
        self._items: dict[str, tuple[Any, float | None]] = {}

    def _is_expired(self, key: str) -> bool:
        item = self._items.get(key)
        if item is None:
            return False
        _, expires_at = item
        if expires_at is None:
            return False
        if expires_at <= monotonic():
            self._items.pop(key, None)
            return True
        return False

    def get(self, key: str) -> Any:
        if self._is_expired(key):
            return None
        item = self._items.get(key)
        if item is None:
            return None
        value, _ = item
        return value

    def set(self, key: str, value: Any, ttl_seconds: int | float | None = None) -> bool:
        if ttl_seconds is not None and ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive when provided")
        expires_at = monotonic() + ttl_seconds if ttl_seconds is not None else None
        self._items[key] = (value, expires_at)
        return True

    def delete(self, key: str) -> bool:
        return self._items.pop(key, None) is not None

    def exists(self, key: str) -> bool:
        if self._is_expired(key):
            return False
        return key in self._items

    def clear(self) -> None:
        self._items.clear()

