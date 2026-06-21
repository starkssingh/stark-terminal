from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_data_platform.warehouse.client import (
    ClickHouseWarehouseClient,
    WarehouseUnavailableError,
)
from stark_terminal_data_platform.warehouse.tables import list_default_warehouse_table_contracts


class WarehouseHealthStatus(BaseModel):
    configured: bool
    enabled: bool
    reachable: bool
    backend: str
    memory_fallback_enabled: bool
    clickhouse_url_present: bool
    database: str
    schema_version: str
    table_contract_count: int
    error: str | None = None


def check_warehouse_health(settings: Settings | None = None) -> WarehouseHealthStatus:
    resolved_settings = settings or get_settings()
    table_count = len(list_default_warehouse_table_contracts())

    if not resolved_settings.clickhouse_enabled:
        backend = "memory" if resolved_settings.clickhouse_use_memory_fallback else "none"
        return WarehouseHealthStatus(
            configured=bool(resolved_settings.clickhouse_url),
            enabled=False,
            reachable=resolved_settings.clickhouse_use_memory_fallback,
            backend=backend,
            memory_fallback_enabled=resolved_settings.clickhouse_use_memory_fallback,
            clickhouse_url_present=bool(resolved_settings.clickhouse_url),
            database=resolved_settings.clickhouse_database,
            schema_version=resolved_settings.warehouse_schema_version,
            table_contract_count=table_count,
        )

    try:
        client = ClickHouseWarehouseClient(resolved_settings)
        reachable = client.ping()
        client.close()
        return WarehouseHealthStatus(
            configured=True,
            enabled=True,
            reachable=reachable,
            backend="clickhouse",
            memory_fallback_enabled=resolved_settings.clickhouse_use_memory_fallback,
            clickhouse_url_present=bool(resolved_settings.clickhouse_url),
            database=resolved_settings.clickhouse_database,
            schema_version=resolved_settings.warehouse_schema_version,
            table_contract_count=table_count,
        )
    except WarehouseUnavailableError as exc:
        return WarehouseHealthStatus(
            configured=bool(resolved_settings.clickhouse_url) or bool(resolved_settings.clickhouse_host),
            enabled=True,
            reachable=False,
            backend="clickhouse",
            memory_fallback_enabled=resolved_settings.clickhouse_use_memory_fallback,
            clickhouse_url_present=bool(resolved_settings.clickhouse_url),
            database=resolved_settings.clickhouse_database,
            schema_version=resolved_settings.warehouse_schema_version,
            table_contract_count=table_count,
            error=exc.__class__.__name__,
        )

