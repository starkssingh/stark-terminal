from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str | bool]:
    settings = get_settings()
    return {
        "status": "ok",
        "service": "stark-terminal-api",
        "version": settings.app_version,
        "prompt": settings.prompt_number,
        "architecture": "institutional-grade-foundation",
        "execution_apis_enabled": settings.execution_apis_enabled,
        "audit_status": "provider-adapter-milestone",
    }
