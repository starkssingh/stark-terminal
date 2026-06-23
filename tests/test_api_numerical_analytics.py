from fastapi.testclient import TestClient

from stark_terminal_api.main import app


def test_numerical_analytics_health_endpoint_is_safe() -> None:
    response = TestClient(app).get("/numerical-analytics/health")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-numerical-analytics"
    assert body["enabled"] is True
    assert body["schema_version"] == "v1"
    assert body["dependency_stage"] == "contracts_and_safe_stdlib"
    assert body["real_data_allowed"] is False
    assert body["trade_signals_allowed"] is False
    assert body["recommendations_allowed"] is False
    assert body["decision_objects_allowed"] is False
    assert body["execution_allowed"] is False
    assert body["max_vector_length"] == 100000
    assert body["status"] == "healthy"


def test_numerical_analytics_contracts_endpoint_is_metadata_only() -> None:
    response = TestClient(app).get("/numerical-analytics/contracts")

    assert response.status_code == 200
    body = response.json()
    assert body["computation_scope"] == "contracts-and-safe-descriptive-stdlib-only"
    assert body["real_data_allowed_now"] is False
    assert body["trade_signals_allowed_now"] is False
    assert body["recommendations_allowed_now"] is False
    assert body["decision_objects_allowed_now"] is False
    assert body["execution_allowed_now"] is False
    assert body["allowed_summary_metrics"] == ["count", "min", "max", "mean"]
    assert "returns" in body["forbidden_analytics"]
    assert "volatility" in body["forbidden_analytics"]
    assert "drawdown" in body["forbidden_analytics"]


def test_numerical_analytics_dependency_gate_endpoint_blocks_heavy_deps() -> None:
    response = TestClient(app).get("/numerical-analytics/dependency-gate")

    assert response.status_code == 200
    body = response.json()
    assert body["dependency_stage"] == "contracts_and_safe_stdlib"
    assert body["heavy_dependencies_blocked"] is True
    assert body["no_new_heavy_dependencies"] is True
    assert "numpy" in body["blocked_now"]
    assert "scipy" in body["blocked_now"]


def test_numerical_analytics_api_does_not_expose_secrets_or_trade_calls() -> None:
    client = TestClient(app)
    text = "\n".join(
        [
            str(client.get("/numerical-analytics/health").json()).lower(),
            str(client.get("/numerical-analytics/contracts").json()).lower(),
            str(client.get("/numerical-analytics/dependency-gate").json()).lower(),
        ]
    )

    assert "password" not in text
    assert "api_key" not in text
    assert "broker_secret" not in text
    assert "trade_signals_allowed_now': true" not in text
    assert "recommendations_allowed_now': true" not in text
    assert "decision_objects_allowed_now': true" not in text
