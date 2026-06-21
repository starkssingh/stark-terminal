from typing import Any

from fastapi import APIRouter

from stark_terminal_data_platform.db.health import check_database_health
from stark_terminal_core.serialization.json import to_jsonable

router = APIRouter()


@router.get("/database/health")
def database_health() -> dict[str, Any]:
    status = check_database_health()
    payload = to_jsonable(status)
    return {
        "service": "stark-terminal-database",
        **payload,
    }
