import pytest

from stark_terminal_core.config.settings import Settings
from stark_terminal_data_platform.cache.client import CacheClient, CacheUnavailableError


def test_cache_client_uses_memory_fallback_by_default() -> None:
    client = CacheClient(Settings())

    assert client.backend == "memory"
    assert client.ping() is True


def test_cache_client_set_get_delete_exists_with_memory_backend() -> None:
    client = CacheClient(Settings(cache_default_ttl_seconds=30))

    assert client.set("stark:development:health:api", {"ok": True}) is True
    assert client.exists("stark:development:health:api") is True
    assert client.get("stark:development:health:api") == {"ok": True}
    assert client.delete("stark:development:health:api") is True
    assert client.get("stark:development:health:api") is None


def test_cache_client_fallback_disabled_without_redis_is_safe() -> None:
    client = CacheClient(Settings(cache_use_memory_fallback=False))

    assert client.backend == "none"
    assert client.get("key") is None
    assert client.exists("key") is False
    assert client.delete("key") is False
    assert client.ping() is False
    with pytest.raises(CacheUnavailableError, match="Cache backend unavailable"):
        client.set("key", "value")


def test_cache_client_errors_do_not_include_raw_redis_url() -> None:
    settings = Settings(
        redis_enabled=True,
        redis_url="redis://:secret@127.0.0.1:1/0",
        cache_use_memory_fallback=False,
    )
    client = CacheClient(settings)

    with pytest.raises(CacheUnavailableError) as exc_info:
        client.set("key", "value", ttl_seconds=1)

    assert "secret" not in str(exc_info.value)
    assert "redis://" not in str(exc_info.value)

