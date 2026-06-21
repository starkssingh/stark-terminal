from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.domain.enums import JobPriority, WorkerRole
from stark_terminal_data_platform.streams.serialization import (
    StreamSerializationError,
    ensure_stream_jsonable,
)
from stark_terminal_data_platform.workers.roles import (
    is_execution_forbidden_role,
    role_to_default_queue,
)


FORBIDDEN_JOB_PAYLOAD_KEY_PARTS = (
    "password",
    "secret",
    "token",
    "api_key",
    "database_url",
    "redis_url",
    "broker_token",
    "broker_secret",
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _has_forbidden_payload_key(value: Any) -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = str(key).lower()
            if any(part in normalized for part in FORBIDDEN_JOB_PAYLOAD_KEY_PARTS):
                return True
            if _has_forbidden_payload_key(item):
                return True
    elif isinstance(value, list | tuple):
        return any(_has_forbidden_payload_key(item) for item in value)
    return False


def ensure_job_payload_jsonable(value: Any) -> Any:
    if _has_forbidden_payload_key(value):
        raise ValueError("job payload contains forbidden secret-like keys")
    try:
        return ensure_stream_jsonable(value)
    except StreamSerializationError as exc:
        raise ValueError(str(exc)) from exc


class JobEnvelope(BaseModel):
    job_id: str = Field(default_factory=lambda: str(uuid4()))
    worker_role: WorkerRole
    job_type: str
    payload: dict[str, object]
    priority: JobPriority = JobPriority.NORMAL
    queue: str
    schema_version: str
    correlation_id: str | None = None
    causation_id: str | None = None
    audit_id: str | None = None
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("job_id", "job_type", "queue", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("job envelope text fields cannot be empty")
        if is_execution_forbidden_role(normalized):
            raise ValueError("execution, broker, order, or live-trading jobs are forbidden")
        return normalized

    @field_validator("worker_role")
    @classmethod
    def worker_role_must_be_safe(cls, value: WorkerRole) -> WorkerRole:
        if is_execution_forbidden_role(value):
            raise ValueError("execution, broker, order, or live-trading worker roles are forbidden")
        return value

    @field_validator("payload")
    @classmethod
    def payload_must_be_safe_json(cls, value: dict[str, object]) -> dict[str, object]:
        ensure_job_payload_jsonable(value)
        return value

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_utc_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)


def create_job_envelope(
    worker_role: WorkerRole,
    job_type: str,
    payload: dict[str, object],
    settings: Settings | None = None,
    priority: JobPriority = JobPriority.NORMAL,
    queue: str | None = None,
    correlation_id: str | None = None,
    causation_id: str | None = None,
    audit_id: str | None = None,
) -> JobEnvelope:
    resolved_settings = settings or get_settings()
    resolved_queue = queue or role_to_default_queue(worker_role) or resolved_settings.worker_default_queue
    return JobEnvelope(
        worker_role=worker_role,
        job_type=job_type,
        payload=payload,
        priority=priority,
        queue=resolved_queue,
        schema_version=resolved_settings.worker_schema_version,
        correlation_id=correlation_id,
        causation_id=causation_id,
        audit_id=audit_id,
    )

