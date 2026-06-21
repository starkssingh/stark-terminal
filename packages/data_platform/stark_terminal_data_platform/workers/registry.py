from __future__ import annotations

from stark_terminal_core.domain.enums import WorkerRole
from stark_terminal_data_platform.workers.base import BaseWorker
from stark_terminal_data_platform.workers.roles import is_execution_forbidden_role


class WorkerRegistryError(ValueError):
    """Raised when worker registry operations are invalid."""


class WorkerRegistry:
    def __init__(self) -> None:
        self._workers: dict[WorkerRole, BaseWorker] = {}

    def register(self, worker: BaseWorker, replace: bool = False) -> None:
        role = WorkerRole(worker.role)
        if is_execution_forbidden_role(role):
            raise WorkerRegistryError("execution, broker, order, or live-trading workers are forbidden")
        if role in self._workers and not replace:
            raise WorkerRegistryError(f"worker role already registered: {role.value}")
        self._workers[role] = worker

    def unregister(self, role: WorkerRole) -> None:
        self._workers.pop(WorkerRole(role), None)

    def get(self, role: WorkerRole) -> BaseWorker | None:
        return self._workers.get(WorkerRole(role))

    def list_roles(self) -> list[WorkerRole]:
        return list(self._workers)

    def list_workers(self) -> list[BaseWorker]:
        return list(self._workers.values())

    def has(self, role: WorkerRole) -> bool:
        return WorkerRole(role) in self._workers

    def clear(self) -> None:
        self._workers.clear()

