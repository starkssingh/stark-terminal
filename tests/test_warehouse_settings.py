from pydantic import ValidationError
import pytest

from stark_terminal_core.config.settings import Settings


def test_warehouse_settings_defaults_are_safe() -> None:
    settings = Settings()

    assert settings.prompt_number == "54"
    assert settings.clickhouse_enabled is False
    assert settings.clickhouse_host == "localhost"
    assert settings.clickhouse_port == 8123
    assert settings.clickhouse_database == "stark_terminal"
    assert settings.clickhouse_use_memory_fallback is True
    assert settings.warehouse_schema_version == "v1"


def test_warehouse_safe_snapshot_excludes_sensitive_values() -> None:
    settings = Settings(
        clickhouse_url="http://user:secret@localhost:8123/stark",
        clickhouse_user="user",
        clickhouse_password="secret",
    )
    snapshot = settings.safe_settings_snapshot()

    assert "clickhouse_url" not in snapshot
    assert "clickhouse_user" not in snapshot
    assert "clickhouse_password" not in snapshot
    assert snapshot["clickhouse_configured"] is True
    assert snapshot["clickhouse_enabled"] is False
    assert snapshot["clickhouse_host"] == "localhost"
    assert snapshot["clickhouse_port"] == 8123
    assert snapshot["clickhouse_database"] == "stark_terminal"
    assert snapshot["clickhouse_use_memory_fallback"] is True
    assert snapshot["warehouse_schema_version"] == "v1"


@pytest.mark.parametrize(
    "field,value",
    [
        ("clickhouse_port", 0),
        ("clickhouse_port", 65536),
        ("clickhouse_connect_timeout_seconds", 0),
        ("clickhouse_send_receive_timeout_seconds", 0),
        ("clickhouse_database", ""),
        ("warehouse_schema_version", ""),
    ],
)
def test_warehouse_setting_validation(field: str, value: int | str) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field: value})
