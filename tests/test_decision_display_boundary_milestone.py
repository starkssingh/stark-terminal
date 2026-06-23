from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)


def _display_text() -> str:
    module_root = ROOT / "packages/core/stark_terminal_core/decision_display"
    route = ROOT / "apps/api/stark_terminal_api/routes/decision_display.py"
    return "\n".join(path.read_text(encoding="utf-8") for path in module_root.glob("*.py")) + "\n" + route.read_text(
        encoding="utf-8"
    )


def test_decision_display_remains_contract_skeleton_only() -> None:
    text = _display_text()

    for phrase in [
        "@router.post",
        "def build_active_decision_card",
        "def generate_recommendation",
        "def generate_action",
        "def score_confidence",
        "DecisionObject(",
        "PySide6",
        "React",
    ]:
        assert phrase not in text


def test_decision_display_layout_has_no_active_ui_or_trade_readiness() -> None:
    layout = client.get("/decision-display/placeholder-layout").json()

    assert layout["display_contract_skeleton_only"] is True
    assert layout["active_ui"] is False
    assert layout["recommendation_generated"] is False
    assert layout["confidence_generated"] is False
    assert layout["decision_object_generated"] is False
    assert layout["readiness_to_trade_generated"] is False
    assert layout["execution_ready"] is False
    assert layout["approval_granted"] is False
    assert layout["override_granted"] is False
