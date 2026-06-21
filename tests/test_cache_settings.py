from pydantic import ValidationError
import pytest

from stark_terminal_core.config.settings import Settings


def test_cache_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.redis_enabled is False
    assert settings.cache_use_memory_fallback is True
    assert settings.cache_default_ttl_seconds == 300
    assert settings.cache_key_prefix == "stark"
    assert settings.cache_environment_namespace == "development"


def test_redis_url_is_not_exposed_in_safe_snapshot() -> None:
    settings = Settings(redis_url="redis://:secret@localhost:6379/0")

    snapshot = settings.safe_settings_snapshot()

    assert "redis_url" not in snapshot
    assert snapshot["redis_configured"] is True
    assert snapshot["redis_enabled"] is False


@pytest.mark.parametrize(
    "field,value",
    [
        ("redis_socket_timeout_seconds", 0),
        ("redis_connect_timeout_seconds", 0),
        ("redis_health_check_interval_seconds", 0),
        ("cache_default_ttl_seconds", 0),
    ],
)
def test_cache_numeric_validation_rejects_invalid_values(field: str, value: int) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field: value})


@pytest.mark.parametrize(
    "field,value",
    [
        ("cache_key_prefix", ""),
        ("cache_environment_namespace", ""),
        ("cache_key_prefix", "not safe"),
        ("cache_environment_namespace", "../prod"),
    ],
)
def test_cache_prefix_and_namespace_validation(field: str, value: str) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field: value})

