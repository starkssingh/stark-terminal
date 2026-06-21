from stark_terminal_core.config.settings import Settings
from stark_terminal_data_platform.warehouse.health import check_warehouse_health


def test_default_warehouse_health_uses_memory_fallback() -> None:
    status = check_warehouse_health(Settings())

    assert status.configured is False
    assert status.enabled is False
    assert status.reachable is True
    assert status.backend == "memory"
    assert status.memory_fallback_enabled is True
    assert status.clickhouse_url_present is False
    assert status.database == "stark_terminal"
    assert status.schema_version == "v1"
    assert status.table_contract_count == 6


def test_disabled_fallback_health_reports_none_backend() -> None:
    status = check_warehouse_health(Settings(clickhouse_use_memory_fallback=False))

    assert status.reachable is False
    assert status.backend == "none"


def test_invalid_enabled_clickhouse_config_returns_unreachable() -> None:
    status = check_warehouse_health(Settings(clickhouse_enabled=True, clickhouse_url="ftp://secret"))

    assert status.enabled is True
    assert status.reachable is False
    assert status.backend == "clickhouse"
    assert status.error == "WarehouseUnavailableError"
    assert "secret" not in status.model_dump_json().lower()
