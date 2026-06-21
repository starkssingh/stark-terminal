from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import JobStatus, WorkerRole
from stark_terminal_data_platform.workers.base import EchoWorker
from stark_terminal_data_platform.workers.harness import InProcessWorkerHarness
from stark_terminal_data_platform.workers.jobs import create_job_envelope
from stark_terminal_data_platform.workers.registry import WorkerRegistry


def registry_with_echo() -> WorkerRegistry:
    registry = WorkerRegistry()
    registry.register(EchoWorker())
    return registry


def test_disabled_harness_returns_safe_skipped_result() -> None:
    job = create_job_envelope(WorkerRole.TEST_WORKER, "echo", {"value": 1}, settings=Settings())
    harness = InProcessWorkerHarness(registry_with_echo(), Settings(workers_enabled=False))

    result = harness.submit(job)

    assert result.status == JobStatus.SKIPPED
    assert "disabled" in (result.error or "").lower()


def test_dry_run_validates_without_executing_worker() -> None:
    job = create_job_envelope(WorkerRole.TEST_WORKER, "echo", {"value": 1}, settings=Settings())
    harness = InProcessWorkerHarness(registry_with_echo(), Settings(workers_enabled=True))

    result = harness.dry_run(job)

    assert result.status == JobStatus.SKIPPED
    assert "dry run" in (result.error or "").lower()


def test_enabled_harness_runs_echo_worker_synchronously() -> None:
    settings = Settings(workers_enabled=True)
    job = create_job_envelope(WorkerRole.TEST_WORKER, "echo", {"value": 1}, settings=settings)
    harness = InProcessWorkerHarness(registry_with_echo(), settings)

    result = harness.submit(job)

    assert result.status == JobStatus.SUCCEEDED
    assert result.output == {"echo": {"value": 1}}


def test_missing_worker_returns_safe_failed_result() -> None:
    settings = Settings(workers_enabled=True)
    job = create_job_envelope(WorkerRole.TEST_WORKER, "echo", {}, settings=settings)
    harness = InProcessWorkerHarness(WorkerRegistry(), settings)

    result = harness.submit(job)

    assert result.status == JobStatus.FAILED
    assert "No worker" in (result.error or "")


def test_submit_many_preserves_order() -> None:
    settings = Settings(workers_enabled=True)
    jobs = [
        create_job_envelope(WorkerRole.TEST_WORKER, "echo", {"value": 1}, settings=settings),
        create_job_envelope(WorkerRole.TEST_WORKER, "echo", {"value": 2}, settings=settings),
    ]
    harness = InProcessWorkerHarness(registry_with_echo(), settings)

    results = harness.submit_many(jobs)

    assert [result.output["echo"]["value"] for result in results] == [1, 2]

