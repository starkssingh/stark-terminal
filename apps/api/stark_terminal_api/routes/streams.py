from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_data_platform.streams.health import check_streams_health

router = APIRouter()


@router.get("/streams/health")
def streams_health() -> dict[str, Any]:
    status = check_streams_health()
    return {
        "service": "stark-terminal-streams",
        **status.model_dump(),
    }
