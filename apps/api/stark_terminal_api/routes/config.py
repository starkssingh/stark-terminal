from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings

router = APIRouter()


@router.get("/config")
def config_snapshot() -> dict[str, Any]:
    return get_settings().safe_settings_snapshot()
