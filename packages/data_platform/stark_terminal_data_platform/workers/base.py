from __future__ import annotations

from datetime import datetime, timezone

from stark_terminal_core.domain.enums import WorkerRole
from stark_terminal_data_platform.workers.jobs import JobEnvelope
from stark_terminal_data_platform.workers.results import WorkerResult
from stark_terminal_data_platform.workers.roles import is_execution_forbidden_role


class WorkerError(RuntimeError):
    """Base worker error."""


class ForbiddenWorkerJobError(WorkerError):
    """Raised when a job attempts forbidden execution/broker/order behavior."""


class BaseWorker:
    role: WorkerRole = WorkerRole.UNKNOWN

    def __init__(self, name: str | None = None) -> None:
        role_value = self.role.value if isinstance(self.role, WorkerRole) else str(self.role)
        self._name = name or role_value.lower()

    @property
    def name(self) -> str:
        return self._name

    def can_handle(self, job: JobEnvelope) -> bool:
        return job.worker_role == self.role

    def validate_job(self, job: JobEnvelope) -> None:
        if is_execution_forbidden_role(job.worker_role) or is_execution_forbidden_role(job.job_type):
            raise ForbiddenWorkerJobError("execution, broker, order, or live-trading jobs are forbidden")
        if not self.can_handle(job):
            raise WorkerError(f"worker {self.name} cannot handle role {job.worker_role.value}")

    def handle(self, job: JobEnvelope) -> WorkerResult:
        raise NotImplementedError

    def run(self, job: JobEnvelope) -> WorkerResult:
        started_at = datetime.now(timezone.utc)
        try:
            self.validate_job(job)
            result = self.handle(job)
            if result.started_at is None:
                result.started_at = started_at
            if result.finished_at is None:
                result.finished_at = datetime.now(timezone.utc)
            return result
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:
            return WorkerResult.failed(
                job_id=job.job_id,
                worker_role=job.worker_role,
                error=exc,
                started_at=started_at,
                finished_at=datetime.now(timezone.utc),
            )


class NoOpWorker(BaseWorker):
    role = WorkerRole.TEST_WORKER

    def handle(self, job: JobEnvelope) -> WorkerResult:
        return WorkerResult.skipped(
            job_id=job.job_id,
            worker_role=self.role,
            reason="NoOpWorker skipped job",
        )


class EchoWorker(BaseWorker):
    role = WorkerRole.TEST_WORKER

    def handle(self, job: JobEnvelope) -> WorkerResult:
        return WorkerResult.succeeded(
            job_id=job.job_id,
            worker_role=self.role,
            output={"echo": job.payload},
            audit_id=job.audit_id,
        )


class FailingWorker(BaseWorker):
    role = WorkerRole.TEST_WORKER

    def handle(self, job: JobEnvelope) -> WorkerResult:
        raise WorkerError("Intentional test worker failure")
