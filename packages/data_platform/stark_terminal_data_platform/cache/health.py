from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_data_platform.cache.client import CacheClient


class CacheHealthStatus(BaseModel):
    configured: bool
    enabled: bool
    reachable: bool
    backend: str
    memory_fallback_enabled: bool
    redis_url_present: bool
    error: str | None = None


def check_cache_health(settings: Settings | None = None) -> CacheHealthStatus:
    resolved_settings = settings or get_settings()
    configured = bool(resolved_settings.redis_url)
    enabled = resolved_settings.redis_enabled

    if enabled and configured:
        client = CacheClient(resolved_settings)
        try:
            reachable = client.ping()
            return CacheHealthStatus(
                configured=configured,
                enabled=enabled,
                reachable=reachable,
                backend="redis",
                memory_fallback_enabled=resolved_settings.cache_use_memory_fallback,
                redis_url_present=configured,
                error=None if reachable else "RedisPingFailed",
            )
        except Exception as exc:
            return CacheHealthStatus(
                configured=configured,
                enabled=enabled,
                reachable=False,
                backend="redis",
                memory_fallback_enabled=resolved_settings.cache_use_memory_fallback,
                redis_url_present=configured,
                error=exc.__class__.__name__,
            )
        finally:
            client.close()

    if resolved_settings.cache_use_memory_fallback:
        return CacheHealthStatus(
            configured=configured,
            enabled=enabled,
            reachable=True,
            backend="memory",
            memory_fallback_enabled=True,
            redis_url_present=configured,
        )

    return CacheHealthStatus(
        configured=configured,
        enabled=enabled,
        reachable=False,
        backend="none",
        memory_fallback_enabled=False,
        redis_url_present=configured,
        error="CacheBackendDisabled",
    )

