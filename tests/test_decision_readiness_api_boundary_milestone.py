from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)


def _phase_text() -> str:
    module_root = ROOT / "packages/core/stark_terminal_core/decision_readiness_api"
    route = ROOT / "apps/api/stark_terminal_api/routes/decision_readiness_api.py"
    return "\n".join(path.read_text(encoding="utf-8") for path in module_root.glob("*.py")) + "\n" + route.read_text(
        encoding="utf-8"
    )


def test_decision_readiness_api_remains_skeleton_only() -> None:
    text = _phase_text()

    for phrase in [
        "@router.post",
        "def generate_readiness_status",
        "def generate_recommendation",
        "def generate_decision_object",
        "def score_confidence",
        "DecisionObject(",
    ]:
        assert phrase not in text


def test_decision_readiness_api_endpoints_return_placeholders_only() -> None:
    contracts = client.get("/decision-readiness-api/contracts").json()
    placeholder = client.get("/decision-readiness-api/response-placeholder").json()
    unavailable = client.get("/decision-readiness-api/unavailable-template").json()

    assert contracts["computation_scope"] == "readiness-contract-skeleton-only"
    assert contracts["readiness_status_generation_allowed_now"] is False
    assert contracts["recommendations_allowed_now"] is False
    assert contracts["decision_object_generation_allowed_now"] is False
    assert unavailable["no_readiness_status_generation"] is True
    assert placeholder["readiness_status_generated"] is False
    assert placeholder["decision_object_generated"] is False
    assert placeholder["approval_granted"] is False
    assert placeholder["execution_ready"] is False
