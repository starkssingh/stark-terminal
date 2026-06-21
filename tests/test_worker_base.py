import pytest

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import JobStatus, WorkerRole
from stark_terminal_data_platform.workers.base import BaseWorker, EchoWorker, FailingWorker, NoOpWorker
from stark_terminal_data_platform.workers.jobs import create_job_envelope


def test_noop_worker_can_handle_and_run_job() -> None:
    job = create_job_envelope(WorkerRole.TEST_WORKER, "noop", {}, settings=Settings())

    result = NoOpWorker().run(job)

    assert result.status == JobStatus.SKIPPED
    assert NoOpWorker().can_handle(job) is True


def test_echo_worker_returns_payload() -> None:
    job = create_job_envelope(WorkerRole.TEST_WORKER, "echo", {"value": 1}, settings=Settings())

    result = EchoWorker().run(job)

    assert result.status == JobStatus.SUCCEEDED
    assert result.output == {"echo": {"value": 1}}


def test_failing_worker_returns_failed_result() -> None:
    job = create_job_envelope(WorkerRole.TEST_WORKER, "fail", {}, settings=Settings())

    result = FailingWorker().run(job)

    assert result.status == JobStatus.FAILED
    assert result.error == "WorkerError"


def test_forbidden_jobs_are_rejected_before_handle() -> None:
    job = create_job_envelope(WorkerRole.TEST_WORKER, "echo", {}, settings=Settings())
    job.job_type = "broker_execution"

    result = EchoWorker().run(job)

    assert result.status == JobStatus.FAILED


def test_keyboard_interrupt_is_not_swallowed() -> None:
    class InterruptWorker(BaseWorker):
        role = WorkerRole.TEST_WORKER

        def handle(self, job):
            raise KeyboardInterrupt

    job = create_job_envelope(WorkerRole.TEST_WORKER, "interrupt", {}, settings=Settings())

    with pytest.raises(KeyboardInterrupt):
        InterruptWorker().run(job)

