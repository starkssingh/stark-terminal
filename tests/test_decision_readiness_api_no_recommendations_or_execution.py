from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_decision_readiness_api_modules_do_not_generate_outputs_or_approvals() -> None:
    module_root = ROOT / "packages/core/stark_terminal_core/decision_readiness_api"
    route_path = ROOT / "apps/api/stark_terminal_api/routes/decision_readiness_api.py"
    text = "\n".join(path.read_text(encoding="utf-8") for path in module_root.glob("*.py"))
    text += "\n" + route_path.read_text(encoding="utf-8")

    forbidden = [
        "def approve_decision",
        "def override_decision",
        "def generate_decision_object",
        "def generate_recommendation",
        "def generate_action",
        "def generate_readiness_status",
        "def score_confidence",
        "def compute_confidence",
        "DecisionObject(",
        "@router.post",
    ]
    for phrase in forbidden:
        assert phrase not in text


def test_decision_readiness_api_routes_and_docs_forbid_execution() -> None:
    route_text = (ROOT / "apps/api/stark_terminal_api/routes/decision_readiness_api.py").read_text(
        encoding="utf-8"
    )
    docs_text = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "docs").glob("DECISION_READINESS*.md"))
    docs_text += "\n" + (ROOT / "docs/DECISION_DESK_READINESS_API_SKELETON.md").read_text(encoding="utf-8")

    assert "/decision-readiness-api" in route_text
    assert "recommendations_allowed_now" in route_text
    assert "readiness_status_generation_allowed_now" in route_text
    assert "decision_object_generation_allowed_now" in route_text
    assert "execution_allowed_now" in route_text
    assert "approval_allowed_now" in route_text
    assert "override_allowed_now" in route_text
    assert "no recommendations" in docs_text
    assert "no DecisionObject generation" in docs_text
    assert "no approval" in docs_text
    assert "no override" in docs_text
    assert "no execution APIs" in docs_text
    assert "readiness-to-trade" in docs_text
    assert "buy/sell/hold/watch/avoid" not in route_text.lower()
