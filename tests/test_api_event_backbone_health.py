from fastapi.testclient import TestClient

from stark_terminal_api.main import app


def test_event_backbone_health_endpoint_returns_expected_keys() -> None:
    client = TestClient(app)

    response = client.get("/event-backbone/health")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-event-backbone"
    for key in {
        "configured",
        "enabled",
        "reachable",
        "backend",
        "mode",
        "memory_fallback_enabled",
        "bootstrap_servers_present",
        "client_id",
        "schema_version",
        "default_topic_count",
        "error",
    }:
        assert key in body
    assert body["backend"] == "memory"


def test_event_backbone_health_endpoint_does_not_expose_raw_kafka_secrets() -> None:
    client = TestClient(app)

    body = client.get("/event-backbone/health").json()

    assert "kafka_bootstrap_servers" not in body
    assert "kafka_sasl_username" not in body
    assert "kafka_sasl_password" not in body


def test_event_backbone_topics_endpoint_returns_contracts_only() -> None:
    client = TestClient(app)

    response = client.get("/event-backbone/topics")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-event-backbone"
    assert body["mode"] == "memory"
    assert body["schema_version"] == "v1"
    assert "stark.development.system" in body["topics"]
    assert body["count"] == len(body["topics"])

