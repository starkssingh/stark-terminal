from stark_terminal_core.config.settings import Settings
from stark_terminal_core.serialization.json import to_jsonable
from stark_terminal_data_platform.timeseries.health import check_timescale_health
from stark_terminal_data_platform.timeseries.hypertables import (
    create_hypertable_sql,
    create_timescaledb_extension_sql,
    validate_hypertable_target,
)
import pytest


def test_hypertable_sql_helpers_return_planning_sql() -> None:
    extension_sql = create_timescaledb_extension_sql()
    hypertable_sql = create_hypertable_sql("ohlcv_bars")

    assert "CREATE EXTENSION IF NOT EXISTS" in extension_sql
    assert "create_hypertable" in hypertable_sql
    assert "if_not_exists => TRUE" in hypertable_sql


@pytest.mark.parametrize(
    ("table_name", "time_column"),
    [
        ("ohlcv-bars", "timestamp"),
        ("ohlcv_bars", "timestamp;drop"),
    ],
)
def test_invalid_hypertable_target_rejected(table_name: str, time_column: str) -> None:
    with pytest.raises(ValueError):
        validate_hypertable_target(table_name, time_column)


def test_timescale_health_disabled_by_default_is_safe() -> None:
    status = check_timescale_health(Settings())

    assert status.configured is False
    assert status.enabled is False
    assert status.reachable is False
    assert status.extension_available is None


def test_timescale_health_invalid_enabled_url_returns_unreachable() -> None:
    status = check_timescale_health(
        Settings(timescale_enabled=True, timescale_database_url="not-a-valid-url")
    )

    assert status.configured is True
    assert status.enabled is True
    assert status.reachable is False
    assert "not-a-valid-url" not in (status.error or "")


def test_timescale_health_snapshot_does_not_expose_raw_url() -> None:
    status = check_timescale_health(
        Settings(
            timescale_enabled=True,
            timescale_database_url="postgresql+psycopg://user:secret@localhost/stark",
        )
    )

    payload = to_jsonable(status)

    assert "timescale_database_url" not in payload
    assert "secret" not in str(payload)
