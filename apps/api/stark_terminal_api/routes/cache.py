from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_data_platform.cache.health import check_cache_health

router = APIRouter()


@router.get("/cache/health")
def cache_health() -> dict[str, Any]:
    status = check_cache_health()
    return {
        "service": "stark-terminal-cache",
        **status.model_dump(),
    }
