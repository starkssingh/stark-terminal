from typing import Any

from fastapi import APIRouter

from stark_terminal_core.serialization.json import to_jsonable
from stark_terminal_data_platform.timeseries.health import check_timescale_health

router = APIRouter()


@router.get("/timeseries/health")
def timeseries_health() -> dict[str, Any]:
    status = check_timescale_health()
    payload = to_jsonable(status)
    return {
        "service": "stark-terminal-timeseries",
        **payload,
    }
