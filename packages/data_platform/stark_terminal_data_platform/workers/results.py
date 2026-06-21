from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field, field_validator

from stark_terminal_core.domain.enums import JobStatus, WorkerRole
from stark_terminal_data_platform.workers.jobs import ensure_job_payload_jsonable


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sanitize_error(error: str | BaseException | None) -> str | None:
    if error is None:
        return None
    if isinstance(error, BaseException):
        return error.__class__.__name__
    lowered = str(error)
    forbidden = ("password", "secret", "token", "api_key", "database_url", "redis_url", "broker")
    if any(term in lowered.lower() for term in forbidden):
        return "SanitizedWorkerError"
    return lowered


class WorkerResult(BaseModel):
    job_id: str
    worker_role: WorkerRole
    status: JobStatus
    started_at: datetime
    finished_at: datetime | None = None
    output: dict[str, object] = Field(default_factory=dict)
    error: str | None = None
    retryable: bool = False
    audit_id: str | None = None

    @field_validator("job_id")
    @classmethod
    def job_id_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("job_id cannot be empty")
        return normalized

    @field_validator("started_at", "finished_at")
    @classmethod
    def timestamps_must_be_utc_aware(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @field_validator("output")
    @classmethod
    def output_must_be_safe_json(cls, value: dict[str, object]) -> dict[str, object]:
        ensure_job_payload_jsonable(value)
        return value

    @field_validator("error")
    @classmethod
    def error_must_be_sanitized(cls, value: str | None) -> str | None:
        return sanitize_error(value)

    @classmethod
    def succeeded(
        cls,
        job_id: str,
        worker_role: WorkerRole,
        output: dict[str, object] | None = None,
        started_at: datetime | None = None,
        finished_at: datetime | None = None,
        audit_id: str | None = None,
    ) -> WorkerResult:
        now = _utc_now()
        return cls(
            job_id=job_id,
            worker_role=worker_role,
            status=JobStatus.SUCCEEDED,
            started_at=started_at or now,
            finished_at=finished_at or _utc_now(),
            output=output or {},
            audit_id=audit_id,
        )

    @classmethod
    def failed(
        cls,
        job_id: str,
        worker_role: WorkerRole,
        error: str | BaseException,
        retryable: bool = False,
        output: dict[str, object] | None = None,
        started_at: datetime | None = None,
        finished_at: datetime | None = None,
        audit_id: str | None = None,
    ) -> WorkerResult:
        now = _utc_now()
        return cls(
            job_id=job_id,
            worker_role=worker_role,
            status=JobStatus.FAILED,
            started_at=started_at or now,
            finished_at=finished_at or _utc_now(),
            output=output or {},
            error=sanitize_error(error),
            retryable=retryable,
            audit_id=audit_id,
        )

    @classmethod
    def skipped(
        cls,
        job_id: str,
        worker_role: WorkerRole,
        reason: str = "Skipped",
        started_at: datetime | None = None,
        finished_at: datetime | None = None,
        audit_id: str | None = None,
    ) -> WorkerResult:
        now = _utc_now()
        return cls(
            job_id=job_id,
            worker_role=worker_role,
            status=JobStatus.SKIPPED,
            started_at=started_at or now,
            finished_at=finished_at or _utc_now(),
            output={},
            error=sanitize_error(reason),
            audit_id=audit_id,
        )

