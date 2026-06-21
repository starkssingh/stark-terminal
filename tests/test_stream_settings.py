from pydantic import ValidationError
import pytest

from stark_terminal_core.config.settings import Settings


def test_stream_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.redis_streams_enabled is False
    assert settings.redis_streams_use_memory_fallback is True
    assert settings.stream_key_prefix == "stark"
    assert settings.stream_environment_namespace == "development"
    assert settings.stream_consumer_group == "stark-terminal"
    assert settings.stream_read_count == 10
    assert settings.stream_block_ms == 1000
    assert settings.stream_max_len == 10000
    assert settings.stream_approximate_trim is True
    assert settings.event_schema_version == "v1"


def test_stream_safe_snapshot_exposes_no_redis_url() -> None:
    settings = Settings(redis_url="redis://:secret@localhost:6379/0")

    snapshot = settings.safe_settings_snapshot()

    assert "redis_url" not in snapshot
    assert snapshot["redis_configured"] is True
    assert snapshot["redis_streams_enabled"] is False
    assert snapshot["redis_streams_use_memory_fallback"] is True


@pytest.mark.parametrize(
    "field,value",
    [
        ("stream_read_count", 0),
        ("stream_block_ms", -1),
        ("stream_max_len", 0),
    ],
)
def test_stream_numeric_validation(field: str, value: int) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field: value})


@pytest.mark.parametrize(
    "field,value",
    [
        ("stream_key_prefix", ""),
        ("stream_environment_namespace", ""),
        ("stream_consumer_group", ""),
        ("event_schema_version", ""),
        ("stream_key_prefix", "../stark"),
        ("stream_environment_namespace", "bad namespace"),
    ],
)
def test_stream_text_validation(field: str, value: str) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field: value})

