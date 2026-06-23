from fastapi.testclient import TestClient

from stark_terminal_api.main import app


def test_analytics_foundation_health_endpoint_is_safe() -> None:
    response = TestClient(app).get("/analytics-foundation/health")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-analytics-foundation"
    assert body["enabled"] is True
    assert body["schema_version"] == "v1"
    assert body["dependency_stage"] == "contracts_only"
    assert body["real_data_allowed"] is False
    assert body["trade_signals_allowed"] is False
    assert body["recommendations_allowed"] is False
    assert body["execution_allowed"] is False
    assert body["module_plan_count"] >= 9
    assert body["roadmap_item_count"] >= 7
    assert body["status"] == "healthy"


def test_analytics_foundation_contracts_endpoint_is_planning_only() -> None:
    response = TestClient(app).get("/analytics-foundation/contracts")

    assert response.status_code == 200
    body = response.json()
    assert body["computation_implemented_now"] is False
    assert body["signals_allowed_now"] is False
    assert body["recommendations_allowed_now"] is False
    assert body["execution_allowed_now"] is False
    assert "returns_analytics" in body["planned_modules"]
    assert "Prompt 30" in body["planned_next_prompts"]


def test_analytics_foundation_dependencies_endpoint_requires_no_heavy_deps() -> None:
    response = TestClient(app).get("/analytics-foundation/dependencies")

    assert response.status_code == 200
    body = response.json()
    assert body["current_stage"] == "CONTRACTS_ONLY"
    assert body["heavy_dependencies_installed_now"] is False
    assert body["computation_implemented_now"] is False
    assert body["no_signals"] is True
    assert body["no_recommendations"] is True
    assert body["no_execution_apis"] is True
    assert "NumPy" in body["blocked_heavy_dependencies_now"]


def test_analytics_foundation_api_does_not_expose_secrets_or_trade_calls() -> None:
    client = TestClient(app)
    text = "\n".join(
        [
            str(client.get("/analytics-foundation/health").json()).lower(),
            str(client.get("/analytics-foundation/contracts").json()).lower(),
            str(client.get("/analytics-foundation/dependencies").json()).lower(),
        ]
    )

    assert "password" not in text
    assert "api_key" not in text
    assert "buy" not in text
    assert "sell" not in text
    assert "recommendations_allowed_now': true" not in text
    assert "signals_allowed_now': true" not in text
