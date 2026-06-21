from fastapi.testclient import TestClient

from stark_terminal_api.main import app


def test_workers_health_endpoint_returns_expected_keys() -> None:
    client = TestClient(app)

    response = client.get("/workers/health")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-workers"
    assert body["enabled"] is False
    assert body["harness_mode"] == "in_process"
    assert body["registered_workers"] == 0
    assert body["available_roles"] == []
    assert body["background_threads_allowed"] is False
    assert body["infinite_loops_allowed"] is False
    assert body["status"] == "DISABLED"
    assert "error" in body


def test_workers_health_endpoint_does_not_expose_execution_enabled() -> None:
    body = TestClient(app).get("/workers/health").json()

    assert body.get("execution_apis_enabled") is not True
    assert "secret" not in str(body)

