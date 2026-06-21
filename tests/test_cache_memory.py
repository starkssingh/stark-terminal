from time import sleep

from stark_terminal_data_platform.cache.memory import InMemoryCache


def test_in_memory_cache_set_get_delete_exists() -> None:
    cache = InMemoryCache()

    assert cache.set("key", {"value": 1}) is True
    assert cache.exists("key") is True
    assert cache.get("key") == {"value": 1}
    assert cache.delete("key") is True
    assert cache.exists("key") is False
    assert cache.get("key") is None


def test_in_memory_cache_ttl_expiration() -> None:
    cache = InMemoryCache()

    cache.set("key", "value", ttl_seconds=0.01)
    sleep(0.02)

    assert cache.exists("key") is False
    assert cache.get("key") is None


def test_in_memory_cache_clear_and_instance_isolation() -> None:
    first = InMemoryCache()
    second = InMemoryCache()

    first.set("key", "value")
    assert second.get("key") is None

    first.clear()
    assert first.exists("key") is False

