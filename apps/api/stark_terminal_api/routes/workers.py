from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_data_platform.workers.health import check_worker_system_health

router = APIRouter()


@router.get("/workers/health")
def workers_health() -> dict[str, Any]:
    status = check_worker_system_health()
    return {
        "service": "stark-terminal-workers",
        **status.model_dump(),
    }
