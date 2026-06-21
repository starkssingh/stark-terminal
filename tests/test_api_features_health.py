from fastapi.testclient import TestClient

from stark_terminal_api.main import app


def test_features_health_endpoint_returns_expected_keys() -> None:
    body = TestClient(app).get("/features/health").json()

    assert body["service"] == "stark-terminal-feature-registry"
    assert body["enabled"] is False
    assert body["backend"] == "memory"
    assert body["feature_store_mode"] == "custom"
    assert body["external_backend_allowed"] is False
    assert body["registered_features"] == 0
    assert body["registered_feature_sets"] == 0
    assert body["quality_reports"] == 0
    assert body["lineage_records"] == 0
    assert body["lineage_required"] is True
    assert body["quality_report_required"] is True
    assert body["status"] == "disabled"
    assert "secret" not in str(body).lower()


def test_features_contracts_endpoint_returns_enums_without_computation() -> None:
    body = TestClient(app).get("/features/contracts").json()

    assert body["service"] == "stark-terminal-feature-registry"
    assert body["schema_version"] == "v1"
    assert body["feature_store_mode"] == "custom"
    assert "FLOAT" in body["feature_value_types"]
    assert "INSTRUMENT" in body["feature_entity_types"]
    assert "DAILY" in body["feature_frequencies"]
    assert "ACTIVE" in body["feature_statuses"]
    assert "PASS" in body["quality_statuses"]
    assert "feast implemented" not in str(body).lower()

