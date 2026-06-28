from __future__ import annotations

import re
from typing import Any

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


HEALTH_ENDPOINTS = [
    "/analytics-foundation/health",
    "/numerical-analytics/health",
    "/returns-analytics/health",
    "/risk-analytics/health",
    "/relationship-analytics/health",
    "/time-series-diagnostics/health",
    "/regime-analytics/health",
    "/regime-features/health",
]

CONTRACT_ENDPOINTS = [
    "/analytics-foundation/contracts",
    "/analytics-foundation/dependencies",
    "/numerical-analytics/contracts",
    "/numerical-analytics/dependency-gate",
    "/returns-analytics/contracts",
    "/risk-analytics/contracts",
    "/relationship-analytics/contracts",
    "/time-series-diagnostics/contracts",
    "/regime-analytics/contracts",
    "/regime-analytics/readiness-template",
    "/regime-features/contracts",
    "/regime-features/readiness-template",
]

FORBIDDEN_SECRET_KEYS = {
    "database_url",
    "timescale_database_url",
    "redis_url",
    "clickhouse_url",
    "clickhouse_password",
    "kafka_bootstrap_servers",
    "broker_secret",
    "broker_token",
}


def _collect_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        keys = set(value)
        for nested in value.values():
            keys.update(_collect_keys(nested))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for item in value:
            keys.update(_collect_keys(item))
        return keys
    return set()


def _collect_boolean_flags(value: Any) -> dict[str, bool]:
    flags: dict[str, bool] = {}
    if isinstance(value, dict):
        for key, nested in value.items():
            if isinstance(nested, bool):
                flags[key] = nested
            else:
                flags.update(_collect_boolean_flags(nested))
    elif isinstance(value, list):
        for item in value:
            flags.update(_collect_boolean_flags(item))
    return flags


def test_all_analytics_regime_health_and_contract_endpoints_work() -> None:
    client = TestClient(app)

    for endpoint in [*HEALTH_ENDPOINTS, *CONTRACT_ENDPOINTS]:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint
        assert isinstance(response.json(), dict)


def test_health_endpoint_reports_prompt_35_analytics_regime_audit_status() -> None:
    client = TestClient(app)

    body = client.get("/health").json()

    assert body["prompt"] == "107"
    assert body["execution_apis_enabled"] is False
    assert body["audit_status"] == "retail-decision-console-internal-preview-milestone-closure"


def test_analytics_regime_api_responses_do_not_expose_secrets_or_actions() -> None:
    client = TestClient(app)
    action_terms = ("buy", "sell", "hold", "watch", "avoid")

    for endpoint in [*HEALTH_ENDPOINTS, *CONTRACT_ENDPOINTS]:
        body = client.get(endpoint).json()
        body_text = repr(body).lower()
        assert FORBIDDEN_SECRET_KEYS.isdisjoint(_collect_keys(body))
        assert "decisionobject(" not in body_text
        for term in action_terms:
            assert re.search(rf"\b{term}\b", body_text) is None, endpoint


def test_analytics_regime_api_dangerous_flags_are_false() -> None:
    client = TestClient(app)

    for endpoint in [*HEALTH_ENDPOINTS, *CONTRACT_ENDPOINTS]:
        body = client.get(endpoint).json()
        flags = _collect_boolean_flags(body)
        for key, value in flags.items():
            if any(
                marker in key
                for marker in [
                    "real_data_allowed",
                    "trade_signals_allowed",
                    "recommendations_allowed",
                    "decision_objects_allowed",
                    "execution_allowed",
                    "classification_allowed",
                    "feature_computation_allowed",
                    "feature_registry_writes_allowed",
                    "ready_for_classification",
                    "ready_for_production",
                ]
            ):
                assert value is False, f"{endpoint} {key}"
