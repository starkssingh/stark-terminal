from stark_terminal_core.config.settings import Settings
from stark_terminal_data_platform.db.health import check_database_health


def test_database_health_uses_sqlite_fallback_without_configured_database_url() -> None:
    status = check_database_health(Settings())

    assert status.configured is False
    assert status.database_url_present is False
    assert status.reachable is True
    assert status.dialect == "sqlite"
    assert status.error is None


def test_database_health_returns_unreachable_for_invalid_url_without_raising() -> None:
    status = check_database_health(Settings(database_url="not-a-valid-sqlalchemy-url"))

    assert status.configured is True
    assert status.database_url_present is True
    assert status.reachable is False
    assert "not-a-valid" not in (status.error or "")
