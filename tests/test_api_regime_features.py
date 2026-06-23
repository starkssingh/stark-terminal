import re

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


FORBIDDEN_KEYS = {
    "database_url",
    "timescale_database_url",
    "redis_url",
    "clickhouse_url",
    "clickhouse_password",
    "kafka_bootstrap_servers",
    "broker_secret",
    "broker_token",
}


def _collect_keys(value: object) -> set[str]:
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


def test_regime_features_health_returns_safe_status() -> None:
    client = TestClient(app)

    response = client.get("/regime-features/health")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-regime-features"
    assert body["feature_computation_allowed"] is False
    assert body["feature_registry_writes_allowed"] is False
    assert body["classification_allowed"] is False
    assert body["trade_signals_allowed"] is False
    assert body["recommendations_allowed"] is False
    assert body["decision_objects_allowed"] is False
    assert body["execution_allowed"] is False
    assert body["provenance_required"] is True
    assert body["evidence_mapping_required"] is True
    assert body["status"] == "healthy"


def test_regime_features_contracts_return_groups_and_forbidden_outputs() -> None:
    client = TestClient(app)

    response = client.get("/regime-features/contracts")

    assert response.status_code == 200
    body = response.json()
    assert body["computation_scope"] == "contracts-and-preparation-only"
    assert body["feature_computation_allowed_now"] is False
    assert body["feature_registry_writes_allowed_now"] is False
    assert body["classification_allowed_now"] is False
    assert body["real_data_allowed_now"] is False
    assert body["trade_signals_allowed_now"] is False
    assert body["recommendations_allowed_now"] is False
    assert body["decision_objects_allowed_now"] is False
    assert body["execution_allowed_now"] is False
    assert "RETURNS" in body["feature_groups"]
    assert "returns_momentum_summary" in body["candidate_feature_names"]
    assert "feature_computation" in body["forbidden_outputs"]


def test_regime_features_readiness_template_does_not_compute_or_classify() -> None:
    client = TestClient(app)

    response = client.get("/regime-features/readiness-template")

    assert response.status_code == 200
    body = response.json()
    assert body["preparation_only"] is True
    assert body["feature_computation_allowed_now"] is False
    assert body["classification_allowed_now"] is False
    assert body["must_not_compute_features"] is True
    assert body["must_not_classify_market_state"] is True
    assert body["must_not_generate_signals_or_decisions"] is True
    assert body["readiness_report"]["ready_for_feature_computation"] is False
    assert body["readiness_report"]["ready_for_classification"] is False


def test_regime_features_dependency_gate_is_safe() -> None:
    client = TestClient(app)

    response = client.get("/regime-features/dependency-gate")

    assert response.status_code == 200
    body = response.json()
    assert body["current_stage"] == "contracts_only"
    assert body["heavy_dependencies_blocked"] is True
    assert body["feature_computation_allowed"] is False
    assert "scipy" in body["blocked_now"]


def test_regime_feature_endpoints_do_not_expose_secrets_or_decisions() -> None:
    client = TestClient(app)

    for endpoint in [
        "/regime-features/health",
        "/regime-features/contracts",
        "/regime-features/readiness-template",
        "/regime-features/dependency-gate",
    ]:
        body = client.get(endpoint).json()
        body_text = repr(body).lower()
        assert FORBIDDEN_KEYS.isdisjoint(_collect_keys(body))
        for term in ["buy", "sell", "hold", "watch", "avoid"]:
            assert re.search(rf"\b{term}\b", body_text) is None
        assert "decisionobject(" not in body_text
