from typing import Any

from fastapi import APIRouter

from stark_terminal_core.serialization.json import to_jsonable
from stark_terminal_data_platform.lake.health import check_research_lake_health

router = APIRouter()


@router.get("/research-lake/health")
def research_lake_health() -> dict[str, Any]:
    status = check_research_lake_health()
    payload = to_jsonable(status)
    return {
        "service": "stark-terminal-research-lake",
        **payload,
    }
