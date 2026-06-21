from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.domain.enums import WorkerStatus
from stark_terminal_data_platform.workers.registry import WorkerRegistry


class WorkerSystemHealthStatus(BaseModel):
    enabled: bool
    harness_mode: str
    registered_workers: int
    available_roles: list[str]
    background_threads_allowed: bool
    infinite_loops_allowed: bool
    status: str
    error: str | None = None


def check_worker_system_health(
    settings: Settings | None = None,
    registry: WorkerRegistry | None = None,
) -> WorkerSystemHealthStatus:
    resolved_settings = settings or get_settings()
    resolved_registry = registry or WorkerRegistry()
    available_roles = [role.value for role in resolved_registry.list_roles()]

    status = WorkerStatus.HEALTHY.value
    error: str | None = None
    if not resolved_settings.workers_enabled:
        status = WorkerStatus.DISABLED.value
    if resolved_settings.worker_allow_background_threads or resolved_settings.worker_allow_infinite_loops:
        status = WorkerStatus.UNHEALTHY.value
        error = "UnsafeWorkerRuntimeConfiguration"

    return WorkerSystemHealthStatus(
        enabled=resolved_settings.workers_enabled,
        harness_mode=resolved_settings.worker_harness_mode,
        registered_workers=len(available_roles),
        available_roles=available_roles,
        background_threads_allowed=resolved_settings.worker_allow_background_threads,
        infinite_loops_allowed=resolved_settings.worker_allow_infinite_loops,
        status=status,
        error=error,
    )

