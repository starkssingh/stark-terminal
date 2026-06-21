from pydantic import ValidationError
import pytest

from stark_terminal_core.config.settings import Settings


def test_worker_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.workers_enabled is False
    assert settings.worker_harness_mode == "in_process"
    assert settings.worker_default_timeout_seconds == 30
    assert settings.worker_max_retries == 0
    assert settings.worker_default_queue == "default"
    assert settings.worker_schema_version == "v1"
    assert settings.worker_allow_background_threads is False
    assert settings.worker_allow_infinite_loops is False


def test_worker_safe_snapshot_includes_worker_fields() -> None:
    snapshot = Settings().safe_settings_snapshot()

    assert snapshot["workers_enabled"] is False
    assert snapshot["worker_harness_mode"] == "in_process"
    assert snapshot["worker_default_timeout_seconds"] == 30
    assert snapshot["worker_max_retries"] == 0
    assert snapshot["worker_default_queue"] == "default"
    assert snapshot["worker_schema_version"] == "v1"
    assert snapshot["worker_allow_background_threads"] is False
    assert snapshot["worker_allow_infinite_loops"] is False


@pytest.mark.parametrize(
    "field,value",
    [
        ("worker_default_timeout_seconds", 0),
        ("worker_max_retries", -1),
    ],
)
def test_worker_numeric_validation(field: str, value: int) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field: value})


@pytest.mark.parametrize(
    "field,value",
    [
        ("worker_default_queue", ""),
        ("worker_schema_version", ""),
        ("worker_harness_mode", "threaded"),
    ],
)
def test_worker_text_validation(field: str, value: str) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field: value})

