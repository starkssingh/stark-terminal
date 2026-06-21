from stark_terminal_core.domain.enums import WorkerRole
from stark_terminal_data_platform.workers.roles import (
    CANONICAL_WORKER_ROLES,
    is_execution_forbidden_role,
    role_to_default_queue,
    role_to_description,
)


def test_canonical_worker_roles_exist() -> None:
    assert WorkerRole.INGESTION_WORKER in CANONICAL_WORKER_ROLES
    assert WorkerRole.SYSTEM_HEALTH_WORKER in CANONICAL_WORKER_ROLES
    assert WorkerRole.TEST_WORKER in CANONICAL_WORKER_ROLES


def test_role_to_default_queue_and_description() -> None:
    assert role_to_default_queue(WorkerRole.FEATURE_WORKER) == "feature_worker"
    assert "feature" in role_to_description(WorkerRole.FEATURE_WORKER).lower()


def test_execution_related_names_are_forbidden() -> None:
    assert is_execution_forbidden_role("execution_worker") is True
    assert is_execution_forbidden_role("order_placement_worker") is True
    assert is_execution_forbidden_role("broker_credential_worker") is True
    assert is_execution_forbidden_role("live_trading_worker") is True
    assert is_execution_forbidden_role(WorkerRole.TEST_WORKER) is False

