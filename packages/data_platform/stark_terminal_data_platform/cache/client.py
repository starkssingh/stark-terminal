from __future__ import annotations

from typing import Any

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_data_platform.cache.memory import InMemoryCache
from stark_terminal_data_platform.cache.serialization import cache_dumps, cache_loads


class CacheError(RuntimeError):
    """Base cache error."""


class CacheUnavailableError(CacheError):
    """Raised when no cache backend is available for a required operation."""


class CacheClient:
    def __init__(
        self,
        settings: Settings | None = None,
        memory_backend: InMemoryCache | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self._memory_backend = memory_backend
        self._redis_client: Any | None = None

    @property
    def backend(self) -> str:
        if self.settings.redis_enabled and self.settings.redis_url:
            return "redis"
        if self.settings.cache_use_memory_fallback:
            return "memory"
        return "none"

    @property
    def memory_backend(self) -> InMemoryCache | None:
        if self.backend != "memory":
            return None
        if self._memory_backend is None:
            self._memory_backend = InMemoryCache()
        return self._memory_backend

    @property
    def redis_client(self) -> Any:
        if self.backend != "redis":
            raise CacheUnavailableError("Redis cache backend is not configured")
        if self._redis_client is None:
            try:
                import redis

                self._redis_client = redis.Redis.from_url(
                    self.settings.redis_url or "",
                    socket_timeout=self.settings.redis_socket_timeout_seconds,
                    socket_connect_timeout=self.settings.redis_connect_timeout_seconds,
                    health_check_interval=self.settings.redis_health_check_interval_seconds,
                    decode_responses=False,
                )
            except Exception as exc:
                raise CacheUnavailableError(
                    f"Redis cache backend unavailable: {exc.__class__.__name__}"
                ) from exc
        return self._redis_client

    def _default_ttl(self, ttl_seconds: int | float | None) -> int | float:
        return self.settings.cache_default_ttl_seconds if ttl_seconds is None else ttl_seconds

    def get(self, key: str) -> Any:
        if self.backend == "memory":
            backend = self.memory_backend
            return cache_loads(backend.get(key) if backend is not None else None)
        if self.backend == "redis":
            try:
                return cache_loads(self.redis_client.get(key))
            except Exception as exc:
                raise CacheUnavailableError(
                    f"cache get failed: {exc.__class__.__name__}"
                ) from exc
        return None

    def set(self, key: str, value: Any, ttl_seconds: int | float | None = None) -> bool:
        payload = cache_dumps(value)
        ttl = self._default_ttl(ttl_seconds)
        if ttl <= 0:
            raise ValueError("ttl_seconds must be positive")

        if self.backend == "memory":
            backend = self.memory_backend
            assert backend is not None
            return backend.set(key, payload, ttl_seconds=ttl)
        if self.backend == "redis":
            try:
                return bool(self.redis_client.set(key, payload, ex=ttl))
            except Exception as exc:
                raise CacheUnavailableError(
                    f"cache set failed: {exc.__class__.__name__}"
                ) from exc
        raise CacheUnavailableError("Cache backend unavailable")

    def delete(self, key: str) -> bool:
        if self.backend == "memory":
            backend = self.memory_backend
            return bool(backend.delete(key) if backend is not None else False)
        if self.backend == "redis":
            try:
                return bool(self.redis_client.delete(key))
            except Exception as exc:
                raise CacheUnavailableError(
                    f"cache delete failed: {exc.__class__.__name__}"
                ) from exc
        return False

    def exists(self, key: str) -> bool:
        if self.backend == "memory":
            backend = self.memory_backend
            return bool(backend.exists(key) if backend is not None else False)
        if self.backend == "redis":
            try:
                return bool(self.redis_client.exists(key))
            except Exception as exc:
                raise CacheUnavailableError(
                    f"cache exists failed: {exc.__class__.__name__}"
                ) from exc
        return False

    def ping(self) -> bool:
        if self.backend == "memory":
            return True
        if self.backend == "redis":
            try:
                return bool(self.redis_client.ping())
            except Exception:
                return False
        return False

    def close(self) -> None:
        if self._redis_client is not None:
            try:
                self._redis_client.close()
            finally:
                self._redis_client = None

    def __enter__(self) -> CacheClient:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()

