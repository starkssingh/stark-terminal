from pydantic import ValidationError
import pytest

from stark_terminal_core.config.settings import Settings


def test_timescale_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.timescale_database_url is None
    assert settings.timescale_enabled is False
    assert settings.timescale_extension_name == "timescaledb"
    assert settings.timescale_create_extension is False
    assert settings.timescale_create_hypertables is False
    assert settings.timescale_chunk_interval == "7 days"


def test_timescale_url_is_not_exposed_in_safe_snapshot() -> None:
    settings = Settings(
        timescale_database_url="postgresql+psycopg://user:secret@localhost/stark_timeseries"
    )

    snapshot = settings.safe_settings_snapshot()

    assert "timescale_database_url" not in snapshot
    assert snapshot["timescale_configured"] is True
    assert snapshot["timescale_enabled"] is False
    assert snapshot["timescale_create_extension"] is False
    assert snapshot["timescale_create_hypertables"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("timescale_extension_name", ""),
        ("timescale_chunk_interval", " "),
    ],
)
def test_timescale_text_validation_rejects_empty_values(field: str, value: str) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field: value})
