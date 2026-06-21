import pytest

from stark_terminal_core.config.settings import Settings
from stark_terminal_data_platform.warehouse.client import (
    ClickHouseWarehouseClient,
    WarehouseUnavailableError,
)


def test_default_client_uses_memory_fallback() -> None:
    client = ClickHouseWarehouseClient(Settings())

    assert client.backend == "memory"
    assert client.ping() is True
    client.execute("SELECT 1")
    assert client.recorder is not None
    assert client.recorder.count() == 1


def test_query_records_in_memory_fallback() -> None:
    client = ClickHouseWarehouseClient(Settings())

    result = client.query("SELECT * FROM table WHERE symbol = {symbol:String}", {"symbol": "RELIANCE"})

    assert result == []
    assert client.recorder is not None
    assert client.recorder.last_query()["parameters"] == {"symbol": "RELIANCE"}


def test_fallback_disabled_without_clickhouse_fails_safely() -> None:
    client = ClickHouseWarehouseClient(Settings(clickhouse_use_memory_fallback=False))

    with pytest.raises(WarehouseUnavailableError) as exc_info:
        client.ping()

    assert "secret" not in str(exc_info.value).lower()


def test_invalid_enabled_clickhouse_url_is_sanitized() -> None:
    client = ClickHouseWarehouseClient(
        Settings(clickhouse_enabled=True, clickhouse_url="ftp://user:secret@localhost")
    )

    with pytest.raises(WarehouseUnavailableError) as exc_info:
        client.ping()

    assert "secret" not in str(exc_info.value).lower()
