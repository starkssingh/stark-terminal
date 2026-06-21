from stark_terminal_core.config.settings import Settings
from stark_terminal_data_platform.cache.health import check_cache_health


def test_cache_health_default_memory_fallback_is_reachable() -> None:
    status = check_cache_health(Settings())

    assert status.configured is False
    assert status.enabled is False
    assert status.reachable is True
    assert status.backend == "memory"
    assert status.memory_fallback_enabled is True


def test_cache_health_disabled_fallback_reports_none_backend() -> None:
    status = check_cache_health(Settings(cache_use_memory_fallback=False))

    assert status.reachable is False
    assert status.backend == "none"
    assert status.error == "CacheBackendDisabled"


def test_cache_health_invalid_redis_url_returns_unreachable() -> None:
    status = check_cache_health(
        Settings(
            redis_enabled=True,
            redis_url="redis://:secret@127.0.0.1:1/0",
            cache_use_memory_fallback=False,
        )
    )

    assert status.configured is True
    assert status.enabled is True
    assert status.reachable is False
    assert status.backend == "redis"
    assert status.error is not None
    assert "secret" not in status.model_dump_json()
    assert "redis://" not in status.model_dump_json()

