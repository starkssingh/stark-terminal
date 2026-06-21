from __future__ import annotations

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.domain.enums import JobStatus
from stark_terminal_data_platform.workers.jobs import JobEnvelope
from stark_terminal_data_platform.workers.registry import WorkerRegistry
from stark_terminal_data_platform.workers.results import WorkerResult
from stark_terminal_data_platform.workers.roles import is_execution_forbidden_role


class InProcessWorkerHarness:
    def __init__(
        self,
        registry: WorkerRegistry | None = None,
        settings: Settings | None = None,
    ) -> None:
        self.registry = registry or WorkerRegistry()
        self.settings = settings or get_settings()

    @property
    def enabled(self) -> bool:
        return self.settings.workers_enabled and self.settings.worker_harness_mode == "in_process"

    def dry_run(self, job: JobEnvelope) -> WorkerResult:
        if is_execution_forbidden_role(job.worker_role) or is_execution_forbidden_role(job.job_type):
            return WorkerResult.failed(job.job_id, job.worker_role, "Forbidden worker job")
        if not self.registry.has(job.worker_role):
            return WorkerResult.skipped(job.job_id, job.worker_role, "No worker registered for role")
        return WorkerResult.skipped(job.job_id, job.worker_role, "Dry run only")

    def submit(self, job: JobEnvelope) -> WorkerResult:
        if is_execution_forbidden_role(job.worker_role) or is_execution_forbidden_role(job.job_type):
            return WorkerResult.failed(job.job_id, job.worker_role, "Forbidden worker job")
        if not self.enabled:
            return WorkerResult.skipped(job.job_id, job.worker_role, "Worker harness disabled")
        worker = self.registry.get(job.worker_role)
        if worker is None:
            return WorkerResult.failed(job.job_id, job.worker_role, "No worker registered for role")
        return worker.run(job)

    def submit_many(self, jobs: list[JobEnvelope]) -> list[WorkerResult]:
        return [self.submit(job) for job in jobs]

