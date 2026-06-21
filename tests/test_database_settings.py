from pydantic import ValidationError
import pytest

from stark_terminal_core.config.settings import Settings


def test_database_settings_defaults_are_valid() -> None:
    settings = Settings()

    assert settings.database_url is None
    assert settings.database_echo is False
    assert settings.database_pool_size == 5
    assert settings.database_max_overflow == 10
    assert settings.database_pool_pre_ping is True
    assert settings.database_connect_timeout_seconds == 10


def test_database_url_is_not_exposed_in_safe_snapshot() -> None:
    settings = Settings(database_url="postgresql+psycopg://user:secret@localhost/stark")

    snapshot = settings.safe_settings_snapshot()

    assert "database_url" not in snapshot
    assert snapshot["database_configured"] is True


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("database_pool_size", 0),
        ("database_max_overflow", -1),
        ("database_connect_timeout_seconds", 0),
    ],
)
def test_database_pool_validation_rejects_invalid_values(field: str, value: int) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field: value})
