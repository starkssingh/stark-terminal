from fastapi.testclient import TestClient

from stark_terminal_api.main import app


def test_health_endpoint_returns_prompt_53_retail_dashboard_milestone_status() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "stark-terminal-api",
        "version": "0.1.0",
        "prompt": "67",
        "architecture": "institutional-grade-foundation",
        "execution_apis_enabled": False,
        "audit_status": "strategy-research-workspace-milestone",
    }
