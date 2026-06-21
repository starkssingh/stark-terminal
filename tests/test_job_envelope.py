from datetime import timezone

from pydantic import ValidationError
import pytest

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import JobPriority, WorkerRole
from stark_terminal_data_platform.workers.jobs import JobEnvelope, create_job_envelope


def test_valid_job_envelope_creation() -> None:
    job = JobEnvelope(
        worker_role=WorkerRole.TEST_WORKER,
        job_type="echo",
        payload={"value": 1},
        queue="test",
        schema_version="v1",
    )

    assert job.job_id
    assert job.priority == JobPriority.NORMAL
    assert job.created_at.tzinfo is not None


def test_create_job_envelope_generates_uuid_and_utc_timestamp() -> None:
    job = create_job_envelope(
        WorkerRole.TEST_WORKER,
        "echo",
        {"value": 1},
        settings=Settings(),
    )

    assert job.job_id
    assert job.queue == "test_worker"
    assert job.schema_version == "v1"
    assert job.created_at.utcoffset() == timezone.utc.utcoffset(job.created_at)


def test_job_envelope_payload_must_be_json_serializable() -> None:
    with pytest.raises(ValidationError):
        create_job_envelope(WorkerRole.TEST_WORKER, "echo", {"bad": object()}, settings=Settings())


@pytest.mark.parametrize("key", ["password", "secret_value", "api_key", "database_url", "redis_url", "broker_token", "broker_secret"])
def test_job_envelope_rejects_forbidden_payload_keys(key: str) -> None:
    with pytest.raises(ValidationError):
        create_job_envelope(WorkerRole.TEST_WORKER, "echo", {key: "value"}, settings=Settings())


@pytest.mark.parametrize("job_type", ["execution_job", "order_placement", "broker_call", "live_trading"])
def test_job_envelope_rejects_forbidden_job_types(job_type: str) -> None:
    with pytest.raises(ValidationError):
        create_job_envelope(WorkerRole.TEST_WORKER, job_type, {}, settings=Settings())


@pytest.mark.parametrize("field,value", [("queue", ""), ("schema_version", "")])
def test_job_envelope_queue_and_schema_validation(field: str, value: str) -> None:
    kwargs = {
        "worker_role": WorkerRole.TEST_WORKER,
        "job_type": "echo",
        "payload": {},
        "queue": "test",
        "schema_version": "v1",
    }
    kwargs[field] = value
    with pytest.raises(ValidationError):
        JobEnvelope(**kwargs)

