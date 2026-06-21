from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import WorkerStatus
from stark_terminal_data_platform.workers.base import EchoWorker
from stark_terminal_data_platform.workers.health import check_worker_system_health
from stark_terminal_data_platform.workers.registry import WorkerRegistry


def test_worker_health_default_does_not_crash() -> None:
    status = check_worker_system_health(Settings())

    assert status.enabled is False
    assert status.harness_mode == "in_process"
    assert status.registered_workers == 0
    assert status.available_roles == []
    assert status.status == WorkerStatus.DISABLED.value


def test_worker_health_with_registry_reports_roles() -> None:
    registry = WorkerRegistry()
    registry.register(EchoWorker())

    status = check_worker_system_health(Settings(workers_enabled=True), registry)

    assert status.enabled is True
    assert status.registered_workers == 1
    assert status.available_roles == ["TEST_WORKER"]
    assert status.status == WorkerStatus.HEALTHY.value


def test_worker_health_reflects_unsafe_runtime_settings() -> None:
    status = check_worker_system_health(
        Settings(worker_allow_background_threads=True, worker_allow_infinite_loops=True)
    )

    assert status.status == WorkerStatus.UNHEALTHY.value
    assert status.error == "UnsafeWorkerRuntimeConfiguration"
    assert "secret" not in status.model_dump_json()

