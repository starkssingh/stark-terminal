from fastapi.testclient import TestClient

from stark_terminal_api.main import app


def test_research_lake_health_endpoint_returns_expected_keys() -> None:
    client = TestClient(app)

    response = client.get("/research-lake/health")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "stark-terminal-research-lake"
    assert set(body) == {
        "service",
        "configured",
        "lake_root_exists",
        "parquet_root_exists",
        "research_artifacts_root_exists",
        "duckdb_available",
        "duckdb_reachable",
        "parquet_engine_available",
        "zones",
        "error",
    }


def test_research_lake_health_endpoint_does_not_expose_sensitive_urls() -> None:
    client = TestClient(app)

    body = client.get("/research-lake/health").json()

    assert "database_url" not in body
    assert "timescale_database_url" not in body
    assert "redis_url" not in body
    assert "postgresql" not in str(body).lower()
