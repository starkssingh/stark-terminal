import pytest

from stark_terminal_core.domain.enums import WorkerRole
from stark_terminal_data_platform.workers.base import EchoWorker
from stark_terminal_data_platform.workers.registry import WorkerRegistry, WorkerRegistryError


def test_worker_registry_register_get_list_unregister_clear() -> None:
    registry = WorkerRegistry()
    worker = EchoWorker()

    registry.register(worker)

    assert registry.has(WorkerRole.TEST_WORKER) is True
    assert registry.get(WorkerRole.TEST_WORKER) is worker
    assert registry.list_roles() == [WorkerRole.TEST_WORKER]
    assert registry.list_workers() == [worker]

    registry.unregister(WorkerRole.TEST_WORKER)
    assert registry.has(WorkerRole.TEST_WORKER) is False

    registry.register(worker)
    registry.clear()
    assert registry.list_workers() == []


def test_worker_registry_duplicate_role_requires_replace() -> None:
    registry = WorkerRegistry()
    first = EchoWorker("first")
    second = EchoWorker("second")

    registry.register(first)
    with pytest.raises(WorkerRegistryError):
        registry.register(second)

    registry.register(second, replace=True)
    assert registry.get(WorkerRole.TEST_WORKER) is second


def test_worker_registry_rejects_forbidden_execution_role() -> None:
    class ExecutionWorker(EchoWorker):
        role = "execution_worker"

    with pytest.raises(ValueError):
        WorkerRegistry().register(ExecutionWorker())

