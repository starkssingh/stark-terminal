from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.serialization.json import to_jsonable
from stark_terminal_data_platform.warehouse.health import check_warehouse_health
from stark_terminal_data_platform.warehouse.tables import list_default_warehouse_table_contracts

router = APIRouter()


@router.get("/warehouse/health")
def warehouse_health() -> dict[str, Any]:
    status = check_warehouse_health()
    return {
        "service": "stark-terminal-warehouse",
        **status.model_dump(),
    }


@router.get("/warehouse/contracts")
def warehouse_contracts() -> dict[str, Any]:
    settings = get_settings()
    contracts = list_default_warehouse_table_contracts()
    return {
        "service": "stark-terminal-warehouse",
        "schema_version": settings.warehouse_schema_version,
        "contracts": to_jsonable(contracts),
        "count": len(contracts),
    }
