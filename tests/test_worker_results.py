from pydantic import ValidationError
import pytest

from stark_terminal_core.domain.enums import JobStatus, WorkerRole
from stark_terminal_data_platform.workers.results import WorkerResult


def test_worker_result_succeeded_helper() -> None:
    result = WorkerResult.succeeded("job-1", WorkerRole.TEST_WORKER, {"value": 1})

    assert result.status == JobStatus.SUCCEEDED
    assert result.output == {"value": 1}
    assert result.finished_at is not None


def test_worker_result_failed_helper_sanitizes_errors() -> None:
    result = WorkerResult.failed(
        "job-1",
        WorkerRole.TEST_WORKER,
        "database_url=postgresql://secret",
    )

    assert result.status == JobStatus.FAILED
    assert result.error == "SanitizedWorkerError"


def test_worker_result_skipped_helper() -> None:
    result = WorkerResult.skipped("job-1", WorkerRole.TEST_WORKER, "disabled")

    assert result.status == JobStatus.SKIPPED
    assert result.error == "disabled"


def test_worker_result_output_must_be_json_serializable() -> None:
    with pytest.raises(ValidationError):
        WorkerResult.succeeded("job-1", WorkerRole.TEST_WORKER, {"bad": object()})

