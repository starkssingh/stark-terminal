from __future__ import annotations

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


client = TestClient(app)


def test_decision_endpoints_do_not_include_execution_or_broker_routes() -> None:
    bad: list[str] = []
    for route in app.routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set())
        if not path.startswith("/decision"):
            continue
        lowered = path.lower()
        if "POST" in methods:
            bad.append(f"{path}:POST")
        for forbidden in ["/execute", "/execution", "/broker", "/order", "/trade", "/approval", "/override"]:
            if forbidden in lowered:
                bad.append(f"{path}:{forbidden}")

    assert bad == []


def test_decision_boundary_endpoints_do_not_expose_secrets_or_dangerous_true_flags() -> None:
    for endpoint in ["/decision-boundary/health", "/decision-boundary/contracts", "/decision-boundary/invariants"]:
        response = client.get(endpoint)
        assert response.status_code == 200
        text = str(response.json()).lower()
        for secret_term in ["password", "api_key", "token", "broker_secret"]:
            assert secret_term not in text
        for dangerous_true in [
            "recommendations_allowed': true",
            "action_generation_allowed': true",
            "confidence_scoring_allowed': true",
            "decision_object_generation_allowed': true",
            "execution_allowed': true",
            "approval_allowed': true",
            "override_allowed': true",
            "active_ui_allowed': true",
            "active_workflow_allowed': true",
            "readiness_to_trade_allowed': true",
            "approval_granted': true",
            "override_granted': true",
            "execution_ready': true",
        ]:
            assert dangerous_true not in text
