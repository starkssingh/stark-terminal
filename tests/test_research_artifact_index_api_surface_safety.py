from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)


INDEX_ROUTE_FILES = [
    ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index.py",
    ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index_api.py",
    ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index_display.py",
]


def test_research_artifact_index_route_families_have_no_post_endpoints() -> None:
    for path in INDEX_ROUTE_FILES:
        source = path.read_text(encoding="utf-8")
        assert "@router.post" not in source
        assert "@router.put" not in source
        assert "@router.delete" not in source


def test_research_artifact_index_health_reflects_prompt_80_boundary_audit() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["prompt"] == "107"
    assert body["audit_status"] == "retail-decision-console-internal-preview-milestone-closure"
    assert body["execution_apis_enabled"] is False
