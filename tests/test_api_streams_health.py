from fastapi.testclient import TestClient

from stark_terminal_api.main import app


def test_streams_health_endpoint_returns_expected_keys() -> None:
    client = TestClient(app)

    response = client.get("/streams/health")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-streams"
    assert body["configured"] is False
    assert body["enabled"] is False
    assert body["reachable"] is True
    assert body["backend"] == "memory"
    assert body["memory_fallback_enabled"] is True
    assert body["redis_url_present"] is False
    assert body["consumer_group"] == "stark-terminal"
    assert body["stream_schema_version"] == "v1"
    assert "error" in body


def test_streams_health_endpoint_does_not_expose_raw_redis_url() -> None:
    client = TestClient(app)

    body = client.get("/streams/health").json()

    assert "redis_url" not in body
    assert "redis://" not in str(body)

